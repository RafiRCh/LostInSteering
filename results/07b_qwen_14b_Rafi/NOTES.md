# Qwen2.5-14B Full Scale Audit: Run 07b Notes

**Run:** 2026-11-16 on Kaggle (Nvidia Tesla T4, 15GB VRAM), notebook `notebooks/07b_qwen_14b_Rafi.ipynb`, kernel `rafirahmanchowdhury/lostinsteering-7b`.
**Start Time:** ~13:06 UTC (7:06 PM local).
**Execution Time:** ~5.7 minutes.
**Status:** **Failed (CUDA Out of Memory)**.

---

## 1. Overview & Objective

Run 07b was designed as the upper-scale anchor for the Qwen2.5 scaling audit:
* Target Model: `Qwen/Qwen2.5-14B-Instruct`
* Fallback Model: `Qwen/Qwen2.5-7B-Instruct`
* Goal: Determine whether sycophancy steering representations and cross-lingual transfer (specifically Hindi→Bengali sibling transfer and factual honesty preservation) strengthen or saturate at the 14B parameter scale.

---

## 2. Failure Analysis

### Primary Failure: Qwen2.5-14B-Instruct OOM
* The 14B model in `bfloat16`/`float16` precision requires approximately **28 GiB of VRAM** for weights alone, plus activation memory during the forward passes.
* The Kaggle environment allocated a single **Nvidia Tesla T4 (14.56 GiB total capacity)**.
* PyTorch threw `torch.OutOfMemoryError` while attempting to load the weights:
  ```
  torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB.
  GPU 0 has a total capacity of 14.56 GiB of which 758.81 MiB is free.
  Process has 13.82 GiB memory in use (13.68 GiB allocated by PyTorch).
  ```

### Secondary Failure: Fallback to 7B also OOM'd
* The script caught the exception and attempted to fall back to `Qwen/Qwen2.5-7B-Instruct`:
  ```
  OOM on Qwen/Qwen2.5-14B-Instruct! Falling back to Qwen/Qwen2.5-7B-Instruct
  ```
* However, because the 14B tensors were not fully dereferenced and garbage collected before the fallback allocation, PyTorch's CUDA memory allocator suffered severe fragmentation:
  ```
  Fallback also failed: CUDA out of memory. Tried to allocate 5.63 GiB.
  GPU 0 has a total capacity of 14.56 GiB of which 758.81 MiB is free.
  Process has 13.82 GiB memory in use.
  ```

---

### Correction to the diagnosis above
`kaggle_run.log` shows two T4s were present (GPU 0 and GPU 1, 15.6 GB each). The real cause: fp16 14B is about 29.5 GB, which does not fit in 2 x ~14.5 GB usable, so `accelerate` logged "Some parameters are on the meta device because they were offloaded to the disk" and then failed pulling a 1.45 GiB tensor (the lm_head) back onto GPU 0 during the first probe forward pass. The 7B fallback then failed because the 14B weights were still resident. Fix applied in the notebook: 4-bit NF4 load, assertion that nothing is offloaded, no fallback model, batched probe, resumable stages.

## 3. Quota Impact & Next Steps

1. **Quota Impact:**
   * Because the kernel crashed within 5.7 minutes, it consumed negligible GPU quota (~0.1 GPU hours) and has been completely stopped.
2. **Path to Run 14B:**
   * **Option A (Quantization):** Load `Qwen/Qwen2.5-14B-Instruct` in 4-bit (`load_in_4bit=True` via `bitsandbytes` NF4). This drops the VRAM requirement to ~9–10 GiB, fitting comfortably within a single T4.
   * **Option B (Multi-GPU):** Select Kaggle's **2× T4** accelerator option with `device_map="auto"` (providing ~29.1 GiB combined VRAM).
   * **Option C (A100 / High-VRAM instance):** Run on Colab Pro, Vast.ai, or RunPod on an A100 (40GB/80GB) or RTX 4090 (24GB with 8-bit).
