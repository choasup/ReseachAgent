#!/usr/bin/env python3
"""给 VLMEvalKit 打 ROCm(gfx942/MI308X) 补丁。用法: python patch_vlmevalkit.py <VLMEvalKit根目录>

改动（全部有断言，重复执行安全）:
1. 新增 vlmeval/vlm/rocm_fix.py: Conv3d(kernel==stride)->matmul 绕 MIOpen 段错误;
   SDPA 限制 math 后端(mem-efficient kernel 在 gfx942 视觉塔上静默算错).
2. qwen3_vl/model.py: flash_attention_2 -> eager(ROCm 无 flash-attn; SDPA 有静默损坏),
   加载后 apply_rocm_patches.
3. cogvlm.py GLMThinking GLM-4.1V 分支: 加 attn_implementation='eager' + apply_rocm_patches.
4. molmo.py: 加载后 apply_rocm_patches(remote code 不强改 attn 实现, 靠 math-sdpa 兜底).
5. config.py: Qwen3-VL-8B-Instruct 的 use_vllm=True -> False(本环境走 transformers).
"""
import sys, os, re

ROOT = sys.argv[1]
VLM = os.path.join(ROOT, "vlmeval", "vlm")

ROCM_FIX = '''"""ROCm gfx942 (MI308X) fixes. 源: 013_mllm/rocm_patches.py, 2026-07-06/07 定位.

- Conv2d/Conv3d(kernel==stride, 输入空间维==kernel) 在 MIOpen 上段错误 -> 等价 matmul.
  (Qwen3-VL patch_embed Conv3d; GLM-4.1V patch_embed Conv3d + downsample Conv2d)
- SDPA 的非 math 后端对视觉塔静默输出错误结果 -> 只留 math 后端.
"""
from types import MethodType

import torch
import torch.nn as nn


def _linear_convnd_forward(self, x):
    if tuple(x.shape[2:]) == tuple(self.kernel_size):
        w = self.weight.flatten(1)
        y = x.flatten(1) @ w.t()
        if self.bias is not None:
            y = y + self.bias
        return y.view(y.shape[0], y.shape[1], *([1] * len(self.kernel_size)))
    # 其他形状走原实现
    return self._conv_forward(x, self.weight, self.bias)


def restrict_sdpa_to_math(verbose=True):
    if torch.version.hip is None:
        return False
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    torch.backends.cuda.enable_math_sdp(True)
    if verbose:
        print("[rocm_fix] SDPA restricted to math backend")
    return True


def apply_rocm_patches(model, verbose=True):
    if torch.version.hip is None:
        return 0
    restrict_sdpa_to_math(verbose)
    n = 0
    for name, mod in model.named_modules():
        if isinstance(mod, (nn.Conv2d, nn.Conv3d)) and tuple(mod.kernel_size) == tuple(mod.stride):
            mod.forward = MethodType(_linear_convnd_forward, mod)
            n += 1
            if verbose:
                print(f"[rocm_fix] {type(mod).__name__} -> matmul: {name}")
    return n
'''


def patch_file(path, pairs):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    changed = False
    for old, new in pairs:
        if new in src:
            print(f"  already patched: {path} :: {new[:60]!r}")
            continue
        assert old in src, f"pattern NOT FOUND in {path}:\n{old}"
        src = src.replace(old, new, 1)
        changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
        print(f"  patched: {path}")


# 1. rocm_fix.py
fix_path = os.path.join(VLM, "rocm_fix.py")
with open(fix_path, "w", encoding="utf-8") as f:
    f.write(ROCM_FIX)
print(f"  wrote: {fix_path}")

# 2. qwen3_vl/model.py
patch_file(os.path.join(VLM, "qwen3_vl", "model.py"), [
    (
        "                self.model = AutoModelForImageTextToText.from_pretrained(\n"
        "                    model_path, torch_dtype='auto', device_map='auto', attn_implementation='flash_attention_2'\n"
        "                )\n"
        "            self.model.eval()",
        "                self.model = AutoModelForImageTextToText.from_pretrained(\n"
        "                    model_path, torch_dtype='auto', device_map='auto', attn_implementation='eager'\n"
        "                )\n"
        "            from ..rocm_fix import apply_rocm_patches\n"
        "            apply_rocm_patches(self.model)\n"
        "            self.model.eval()",
    ),
])

# 3. cogvlm.py (GLMThinking, GLM-4.1V 分支)
patch_file(os.path.join(VLM, "cogvlm.py"), [
    (
        "                self.model = Glm4vForConditionalGeneration.from_pretrained(\n"
        "                    pretrained_model_name_or_path=model_path,\n"
        "                    torch_dtype=torch.bfloat16,\n"
        "                    local_files_only=True,\n"
        "                    trust_remote_code=True\n"
        "                ).to(self.device)",
        "                self.model = Glm4vForConditionalGeneration.from_pretrained(\n"
        "                    pretrained_model_name_or_path=model_path,\n"
        "                    torch_dtype=torch.bfloat16,\n"
        "                    local_files_only=True,\n"
        "                    trust_remote_code=True,\n"
        "                    attn_implementation='eager'\n"
        "                ).to(self.device)\n"
        "                from .rocm_fix import apply_rocm_patches\n"
        "                apply_rocm_patches(self.model)",
    ),
])

# 4b. molmo.py: MMMU split 的导入路径错误（顶层无 MMMUDataset）
patch_file(os.path.join(VLM, "molmo.py"), [
    ("            from .. import MMMUDataset\n",
     "            from ..dataset import MMMUDataset\n"),
])

# 4. molmo.py
patch_file(os.path.join(VLM, "molmo.py"), [
    (
        "        self.processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16)",  # noqa: E501
        "        from .rocm_fix import apply_rocm_patches\n"
        "        apply_rocm_patches(self.model)\n"
        "        self.processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16)",  # noqa: E501
    ),
])

# 5. smp/misc.py: get_gpu_memory 在 ROCm 上没有 nvidia-smi -> 用 torch.cuda.mem_get_info
patch_file(os.path.join(ROOT, "vlmeval", "smp", "misc.py"), [
    (
        "def get_gpu_memory():\n"
        "    import subprocess\n"
        "    try:\n",
        "def get_gpu_memory():\n"
        "    import subprocess\n"
        "    try:  # ROCm: nvidia-smi 不存在, 用 torch 查询空闲显存(MiB)\n"
        "        import torch\n"
        "        if torch.cuda.is_available() and torch.version.hip is not None:\n"
        "            return [int(torch.cuda.mem_get_info(i)[0] // 1048576)\n"
        "                    for i in range(torch.cuda.device_count())]\n"
        "    except Exception as e:\n"
        "        print(f'{type(e)}: {str(e)}')\n"
        "    try:\n",
    ),
])

# 6. config.py: Qwen3-VL-8B-Instruct -> use_vllm=False
cfg_path = os.path.join(ROOT, "vlmeval", "config.py")
with open(cfg_path, encoding="utf-8") as f:
    cfg = f.read()
i = cfg.index('"Qwen3-VL-8B-Instruct": partial(')
j = cfg.index("),", i)
block = cfg[i:j]
if "use_vllm=False" in block:
    print("  config.py already patched")
else:
    assert "use_vllm=True" in block, "use_vllm=True not found in Qwen3-VL-8B-Instruct block"
    cfg = cfg[:i] + block.replace("use_vllm=True", "use_vllm=False", 1) + cfg[j:]
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(cfg)
    print("  patched: config.py (Qwen3-VL-8B-Instruct use_vllm=False)")

# 7. config.py: 注册两个本地 vLLM serve 的 API 模型（ROCm 上 transformers 逐样本太慢）
#    采样参数与各自 HF generation_config / VLMEvalKit transformers 路径一致
API_ENTRIES = (
    '    "GLM4_1VThinking-9b": partial(vlm.GLMThinking, model_path="THUDM/GLM-4.1V-9B-Thinking"),\n'
    '    "Qwen3-VL-8B-Instruct-vllm": partial(\n'
    '        api.LMDeployAPI,\n'
    '        api_base="http://127.0.0.1:18001/v1/chat/completions",\n'
    '        model="Qwen3-VL-8B-Instruct",\n'
    '        temperature=0.7, top_p=0.8, top_k=20, presence_penalty=1.5,\n'
    '        max_tokens=16384, timeout=600, retry=8,\n'
    '    ),\n'
    '    "GLM4_1VThinking-9b-vllm": partial(\n'
    '        api.LMDeployAPI,\n'
    '        api_base="http://127.0.0.1:18002/v1/chat/completions",\n'
    '        model="GLM-4.1V-9B-Thinking",\n'
    '        temperature=0.8, top_p=0.6, top_k=2,\n'
    '        max_tokens=8192, timeout=600, retry=8,\n'
    '    ),\n'
)
patch_file(cfg_path, [
    (
        '    "GLM4_1VThinking-9b": partial(vlm.GLMThinking, model_path="THUDM/GLM-4.1V-9B-Thinking"),\n',
        API_ENTRIES,
    ),
])

# 8. lmdeploy.py: GLM thinking 模型 API 输出清理类（等价 GLMThinking.extract_answer）
lmd_path = os.path.join(ROOT, "vlmeval", "api", "lmdeploy.py")
GLM_CLEAN = '''

class GLMAnswerClean(LMDeployAPI):
    """GLM thinking 系列经 OpenAI 兼容 API 的输出清理:
    去掉 <answer>/</answer>/<|begin_of_box|>/<|end_of_box|>/<think> 标记,
    与 vlm.GLMThinking.extract_answer 的口径对齐, 避免污染 exact_matching."""

    def generate(self, message, **kwargs1):
        import re
        out = super().generate(message, **kwargs1)
        if isinstance(out, str):
            out = re.sub(
                r"</?answer>|<\\|begin_of_box\\|>|<\\|end_of_box\\|>|</?think>", "", out
            ).strip()
        return out
'''
with open(lmd_path, encoding="utf-8") as f:
    lmd = f.read()
if "class GLMAnswerClean" not in lmd:
    with open(lmd_path, "a", encoding="utf-8") as f:
        f.write(GLM_CLEAN)
    print("  patched: lmdeploy.py (+GLMAnswerClean)")
else:
    print("  already patched: lmdeploy.py")

# 9. api/__init__.py 导出
patch_file(os.path.join(ROOT, "vlmeval", "api", "__init__.py"), [
    (
        "from .lmdeploy import LMDeployAPI, LMDeployWrapper",
        "from .lmdeploy import LMDeployAPI, LMDeployWrapper, GLMAnswerClean",
    ),
    (
        "'SiliconFlowAPI', 'LMDeployAPI', 'ARM_thinker', 'OpenAISDKWrapper', 'LMDeployWrapper',",
        "'SiliconFlowAPI', 'LMDeployAPI', 'ARM_thinker', 'OpenAISDKWrapper', 'LMDeployWrapper', 'GLMAnswerClean',",
    ),
])

# 10. config.py: GLM vllm 条目改用清理类
patch_file(cfg_path, [
    (
        '    "GLM4_1VThinking-9b-vllm": partial(\n        api.LMDeployAPI,',
        '    "GLM4_1VThinking-9b-vllm": partial(\n        api.GLMAnswerClean,',
    ),
])

print("PATCH_OK")
