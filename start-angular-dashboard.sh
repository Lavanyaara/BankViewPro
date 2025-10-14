#!/bin/bash

echo "Starting Credit Review Dashboard..."
echo ""

# Start backend in background
echo "🚀 Starting backend server on port 3000..."
cd backend
npm run dev > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🚀 Starting frontend application on port 4200..."
cd frontend  
npm start

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
