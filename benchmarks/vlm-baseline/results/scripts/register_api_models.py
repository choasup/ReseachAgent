#!/usr/bin/env python3
"""为新增开源模型批量注册 VLMEvalKit API 条目（LMDeployAPI, 端口 18011 轮换）。幂等。
采样参数策略: 不显式传 temperature/top_p（LMDeployAPI 过滤 None），由 vLLM serve
加载各模型自带 generation_config 作为默认 —— 每家用官方推荐配置，公平且零维护。
用法: python register_api_models.py <VLMEvalKit根>"""
import sys, os

ROOT = sys.argv[1]
cfg_path = os.path.join(ROOT, "vlmeval", "config.py")

# (VLMEvalKit 注册名, served-model-name)
MODELS = [
    ("InternVL3-8B-vllm", "InternVL3-8B"),
    ("Qwen2.5-VL-7B-vllm", "Qwen2.5-VL-7B-Instruct"),
    ("MiniCPM-V-2.6-vllm", "MiniCPM-V-2_6"),
    ("Ovis2-8B-vllm", "Ovis2-8B"),
    ("LLaVA-OneVision-7B-vllm", "llava-onevision-qwen2-7b-ov-hf"),
    ("Phi-3.5-Vision-vllm", "Phi-3.5-vision-instruct"),
    ("Idefics3-8B-vllm", "Idefics3-8B-Llama3"),
    ("DeepSeek-VL2-small-vllm", "deepseek-vl2-small"),
    ("Pixtral-12B-vllm", "Pixtral-12B-2409"),
]

src = open(cfg_path, encoding="utf-8").read()
anchor = '    "GLM4_1VThinking-9b-vllm": partial(\n'
assert anchor in src, "anchor not found"
block = ""
for reg, served in MODELS:
    if f'"{reg}"' in src:
        print(f"  already: {reg}")
        continue
    block += (
        f'    "{reg}": partial(\n'
        f'        api.LMDeployAPI,\n'
        f'        api_base="http://127.0.0.1:18011/v1/chat/completions",\n'
        f'        model="{served}",\n'
        f'        temperature=None, max_tokens=8192, timeout=600, retry=8,\n'
        f'    ),\n'
    )
    print(f"  added: {reg} -> {served}")
if block:
    src = src.replace(anchor, block + anchor, 1)
    open(cfg_path, "w", encoding="utf-8").write(src)
print("REGISTER_API_OK")
