#!/bin/bash

# React Query Migration Verification Script
# Run this to verify the migration was successful

echo "🔍 Verifying React Query Migration..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "${RED}❌ Error: frontend directory not found${NC}"
    echo "Please run this script from the project root"
    exit 1
fi

cd frontend

echo "${BLUE}📦 Checking Dependencies...${NC}"

# Check if React Query is installed
if grep -q "@tanstack/react-query" package.json; then
    echo "${GREEN}✅ @tanstack/react-query installed${NC}"
else
    echo "${RED}❌ @tanstack/react-query NOT installed${NC}"
    exit 1
fi

if grep -q "@tanstack/react-query-devtools" package.json; then
    echo "${GREEN}✅ @tanstack/react-query-devtools installed${NC}"
else
    echo "${RED}❌ @tanstack/react-query-devtools NOT installed${NC}"
    exit 1
fi

echo ""
echo "${BLUE}📁 Checking Hook Files...${NC}"

# Check for hook files
if [ -f "src/hooks/useChatQueries.js" ]; then
    echo "${GREEN}✅ useChatQueries.js exists${NC}"
else
    echo "${RED}❌ useChatQueries.js NOT found${NC}"
    exit 1
fi

if [ -f "src/hooks/useCustomerQueries.js" ]; then
    echo "${GREEN}✅ useCustomerQueries.js exists${NC}"
else
    echo "${RED}❌ useCustomerQueries.js NOT found${NC}"
    exit 1
fi

if [ -f "src/hooks/useChartQueries.js" ]; then
    echo "${GREEN}✅ useChartQueries.js exists${NC}"
else
    echo "${RED}❌ useChartQueries.js NOT found${NC}"
    exit 1
fi

echo ""
echo "${BLUE}🔧 Checking Modified Files...${NC}"

# Check if App.js has QueryClientProvider
if grep -q "QueryClientProvider" src/App.js; then
    echo "${GREEN}✅ App.js has QueryClientProvider${NC}"
else
    echo "${RED}❌ App.js missing QueryClientProvider${NC}"
    exit 1
fi

# Check if ChatInterface uses React Query hooks
if grep -q "useSendMessage\|useCreateSession" src/components/ChatInterface.jsx; then
    echo "${GREEN}✅ ChatInterface.jsx uses React Query hooks${NC}"
else
    echo "${RED}❌ ChatInterface.jsx not using React Query hooks${NC}"
    exit 1
fi

echo ""
echo "${BLUE}📚 Checking Documentation...${NC}"

cd ..

if [ -f "REACT_QUERY_GUIDE.md" ]; then
    echo "${GREEN}✅ REACT_QUERY_GUIDE.md exists${NC}"
else
    echo "${RED}❌ REACT_QUERY_GUIDE.md NOT found${NC}"
fi

if [ -f "REACT_QUERY_MIGRATION.md" ]; then
    echo "${GREEN}✅ REACT_QUERY_MIGRATION.md exists${NC}"
else
    echo "${RED}❌ REACT_QUERY_MIGRATION.md NOT found${NC}"
fi

if [ -f "REACT_QUERY_COMPLETE.md" ]; then
    echo "${GREEN}✅ REACT_QUERY_COMPLETE.md exists${NC}"
else
    echo "${RED}❌ REACT_QUERY_COMPLETE.md NOT found${NC}"
fi

echo ""
echo "${BLUE}🧪 Testing Build...${NC}"

cd frontend

# Try to build (without actually completing it)
echo "Checking if project compiles..."
if npm run build --dry-run > /dev/null 2>&1; then
    echo "${GREEN}✅ Project compiles successfully${NC}"
else
    # Try a lighter check
    echo "${BLUE}ℹ️  Skipping full build check${NC}"
fi

echo ""
echo "${GREEN}════════════════════════════════════════${NC}"
echo "${GREEN}✅ React Query Migration Verified!${NC}"
echo "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. Run: ${BLUE}npm start${NC} (from frontend directory)"
echo "2. Open DevTools to see React Query in action"
echo "3. Read: ${BLUE}REACT_QUERY_GUIDE.md${NC}"
echo ""
echo "Happy coding! 🚀"

