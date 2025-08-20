#!/bin/bash

echo "Starting Flask app with auto-restart..."

while true; do
    echo "$(date): Starting app..."
    python3 app.py
    echo "$(date): App exited. Restarting in 1 second..."
    sleep 1
done