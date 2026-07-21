#!/usr/bin/env python3
"""企业微信智能机器人 <-> Claude Code session 桥接器。

依赖企业微信「智能机器人·长连接模式」(wss://openws.work.weixin.qq.com):
  pip install wecom-aibot-sdk

数据流:
  企微用户发消息 -> aibot_msg_callback -> 本进程 stdout 打一行 WECOM_MSG JSON
    (由 Claude session 的持久 Monitor 捕获, 变成对话事件)
  本进程同时用流式回复立即回一句占位确认。
  Claude 生成回答后写入 outbox 目录 (JSON: {"chatid": ..., "markdown": ...})
    -> 本进程轮询到之后用 aibot_send_msg 主动推送回企微。

凭证来源(按优先级): 环境变量 WECOM_BOT_ID / WECOM_BOT_SECRET,
或仓库根目录 .wecom.env (KEY=VALUE 每行一条, 已被 .gitignore 排除)。

stdout 只输出事件行(供 Monitor 消费), 运行日志全部走 stderr。
"""

from __future__ import annotations

import asyncio
import json
import os
import ssl
import sys
import uuid
from pathlib import Path

from wecom_aibot_sdk import WSClient

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".wecom.env"
OUTBOX_DIR = Path(os.environ.get("WECOM_OUTBOX", REPO_ROOT / ".wecom" / "outbox"))
SENT_DIR = OUTBOX_DIR.parent / "sent"
CA_BUNDLE = os.environ.get("WECOM_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
ACK_TEXT = "✅ 已收到，研究助手正在处理，稍后回复…"
MARKDOWN_CHUNK = 3500  # 企微单条 markdown 消息长度上限内的安全值


def log(*args: object) -> None:
    print(*args, file=sys.stderr, flush=True)


def emit(kind: str, payload: dict) -> None:
    """向 stdout 输出一行事件, 供 Monitor 捕获。"""
    print(f"{kind} {json.dumps(payload, ensure_ascii=False)}", flush=True)


class StderrLogger:
    def debug(self, message: str, *args: object) -> None:
        log("[debug]", message, *args)

    def info(self, message: str, *args: object) -> None:
        log("[info]", message, *args)

    def warn(self, message: str, *args: object) -> None:
        log("[warn]", message, *args)

    def error(self, message: str, *args: object) -> None:
        log("[error]", message, *args)


def load_credentials() -> tuple[str, str]:
    bot_id = os.environ.get("WECOM_BOT_ID", "")
    secret = os.environ.get("WECOM_BOT_SECRET", "")
    if (not bot_id or not secret) and ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key == "WECOM_BOT_ID" and not bot_id:
                bot_id = value
            elif key == "WECOM_BOT_SECRET" and not secret:
                secret = value
    if not bot_id or not secret:
        log("[fatal] 缺少凭证: 请设置 WECOM_BOT_ID/WECOM_BOT_SECRET 或创建 .wecom.env")
        sys.exit(1)
    return bot_id, secret


def build_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if os.path.exists(CA_BUNDLE):
        ctx.load_verify_locations(cafile=CA_BUNDLE)
    return ctx


def summarize_message(body: dict) -> dict:
    """把 aibot_msg_callback 的 body 压缩成给 Claude 看的一行 JSON。"""
    msgtype = body.get("msgtype", "")
    sender = body.get("from") or {}
    chatid = body.get("chatid") or sender.get("userid") or ""
    summary = {
        "chatid": chatid,
        "chattype": body.get("chattype", ""),
        "from": sender.get("userid", ""),
        "msgtype": msgtype,
        "msgid": body.get("msgid", ""),
    }
    if msgtype == "text":
        summary["content"] = (body.get("text") or {}).get("content", "")
    elif msgtype == "mixed":
        items = (body.get("mixed") or {}).get("msg_item", [])
        texts = [
            (item.get("text") or {}).get("content", "")
            for item in items
            if item.get("msgtype") == "text"
        ]
        summary["content"] = " ".join(t for t in texts if t)
        summary["has_media"] = any(item.get("msgtype") != "text" for item in items)
    else:
        # 非文本消息: 原样带上 body 供排查(截断防止刷屏)
        summary["raw_body"] = json.dumps(body, ensure_ascii=False)[:800]
    return summary


async def send_markdown(client: WSClient, chatid: str, content: str) -> None:
    """主动推送 markdown, 超长自动分段。"""
    chunks = [content[i : i + MARKDOWN_CHUNK] for i in range(0, len(content), MARKDOWN_CHUNK)] or [""]
    for index, chunk in enumerate(chunks):
        await client.send_message(chatid, {"msgtype": "markdown", "markdown": {"content": chunk}})
        if index < len(chunks) - 1:
            await asyncio.sleep(2.5)  # 限速 30 条/分钟, 留出余量


async def outbox_loop(client: WSClient) -> None:
    """轮询 outbox 目录, 把 Claude 写入的回复发回企微。"""
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    SENT_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        for path in sorted(OUTBOX_DIR.glob("*.json")):
            try:
                data = json.loads(path.read_text())
                chatid = data["chatid"]
                content = data.get("markdown") or data.get("content") or ""
                if not content:
                    raise ValueError("outbox 文件缺少 markdown/content 字段")
                await send_markdown(client, chatid, content)
                path.rename(SENT_DIR / path.name)
                emit("WECOM_SENT", {"file": path.name, "chatid": chatid})
            except Exception as err:  # noqa: BLE001 — 单个文件失败不拖垮循环
                emit("WECOM_SEND_ERROR", {"file": path.name, "error": str(err)})
                path.rename(path.with_suffix(".failed"))
        await asyncio.sleep(2)


def main() -> None:
    bot_id, secret = load_credentials()
    client = WSClient(
        bot_id,
        secret,
        max_reconnect_attempts=-1,  # 网络抖动时无限重连
        ws_options={"ssl": build_ssl_context()},
        logger=StderrLogger(),
    )

    async def on_message(frame: dict) -> None:
        body = frame.get("body") or {}
        summary = summarize_message(body)
        emit("WECOM_MSG", summary)
        try:
            await client.reply_stream(frame, uuid.uuid4().hex, ACK_TEXT, finish=True)
        except Exception as err:  # noqa: BLE001
            log("[warn] 占位确认发送失败:", err)

    client.on("message", on_message)
    client.on("authenticated", lambda: emit("WECOM_STATUS", {"state": "authenticated"}))
    client.on("disconnected", lambda reason: emit("WECOM_STATUS", {"state": "disconnected", "reason": str(reason)}))
    client.on(
        "event.disconnected_event",
        lambda _frame: emit("WECOM_STATUS", {"state": "kicked", "reason": "同一机器人建立了新的长连接, 本连接被服务端断开"}),
    )
    client.on("error", lambda err: emit("WECOM_STATUS", {"state": "error", "error": str(err)}))

    async def run() -> None:
        await client.connect()
        await outbox_loop(client)  # 常驻

    asyncio.run(run())


if __name__ == "__main__":
    main()
