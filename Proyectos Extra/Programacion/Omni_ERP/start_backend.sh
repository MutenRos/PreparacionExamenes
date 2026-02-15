#!/bin/bash
cd /home/dario/src
source /home/dario/.venv/bin/activate
export PYTHONPATH=/home/dario/src
export OLLAMA_HOST=http://127.0.0.1:11434
export OLLAMA_MODEL=llama3
exec python -m uvicorn dario_app.api:app --host 0.0.0.0 --port 8001 --reload
