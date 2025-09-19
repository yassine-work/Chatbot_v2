import torch
from transformers import AutoModel, AutoTokenizer
import os
import onnx

# Define model and output paths
model_id = "sentence-transformers/all-MiniLM-L6-v2"
onnx_dir = "./onnx_model"
os.makedirs(onnx_dir, exist_ok=True)
onnx_model_path = os.path.join(onnx_dir, "model.onnx")

# Load model and tokenizer
model = AutoModel.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Set model to evaluation mode
model.eval()

# Create dummy input for ONNX export
dummy_input = tokenizer(
    "This is a dummy input for ONNX export",
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

# Convert inputs to torch tensors
input_ids = dummy_input["input_ids"]
attention_mask = dummy_input["attention_mask"]
token_type_ids = dummy_input.get("token_type_ids", None)

# Prepare inputs for export
inputs = (input_ids, attention_mask)
if token_type_ids is not None:
    inputs = (input_ids, attention_mask, token_type_ids)

# Export model to ONNX
torch.onnx.export(
    model,
    inputs,
    onnx_model_path,
    export_params=True,
    opset_version=14,  # Updated to support scaled_dot_product_attention
    do_constant_folding=True,
    input_names=["input_ids", "attention_mask", "token_type_ids"],
    output_names=["last_hidden_state"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "token_type_ids": {0: "batch_size", 1: "sequence_length"},
        "last_hidden_state": {0: "batch_size", 1: "sequence_length"}
    }
)

# Save tokenizer
tokenizer.save_pretrained(onnx_dir)

# Verify ONNX model
onnx_model = onnx.load(onnx_model_path)
onnx.checker.check_model(onnx_model)
print(f"ONNX model saved to {onnx_model_path} and verified successfully.")