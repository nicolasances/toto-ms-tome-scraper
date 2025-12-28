#!/bin/bash

# Start the FastAPI application with uvicorn
# For development, use --reload to auto-reload on code changes
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
