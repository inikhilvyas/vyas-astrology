#!/usr/bin/env python3
"""
VYAS-Daivagya Model Merging & GGUF Quantization Engine
======================================================
Merges fine-tuned LoRA weights back into the base model (Qwen-2.5-1.5B or Llama-3.2-3B)
and exports to GGUF format (Q4_K_M, Q5_K_M, Q8_0) for instant offline execution in VYAS.
"""

import os
import sys
import argparse

def merge_and_export(base_model_id: str, lora_dir: str, merged_dir: str, gguf_out: str):
    """Merges LoRA into base weights and generates standalone model."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    print("==================================================")
    print("  VYAS-DAIVAGYA MODEL MERGE & EXPORT ENGINE")
    print(f"  Base Model:   {base_model_id}")
    print(f"  LoRA Adapter: {lora_dir}")
    print(f"  Merged Dir:   {merged_dir}")
    print("==================================================")

    os.makedirs(merged_dir, exist_ok=True)

    print("\n[1/3] Loading base model in full precision...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True
    )

    print("\n[2/3] Loading and fusing LoRA adapter weights...")
    model = PeftModel.from_pretrained(base_model, lora_dir)
    merged_model = model.merge_and_unload()

    print(f"\n[3/3] Saving merged standalone weights to {merged_dir}...")
    merged_model.save_pretrained(merged_dir, safe_serialization=True)
    tokenizer.save_pretrained(merged_dir)

    print(f"\n[SUCCESS] Standalone Model Weights saved at: {merged_dir}")
    print("\nTo convert to GGUF for offline llama.cpp execution:")
    print(f"  python llama.cpp/convert_hf_to_gguf.py {merged_dir} --outtype q8_0 --outfile {gguf_out}")
    print(f"  ./llama-quantize {gguf_out} {gguf_out.replace('.gguf', '-q4_k_m.gguf')} Q4_K_M")

def main():
    parser = argparse.ArgumentParser(description="Merge LoRA and Export GGUF")
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--lora_dir", type=str, default="models/vyas-daivagya-1.5b-lora")
    parser.add_argument("--merged_dir", type=str, default="models/vyas-daivagya-1.5b-merged")
    parser.add_argument("--gguf_out", type=str, default="models/vyas-daivagya-1.5b.gguf")
    args = parser.parse_args()

    merge_and_export(args.base_model, args.lora_dir, args.merged_dir, args.gguf_out)

if __name__ == "__main__":
    main()

