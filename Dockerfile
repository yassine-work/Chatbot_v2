# Stage 1: Builder
FROM python:3.10-slim AS builder
WORKDIR /app
# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libatlas-base-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
# Install dependencies (no PyTorch)
RUN pip install --no-cache-dir -r requirements.txt -t /app/install

# Stage 2: Runtime
FROM python:3.10-slim
WORKDIR /app
# Install runtime dependencies for chromadb, uvicorn, and onnxruntime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    libgomp1 \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uvicorn
# Copy installed Python packages
COPY --from=builder /app/install /usr/local/lib/python3.10/site-packages
# Copy necessary app files
COPY backend.py chatbot.py config.py load_documents.py retriever.py sanitizer.py carbonjar_knowledgebase.txt ./
# Create and copy static and onnx_model directories
RUN mkdir -p /app/static /app/onnx_model
COPY static /app/static
COPY onnx_model /app/onnx_model
# Create chroma_data directory for runtime persistence
RUN mkdir -p /app/chroma_data && chmod -R 777 /app/chroma_data
EXPOSE 8000
# Run as non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]