#!/bin/bash

echo "======================================"
echo "Credit Review Dashboard - Setup Script"
echo "======================================"
echo ""

# Install Backend Dependencies
echo "📦 Installing backend dependencies..."
cd backend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Backend installation failed"
    exit 1
fi
cd ..

echo "✅ Backend dependencies installed"
echo ""

# Install Frontend Dependencies  
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend installation failed"
    exit 1
fi
cd ..

echo "✅ Frontend dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cat > backend/.env << EOF
PORT=3000
OPENAI_API_KEY=\${OPENAI_API_KEY}
EOF
    echo "✅ Created backend/.env"
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To start the application:"
echo "1. Start backend:  cd backend && npm run dev"
echo "2. Start frontend: cd frontend && npm start"
echo ""
echo "Or run both with:"
echo "./start-angular-dashboard.sh"
echo ""
