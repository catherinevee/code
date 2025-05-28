#!/bin/bash
# Test suite for Modern Webapp

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_TOTAL=0
BASE_URL="http://localhost:8080"

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    ((TESTS_TOTAL++))
    echo -n "Testing $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAIL${NC}"
    fi
}

# Wait for application to be ready
echo "Waiting for application to be ready..."
for i in {1..30}; do
    if curl -f -s "$BASE_URL/health" > /dev/null; then
        break
    fi
    sleep 1
done

echo "Running tests..."
echo ""

# Test suite
run_test "Main page loads" "curl -f -s '$BASE_URL/' > /dev/null"
run_test "Health endpoint responds" "curl -f -s '$BASE_URL/health' | grep -q 'healthy'"
run_test "404 page works" "[[ \$(curl -s -o /dev/null -w '%{http_code}' '$BASE_URL/nonexistent') == '404' ]]"
run_test "Gzip compression enabled" "curl -H 'Accept-Encoding: gzip' -I -s '$BASE_URL/' | grep -q 'Content-Encoding: gzip'"
run_test "Security headers present" "curl -I -s '$BASE_URL/' | grep -q 'X-Frame-Options'"
run_test "Response time acceptable" "[[ \$(curl -o /dev/null -s -w '%{time_total}' '$BASE_URL/') < 1.0 ]]"

echo ""
echo "Results: $TESTS_PASSED/$TESTS_TOTAL tests passed"

if [[ $TESTS_PASSED -eq $TESTS_TOTAL ]]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ❌${NC}"
    exit 1
fi
