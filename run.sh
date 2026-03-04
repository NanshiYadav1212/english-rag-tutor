#!/bin/bash
# run.sh - Start both backend and frontend servers

echo "🚀 AI Language Tutor - Development Server Launcher"
echo "=================================================="

# Check if MongoDB is running
echo "✓ Checking MongoDB..."
if ! mongosh --eval "db.version()" > /dev/null 2>&1; then
    echo "❌ MongoDB is not running!"
    echo "   Start MongoDB with: mongod"
    exit 1
fi
echo "✓ MongoDB is running"

# Start backend
echo ""
echo "🔧 Starting Backend..."
echo "   Navigate to: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

cd backend || exit

# Check Python dependencies
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Seed quizzes if not already done
echo "📚 Checking quizzes..."
python -m app.scripts.seed_quizzes

# Start backend in background
uvicorn app.main:app --reload &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait a bit for backend to start
sleep 2

# Start frontend
echo ""
echo "⚛️  Starting Frontend..."
cd ../frontend || exit

if [ ! -d node_modules ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "   Navigate to: http://localhost:5173"
echo ""

npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait a bit for frontend to start
sleep 2

echo ""
echo "✓ Both servers are running!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user interrupt
wait $BACKEND_PID $FRONTEND_PID

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

echo ""
echo "Servers stopped. Goodbye! 👋"
