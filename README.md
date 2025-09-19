Carbon Jar Chatbot
Overview
Carbon Jar is a chatbot application that provides intelligent responses based on a knowledge base. It features a React-based frontend for user interaction and a FastAPI backend for query processing. The system uses ONNX for sentence embeddings, ChromaDB for vector storage and retrieval, and Redis for caching. The knowledge base is sourced from carbonjar_knowledgebase.txt, which is chunked and embedded for efficient retrieval.
Features

Frontend: React-based UI (chatbot-ui-new) for user-friendly interaction.
Backend: FastAPI server (backend.py) for handling queries and responses.
Embedding Model: ONNX (onnxruntime) with a sentence transformer model for text embeddings.
Vector Database: ChromaDB (chromadb) for storing and querying document embeddings.
Knowledge Base: Processes carbonjar_knowledgebase.txt into chunks (load_documents.py).
Sanitization: Input sanitization (sanitizer.py) for safe query handling.
Caching: Redis (redis) for improved performance.
Model Conversion: Script (convert_to_onnx.py) for converting models to ONNX format (requires torch for conversion, not needed in runtime).

Prerequisites

Python 3.8+
Node.js 18+ (for React frontend)
Docker (optional, for containerized deployment)
Redis server
Required Python packages (listed in requirements.txt)

Note: The convert_to_onnx.py script requires torch for model conversion, but torch is not included in requirements.txt as the Docker image uses the pre-converted ONNX model.
Installation
1. Extract the Project
Unzip the provided carbon_jar_project.zip:
unzip carbon_jar_project.zip
cd chatbot

2. Set Up the Python Environment
Create and activate a virtual environment:
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

Install Python dependencies:
pip install -r requirements.txt

3. Set Up Environment Variables
Create a .env file in the project root with the following:
CHROMA_PATH=./chroma_data
# Add Redis host, port, or other configurations as needed

4. Set Up the Knowledge Base
Ensure carbonjar_knowledgebase.txt is in the project root. The knowledge base will be processed into chunks and stored in ChromaDB during initialization.
5. Initialize the Vector Database
Run the script to load and embed the knowledge base:
python load_documents.py

This creates a ChromaDB collection in ./chroma_data using the ONNX model for embeddings.
6. Set Up the React Frontend
Navigate to the chatbot-ui-new directory and install Node.js dependencies:
cd chatbot-ui-new
npm install

7. Run the Application
Start the Redis server (if not already running):
redis-server

Start the FastAPI backend:
uvicorn backend:app --host 0.0.0.0 --port 8000

Start the React frontend:
cd chatbot-ui-new
npm start

The frontend will be available at http://localhost:3000, and the backend API at http://localhost:8000.
8. (Optional) Docker Deployment
Build and run the application using Docker Compose:
docker-compose up --build

Note: The Docker image includes the pre-converted ONNX model, so torch is not required in the runtime environment.
Usage

Open the React frontend in a browser (http://localhost:3000).
Enter a query in the chatbot interface.
The backend processes the query using the ONNX model, retrieves relevant documents from ChromaDB, and returns a response.
Responses are cached in Redis for faster subsequent queries.

Preparing the Project for Distribution
To prepare the project for sharing or deployment:

Remove unnecessary directories to reduce size:rm -rf env __pycache__ chatbot-ui-new/node_modules chatbot-ui-new/.tsbuildinfo


env/: Virtual environment (recreate during installation).
__pycache__: Python cache files (automatically regenerated).
chatbot-ui-new/node_modules/: Node.js dependencies (reinstalled via npm install).
chatbot-ui-new/*.tsbuildinfo: TypeScript build artifacts (regenerated during build).
Optionally, exclude chroma_data/ if the vector database should be rebuilt on setup.


Verify the remaining files match the structure below.
Zip the project:zip -r carbon_jar_project.zip chatbot



Project Structure
chatbot/
├── backend.py              # FastAPI backend server
├── chatbot.py              # Chatbot logic
├── chatbot-ui-new/         # React frontend
│   ├── components.json     # Component configurations
│   ├── eslint.config.js    # ESLint configuration
│   ├── index.html          # HTML entry point
│   ├── package.json        # Node.js dependencies
│   ├── package-lock.json   # Dependency lock file
│   ├── postcss.config.js   # PostCSS configuration
│   ├── src/               # React source code
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   ├── tsconfig.json       # TypeScript configuration
│   ├── tsconfig.app.json   # TypeScript app configuration
│   ├── tsconfig.node.json  # TypeScript node configuration
│   ├── vite.config.ts      # Vite configuration
├── config.py               # Configuration settings
├── convert_to_onnx.py      # Script to convert model to ONNX format (requires torch)
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration for backend
├── load_documents.py       # Script to process and embed knowledge base
├── onnx_model/             # ONNX model and tokenizer
├── requirements.txt        # Python runtime dependencies
├── retriever.py            # ONNX-based retrieval logic
├── sanitizer.py            # Input sanitization
├── static/                 # Static files for FastAPI
├── carbonjar_knowledgebase.txt  # Knowledge base text file
├── chroma_data/            # ChromaDB storage (optional, rebuild with load_documents.py)

Dependencies

Python: fastapi, uvicorn, requests, chromadb, onnxruntime, transformers, python-dotenv, redis, numpy
Node.js: Managed via chatbot-ui-new/package.json. Key dependencies include:
react, react-dom: React framework
vite: Build tool
tailwindcss, postcss, autoprefixer: Styling
typescript, eslint: Type checking and linting
Install with npm install in chatbot-ui-new/.


Conversion Script: torch (required only for convert_to_onnx.py, not included in requirements.txt)

Notes

Ensure the ONNX model (onnx_model/model.onnx) and tokenizer are in the onnx_model/ directory.
The carbonjar_knowledgebase.txt file should be formatted with ## headers for proper chunking.
For production, configure Redis with secure settings and consider a reverse proxy (e.g., Nginx) for the FastAPI server.
The ONNX model is pre-converted, so torch is not needed unless re-running convert_to_onnx.py.

Troubleshooting

ChromaDB errors: Verify CHROMA_PATH exists and is writable.
ONNX model issues: Ensure model and tokenizer paths are correct in retriever.py and load_documents.py.
Redis connection errors: Confirm the Redis server is running and accessible.
Frontend issues: Check the React app's connection to the backend API (http://localhost:8000).
Model conversion: If re-running convert_to_onnx.py, install torch separately (pip install torch).

License
This project is licensed under the MIT License.