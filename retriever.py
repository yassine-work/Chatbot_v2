import numpy as np
from onnxruntime import InferenceSession
from transformers import AutoTokenizer
from load_documents import VECTOR_DB

class ONNXRetriever:
    def __init__(self, model_path="./onnx_model/model.onnx", tokenizer_path="./onnx_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.session = InferenceSession(model_path, providers=["CPUExecutionProvider"])
    
    def encode(self, texts):
        # Tokenize input texts
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="np"
        )
        
        # Prepare inputs for ONNX model
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
            "token_type_ids": inputs.get("token_type_ids", np.zeros_like(inputs["input_ids"])).astype(np.int64)
        }
        
        # Run inference
        outputs = self.session.run(None, ort_inputs)
        embeddings = outputs[0]  # First output is last_hidden_state
        
        # Mean pooling to get sentence embeddings
        attention_mask = inputs["attention_mask"]
        embeddings = np.sum(embeddings * attention_mask[:, :, None], axis=1) / np.sum(attention_mask, axis=1)[:, None]
        return embeddings

def retrieve_relevant_docs(query, top_k=2):
    if VECTOR_DB is None:
        print("Error: VECTOR_DB not initialized.")
        return []
    try:
        model = ONNXRetriever()
        query_emb = model.encode([query])[0].tolist()
        print(f"Query: {query}, Embedding shape: {len(query_emb)}")
        results = VECTOR_DB.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        print(f"Retrieval results: {results}")
        return results['documents'][0] if results['documents'] else []
    except Exception as e:
        print(f"Error in retrieve_relevant_docs: {e}")
        return []