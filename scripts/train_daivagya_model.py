#!/usr/bin/env python3
"""
VYAS-Daivagya Foundation Model Fine-Tuning Pipeline
===================================================
Fine-tunes a compact, ultra-fast language model (Qwen-2.5-1.5B-Instruct or Llama-3.2-3B-Instruct)
on the VYAS-Daivagya SFT Dataset using QLoRA (4-bit Parameter-Efficient Fine-Tuning).

Can run on:
- Free Google Colab T4 GPU (takes ~45-60 mins).
- Single consumer GPU (RTX 3060 / 4060 / 4090 / A100).
- RunPod / Lambda Labs ($0.20 - $0.50 total compute cost).

Outputs:
- Merged HuggingFace Model Weights.
- Quantized GGUF Model (Q4_K_M ~ 1.1 GB) for offline on-device deployment in VYAS.
"""

import os
import sys
import argparse
from typing import Dict, Any

def check_dependencies():
    """Verifies that PyTorch and essential fine-tuning packages are present."""
    try:
        import torch
        print(f"[INFO] PyTorch version: {torch.__version__}")
        print(f"[INFO] CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"[INFO] Active GPU: {torch.cuda.get_device_name(0)}")
            print(f"[INFO] Total VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
    except ImportError:
        print("[ERROR] PyTorch not installed. Please install torch with CUDA support.")
        sys.exit(1)

def train_daivagya(model_id: str = "Qwen/Qwen2.5-1.5B-Instruct",
                   train_file: str = "data/daivagya_sft/vyas_daivagya_sft_train.jsonl",
                   val_file: str = "data/daivagya_sft/vyas_daivagya_sft_val.jsonl",
                   output_dir: str = "models/vyas-daivagya-1.5b-lora",
                   batch_size: int = 4,
                   grad_accum: int = 4,
                   epochs: int = 3,
                   learning_rate: float = 2e-4):
    """
    Executes 4-bit QLoRA fine-tuning using HuggingFace TRL and PEFT.
    """
    import torch
    from datasets import load_dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer

    print("\n==================================================")
    print("  VYAS-DAIVAGYA FOUNDATION MODEL TRAINING PIPELINE")
    print(f"  Base Model:       {model_id}")
    print(f"  Training File:    {train_file}")
    print(f"  Output Directory: {output_dir}")
    print("==================================================\n")

    if not os.path.exists(train_file):
        raise FileNotFoundError(f"Training dataset not found: {train_file}. Run scripts/build_daivagya_sft_dataset.py first!")

    # 1. 4-Bit NormalFloat Quantization Config (QLoRA)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 2. Load Base Tokenizer & Model
    print(f"[1/5] Loading tokenizer and 4-bit quantized base model: {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    model = prepare_model_for_kbit_training(model)

    # 3. Configure Parameter-Efficient LoRA Adapters
    print("[2/5] Configuring LoRA rank-16 adapter matrix across attention heads...")
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 4. Load Dataset
    print(f"[3/5] Loading training dataset from {train_file}...")
    dataset = load_dataset("json", data_files={"train": train_file, "val": val_file})

    def formatting_prompts_func(example):
        """Formats ChatML messages into raw training text."""
        output_texts = []
        for msgs in example['messages']:
            text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
            output_texts.append(text)
        return output_texts

    # 5. Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        num_train_epochs=epochs,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="paged_adamw_8bit",
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["val"],
        peft_config=peft_config,
        dataset_text_field="messages",
        max_seq_length=2048,
        tokenizer=tokenizer,
        args=training_args,
        formatting_func=formatting_prompts_func
    )

    print("\n[4/5] Initiating Fine-Tuning Execution...")
    trainer.train()

    print(f"\n[5/5] Saving fine-tuned LoRA weights to {output_dir}...")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print("\n[SUCCESS] Vyas-Daivagya Fine-Tuning Completed Successfully!")
    print(f"Weights saved at: {output_dir}")
    print("\nNext step: Merge LoRA and export to GGUF using:")
    print(f"python scripts/export_daivagya_gguf.py --base_model {model_id} --lora_dir {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="VYAS-Daivagya Foundation Training")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-1.5B-Instruct", help="Base model HuggingFace ID")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size per device")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    args = parser.parse_args()

    check_dependencies()
    train_daivagya(model_id=args.model, batch_size=args.batch_size, epochs=args.epochs)

if __name__ == "__main__":
    main()

