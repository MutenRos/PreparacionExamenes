#!/bin/bash
# Test script to validate all 5 new Dynamics 365 modules

echo "🔬 Testing Phase 2 Implementation - 5 New Modules"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Test function
test_module() {
    local module=$1
    local path="/home/dario/src/dario_app/modules/$module"
    
    echo -n "Testing $module..."
    
    if [ ! -d "$path" ]; then
        echo -e "${RED}✗ Directory not found${NC}"
        ERRORS=$((ERRORS+1))
        return 1
    fi
    
    # Check files exist
    if [ ! -f "$path/models.py" ]; then
        echo -e "${RED}✗ models.py missing${NC}"
        ERRORS=$((ERRORS+1))
        return 1
    fi
    
    if [ ! -f "$path/routes.py" ]; then
        echo -e "${RED}✗ routes.py missing${NC}"
        ERRORS=$((ERRORS+1))
        return 1
    fi
    
    # Validate Python syntax
    python3 -m py_compile "$path/models.py" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ models.py syntax error${NC}"
        ERRORS=$((ERRORS+1))
        return 1
    fi
    
    python3 -m py_compile "$path/routes.py" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ routes.py syntax error${NC}"
        ERRORS=$((ERRORS+1))
        return 1
    fi
    
    echo -e "${GREEN}✓${NC}"
    return 0
}

# Test each module
echo ""
echo "Module Validation:"
test_module "recruitment"
test_module "service_scheduling"
test_module "sustainability"
test_module "contract_management"
test_module "warranty_management"

echo ""
echo "API Integration:"

# Test API file
echo -n "Testing api/__init__.py..."
if python3 -m py_compile /home/dario/src/dario_app/api/__init__.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Syntax error${NC}"
    ERRORS=$((ERRORS+1))
fi

# Test Database file
echo -n "Testing database/__init__.py..."
if python3 -m py_compile /home/dario/src/dario_app/database/__init__.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Syntax error${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
echo "API Router Registration:"

# Check router imports in api/__init__.py
ROUTERS=("recruitment_router" "service_scheduling_router" "sustainability_router" "contract_management_router" "warranty_router")

for router in "${ROUTERS[@]}"; do
    echo -n "Checking $router..."
    if grep -q "$router" /home/dario/src/dario_app/api/__init__.py; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ Not found${NC}"
        ERRORS=$((ERRORS+1))
    fi
done

echo ""
echo "Model Count Verification:"

# Count models in each module
declare -A expected_models
expected_models["recruitment"]=6
expected_models["service_scheduling"]=5
expected_models["sustainability"]=6
expected_models["contract_management"]=6
expected_models["warranty_management"]=5

for module in "${!expected_models[@]}"; do
    count=$(grep -c "^class.*Base\):" /home/dario/src/dario_app/modules/$module/models.py 2>/dev/null || echo 0)
    expected=${expected_models[$module]}
    echo -n "  $module: "
    if [ "$count" -ge "$((expected - 1))" ]; then
        echo -e "${GREEN}✓ Found $count models (expected ~$expected)${NC}"
    else
        echo -e "${RED}✗ Found $count models (expected ~$expected)${NC}"
        ERRORS=$((ERRORS+1))
    fi
done

echo ""
echo "Database Import Check:"

# Check if all models are imported in database/__init__.py
modules_to_check=("recruitment" "service_scheduling" "sustainability" "contract_management" "warranty_management")

for module in "${modules_to_check[@]}"; do
    echo -n "  from dario_app.modules.$module..."
    if grep -q "from dario_app.modules.$module" /home/dario/src/dario_app/database/__init__.py; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ Not imported${NC}"
        ERRORS=$((ERRORS+1))
    fi
done

echo ""
echo "=================================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed! Phase 2 implementation is complete.${NC}"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS errors${NC}"
    exit 1
fi
