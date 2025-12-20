#!/bin/bash
#
# Tests for setup_tuning_project.sh
# Run with: bash tests/test_setup_project.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SETUP_SCRIPT="$PROJECT_ROOT/scripts/setup_tuning_project.sh"
TEST_DIR=$(mktemp -d)
TEST_PROJECT="$TEST_DIR/test-project"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Running setup_tuning_project.sh Tests"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Test 1: Script requires project directory argument
echo "Test 1: Script requires project directory argument"
if $SETUP_SCRIPT 2>&1 | grep -q "Usage:"; then
    pass "Shows usage when no argument provided"
else
    fail "Should show usage when no argument provided"
fi

# Test 2: Creates directory structure (non-interactive mode via input)
echo ""
echo "Test 2: Creates directory structure"

# Simulate interactive input
{
    echo "2017"      # Year
    echo "WRX"       # Model
    echo "stock"     # Turbo
    echo "stock"     # Intercooler
    echo "stock"     # Downpipe
    echo "stock"     # Intake
    echo "stock"     # EBCS
    echo "N"         # Flex Fuel
    echo "N"         # AOS
    echo "stock"     # Injectors
    echo "stock"     # Fuel pump
    echo "93"        # Fuel grade
    echo "18"        # Target boost
    echo "6500"      # Redline
    echo "street"    # Use case
    echo "moderate"  # Climate
    echo "low"       # Altitude
} | $SETUP_SCRIPT "$TEST_PROJECT" > /dev/null 2>&1

if [ -d "$TEST_PROJECT/datalogs" ]; then
    pass "Creates datalogs directory"
else
    fail "Should create datalogs directory"
fi

if [ -d "$TEST_PROJECT/output" ]; then
    pass "Creates output directory"
else
    fail "Should create output directory"
fi

if [ -d "$TEST_PROJECT/tables/original" ]; then
    pass "Creates tables/original directory"
else
    fail "Should create tables/original directory"
fi

if [ -d "$TEST_PROJECT/tables/revised" ]; then
    pass "Creates tables/revised directory"
else
    fail "Should create tables/revised directory"
fi

# Test 3: Creates vehicle_config.yaml
echo ""
echo "Test 3: Creates vehicle_config.yaml"
if [ -f "$TEST_PROJECT/vehicle_config.yaml" ]; then
    pass "Creates vehicle_config.yaml"
else
    fail "Should create vehicle_config.yaml"
fi

# Test 4: Config contains vehicle info
echo ""
echo "Test 4: Config contains correct vehicle info"
if grep -q "year: 2017" "$TEST_PROJECT/vehicle_config.yaml"; then
    pass "Config contains vehicle year"
else
    fail "Config should contain vehicle year"
fi

if grep -q "model: WRX" "$TEST_PROJECT/vehicle_config.yaml"; then
    pass "Config contains vehicle model"
else
    fail "Config should contain vehicle model"
fi

# Test 5: Config contains safety margins
echo ""
echo "Test 5: Config contains safety margins"
if grep -q "timing_margin_degrees:" "$TEST_PROJECT/vehicle_config.yaml"; then
    pass "Config contains timing margin"
else
    fail "Config should contain timing margin"
fi

if grep -q "wot_afr_target:" "$TEST_PROJECT/vehicle_config.yaml"; then
    pass "Config contains WOT AFR target"
else
    fail "Config should contain WOT AFR target"
fi

if grep -q "dam_minimum:" "$TEST_PROJECT/vehicle_config.yaml"; then
    pass "Config contains DAM minimum"
else
    fail "Config should contain DAM minimum"
fi

# Test 6: Creates README.md
echo ""
echo "Test 6: Creates project README"
if [ -f "$TEST_PROJECT/README.md" ]; then
    pass "Creates README.md"
else
    fail "Should create README.md"
fi

if grep -q "Mod List" "$TEST_PROJECT/README.md"; then
    pass "README contains mod list section"
else
    fail "README should contain mod list section"
fi

# Test 7: Creates .gitignore
echo ""
echo "Test 7: Creates .gitignore"
if [ -f "$TEST_PROJECT/.gitignore" ]; then
    pass "Creates .gitignore"
else
    fail "Should create .gitignore"
fi

# Test 8: Safety margin calculation - high risk config
echo ""
echo "Test 8: Safety margin adjusts for risk factors"
TEST_PROJECT_RISKY="$TEST_DIR/risky-project"

{
    echo "2017"      # Year
    echo "WRX"       # Model
    echo "upgraded"  # Turbo (adds risk)
    echo "stock"     # Intercooler (stock with mods = risk)
    echo "catless"   # Downpipe
    echo "aftermarket"  # Intake
    echo "stock"     # EBCS (stock = risk)
    echo "N"         # Flex Fuel
    echo "N"         # AOS
    echo "stock"     # Injectors
    echo "stock"     # Fuel pump
    echo "91"        # Fuel grade (low octane = risk)
    echo "22"        # Target boost (high)
    echo "6500"      # Redline
    echo "track"     # Use case (track = risk)
    echo "hot"       # Climate (hot = risk)
    echo "high"      # Altitude (high = risk)
} | $SETUP_SCRIPT "$TEST_PROJECT_RISKY" > /dev/null 2>&1

# Check that timing margin increased (should be higher than base 2)
TIMING_MARGIN=$(grep "timing_margin_degrees:" "$TEST_PROJECT_RISKY/vehicle_config.yaml" | awk '{print $2}')
if [ "$TIMING_MARGIN" -gt 2 ]; then
    pass "Timing margin increased for risky config ($TIMING_MARGIN°)"
else
    fail "Timing margin should be > 2 for risky config, got $TIMING_MARGIN"
fi

# Check boost margin for stock EBCS + high altitude
BOOST_MARGIN=$(grep "boost_margin_psi:" "$TEST_PROJECT_RISKY/vehicle_config.yaml" | awk '{print $2}')
if [ "$BOOST_MARGIN" -gt 0 ]; then
    pass "Boost margin set for stock EBCS + high altitude ($BOOST_MARGIN psi)"
else
    fail "Boost margin should be > 0 for stock EBCS + high altitude"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Test Summary"
echo "════════════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Passed${NC}: $TESTS_PASSED"
echo -e "  ${RED}Failed${NC}: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
fi
