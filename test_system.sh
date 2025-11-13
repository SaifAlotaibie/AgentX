#!/bin/bash

echo "=================================="
echo "🎉 Qiwa AI Agent System - Test"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Testing Backend...${NC}"
BACKEND=$(curl -s http://localhost:8000/)
if [[ $BACKEND == *"Qiwa"* ]]; then
    echo -e "${GREEN}✓ Backend is running on http://localhost:8000${NC}"
else
    echo "✗ Backend is NOT running"
    exit 1
fi

echo ""
echo -e "${BLUE}2. Testing Frontend...${NC}"
FRONTEND=$(curl -s http://localhost:5173/ | grep -o "وكيل قوى")
if [[ $FRONTEND == "وكيل قوى" ]]; then
    echo -e "${GREEN}✓ Frontend is running on http://localhost:5173${NC}"
else
    echo "✗ Frontend is NOT running"
    exit 1
fi

echo ""
echo -e "${BLUE}3. Testing Resume API...${NC}"
RESUMES=$(curl -s http://localhost:8000/resumes/demo_user)
if [[ $RESUMES == *"success"* ]]; then
    echo -e "${GREEN}✓ Resume API is working${NC}"
    COUNT=$(echo $RESUMES | grep -o '"count":[0-9]*' | cut -d':' -f2)
    echo "  Found $COUNT resumes"
else
    echo "✗ Resume API failed"
fi

echo ""
echo -e "${BLUE}4. Testing Tickets API...${NC}"
TICKETS=$(curl -s http://localhost:8000/tickets/demo_user)
if [[ $TICKETS == *"success"* ]]; then
    echo -e "${GREEN}✓ Tickets API is working${NC}"
    COUNT=$(echo $TICKETS | grep -o '"count":[0-9]*' | cut -d':' -f2)
    echo "  Found $COUNT tickets"
else
    echo "✗ Tickets API failed"
fi

echo ""
echo "=================================="
echo "✅ System Status: READY"
echo "=================================="
echo ""
echo "📱 Open your browser at:"
echo "   http://localhost:5173"
echo ""
echo "💬 Try these commands:"
echo "   1. أريد إضافة سيرتي الذاتية"
echo "   2. ما هي شروط التوظيف؟"
echo ""
echo "🎯 Pages available:"
echo "   • Chat:      http://localhost:5173/"
echo "   • Dashboard: http://localhost:5173/dashboard"
echo "   • Tickets:   http://localhost:5173/tickets"
echo ""

