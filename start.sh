#!/bin/bash
set -e
echo "Starting Decentralized Identity Management System..."
uvicorn app:app --host 0.0.0.0 --port 9131 --workers 1
