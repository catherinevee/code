#!/bin/bash
# helm-deploy.sh - Helm deployment script for Catherine College Housing

set -e

# Configuration
CHART_NAME="starrez-housing"
NAMESPACE_PREFIX="housing"
HELM_TIMEOUT="300s"
ENVIRONMENTS=("development" "staging" "production")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              StarRez Housing - Helm Deployment              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo -e "${YELLOW}Usage: $0 [COMMAND] [ENVIRONMENT] [OPTIONS]${NC}"
    echo ""
    echo "Commands:"
    echo "  install     Install the chart"
    echo "  upgrade     Upgrade the chart"
    echo "  uninstall   Uninstall the chart"
    echo "  status      Show deployment status"
    echo "  lint        Lint the chart"
    echo "  template    Generate templates"
    echo ""
    echo "Environments:"
    for env in "${ENVIRONMENTS[@]}"; do
        echo "  - $env"
    done
    echo ""
    echo "Options:"
    echo "  --dry-run       Show what would be deployed"
    echo "  --debug         Enable debug output"
    echo "  --wait          Wait for deployment to complete"
    echo "  --timeout       Timeout for operations (default: ${HELM_TIMEOUT})"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install development"
    echo "  $0 upgrade production --wait"
    echo "  $0 template staging --dry-run"
    echo "  $0 status production"
}

check_prerequisites() {
    echo -e "${BLUE}📋 Checking prerequisites...${NC}"
    
    local missing_tools=()
    
    if ! command -v helm &> /dev/null; then
        missing_tools+=("helm")
    fi
    
    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        echo -e "${RED}❌ Missing required tools: ${missing_tools[*]}${NC}"
        echo "Please install the missing tools and try again."
        exit 1
    fi
    
    # Check kubectl connection
    if ! kubectl cluster-info &> /dev/null; then
        echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
        echo "Please check your kubectl configuration."
        exit 1
    fi
    
    # Check if helm chart exists
    if [ ! -f "Chart.yaml" ]; then
        echo -e "${RED}❌ Chart.yaml not found in current directory${NC}"
        echo "Please run this script from the chart directory."
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
}

validate_environment() {
    local env=$1
    
    if [[ ! " ${ENVIRONMENTS[@]} " =~ " ${env} " ]]; then
        echo -e "${RED}❌ Invalid environment: ${env}${NC}"
        echo "Valid environments: ${ENVIRONMENTS[*]}"
        exit 1
    fi
}

get_namespace() {
    local env=$1
    
    case $env in
        "development")
            echo "${NAMESPACE_PREFIX}-dev"
            ;;
        "staging")
            echo "${NAMESPACE_PREFIX}-staging"
            ;;
        "production")
            echo "${NAMESPACE_PREFIX}"
            ;;
        *)
            echo "${NAMESPACE_PREFIX}-${env}"
            ;;
    esac
}

get_release_name() {
    local env=$1
    
    case $env in
        "development")
            echo "${CHART_NAME}-dev"
            ;;
        "staging")
            echo "${CHART_NAME}-staging"
            ;;
        "production")
            echo "${CHART_NAME}"
            ;;
        *)
            echo "${CHART_NAME}-${env}"
            ;;
    esac
}

create_namespace() {
    local namespace=$1
    
    if ! kubectl get namespace "$namespace" &> /dev/null; then
        echo -e "${BLUE}📦 Creating namespace: ${namespace}${NC}"
        kubectl create namespace "$namespace"
        kubectl label namespace "$namespace" name="$namespace" --overwrite
    fi
}

lint_chart() {
    echo -e "${BLUE}🔍 Linting Helm chart...${NC}"
    
    helm lint .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chart lint passed${NC}"
    else
        echo -e "${RED}❌ Chart lint failed${NC}"
        exit 1
    fi
}

install_chart() {
    local env=$1
    local dry_run=$2
    local debug=$3
    local wait_flag=$4
    local timeout=$5
    
    local namespace
    namespace=$(get_namespace "$env")
    local release_name
    release_name=$(get_release_name "$env")
    
    echo -e "${BLUE}🚀 Installing chart for ${env} environment...${NC}"
    echo "  Release: ${release_name}"
    echo "  Namespace: ${namespace}"
    
    # Create namespace if it doesn't exist
    if [[ "$dry_run" != "--dry-run" ]]; then
        create_namespace "$namespace"
    fi
    
    # Build helm command
    local helm_cmd="helm install ${release_name} . --namespace ${namespace}"
    
    # Add values file if it exists
    if [ -f "values-${env}.yaml" ]; then
        helm_cmd="${helm_cmd} --values values-${env}.yaml"
    fi
    
    # Add optional flags
    if [[ "$dry_run" == "--dry-run" ]]; then
        helm_cmd="${helm_cmd} --dry-run"
    fi
    
    if [[ "$debug" == "--debug" ]]; then
        helm_cmd="${helm_cmd} --debug"
    fi
    
    if [[ "$wait_flag" == "--wait" ]]; then
        helm_cmd="${helm_cmd} --wait --timeout ${timeout}"
    fi
    
    echo -e "${BLUE}Executing: ${helm_cmd}${NC}"
    eval "$helm_cmd"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chart installed successfully${NC}"
    else
        echo -e "${RED}❌ Chart installation failed${NC}"
        exit 1
    fi
}

upgrade_chart() {
    local env=$1
    local dry_run=$2
    local debug=$3
    local wait_flag=$4
    local timeout=$5
    
    local namespace
    namespace=$(get_namespace "$env")
    local release_name
    release_name=$(get_release_name "$env")
    
    echo -e "${BLUE}⬆️  Upgrading chart for ${env} environment...${NC}"
    echo "  Release: ${release_name}"
    echo "  Namespace: ${namespace}"
    
    # Build helm command
    local helm_cmd="helm upgrade ${release_name} . --namespace ${namespace}"
    
    # Add values file if it exists
    if [ -f "values-${env}.yaml" ]; then
        helm_cmd="${helm_cmd} --values values-${env}.yaml"
    fi
    
    # Add optional flags
    if [[ "$dry_run" == "--dry-run" ]]; then
        helm_cmd="${helm_cmd} --dry-run"
    fi
    
    if [[ "$debug" == "--debug" ]]; then
        helm_cmd="${helm_cmd} --debug"
    fi
    
    if [[ "$wait_flag" == "--wait" ]]; then
        helm_cmd="${helm_cmd} --wait --timeout ${timeout}"
    fi
    
    echo -e "${BLUE}Executing: ${helm_cmd}${NC}"
    eval "$helm_cmd"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chart upgraded successfully${NC}"
    else
        echo -e "${RED}❌ Chart upgrade failed${NC}"
        exit 1
    fi
}

uninstall_chart() {
    local env=$1
    local wait_flag=$2
    local timeout=$3
    
    local namespace
    namespace=$(get_namespace "$env")
    local release_name
    release_name=$(get_release_name "$env")
    
    echo -e "${YELLOW}🗑️  Uninstalling chart for ${env} environment...${NC}"
    echo "  Release: ${release_name}"
    echo "  Namespace: ${namespace}"
    
    read -p "$(echo -e ${RED})Are you sure you want to uninstall ${release_name}? (y/N): $(echo -e ${NC})" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}❌ Uninstall cancelled${NC}"
        exit 0
    fi
    
    # Build helm command
    local helm_cmd="helm uninstall ${release_name} --namespace ${namespace}"
    
    if [[ "$wait_flag" == "--wait" ]]; then
        helm_cmd="${helm_cmd} --wait --timeout ${timeout}"
    fi
    
    echo -e "${BLUE}Executing: ${helm_cmd}${NC}"
    eval "$helm_cmd"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chart uninstalled successfully${NC}"
        
        # Ask if user wants to delete namespace
        read -p "$(echo -e ${YELLOW})Delete namespace ${namespace}? (y/N): $(echo -e ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kubectl delete namespace "$namespace"
            echo -e "${GREEN}✅ Namespace deleted${NC}"
        fi
    else
        echo -e "${RED}❌ Chart uninstallation failed${NC}"
        exit 1
    fi
}

show_status() {
    local env=$1
    
    local namespace
    namespace=$(get_namespace "$env")
    local release_name
    release_name=$(get_release_name "$env")
    
    echo -e "${BLUE}📊 Status for ${env} environment:${NC}"
    echo "  Release: ${release_name}"
    echo "  Namespace: ${namespace}"
    echo ""
    
    # Check if release exists
    if ! helm list -n "$namespace" | grep -q "$release_name"; then
        echo -e "${YELLOW}⚠️  Release ${release_name} not found in namespace ${namespace}${NC}"
        return
    fi
    
    # Helm status
    echo -e "${YELLOW}Helm Status:${NC}"
    helm status "$release_name" -n "$namespace"
    
    echo ""
    echo -e "${YELLOW}Kubernetes Resources:${NC}"
    kubectl get all -n "$namespace" -l "app.kubernetes.io/instance=${release_name}"
    
    # Get access information
    local host
    case $env in
        "development")
            host="dev.catherine.it.com"
            ;;
        "staging")
            host="staging.catherine.it.com"
            ;;
        "production")
            host="catherine.it.com"
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}🌐 Access Information:${NC}"
    echo "URL: https://${host}"
    echo "Environment: ${env}"
}

generate_template() {
    local env=$1
    local dry_run=$2
    local debug=$3
    
    local namespace
    namespace=$(get_namespace "$env")
    local release_name
    release_name=$(get_release_name "$env")
    
    echo -e "${BLUE}📄 Generating templates for ${env} environment...${NC}"
    
    # Build helm command
    local helm_cmd="helm template ${release_name} . --namespace ${namespace}"
    
    # Add values file if it exists
    if [ -f "values-${env}.yaml" ]; then
        helm_cmd="${helm_cmd} --values values-${env}.yaml"
    fi
    
    if [[ "$debug" == "--debug" ]]; then
        helm_cmd="${helm_cmd} --debug"
    fi
    
    eval "$helm_cmd"
}

main() {
    print_banner
    
    # Parse arguments
    local command="$1"
    local environment="$2"
    shift 2 2>/dev/null || true
    
    local dry_run=""
    local debug=""
    local wait_flag=""
    local timeout="$HELM_TIMEOUT"
    
    # Parse additional options
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="--dry-run"
                shift
                ;;
            --debug)
                debug="--debug"
                shift
                ;;
            --wait)
                wait_flag="--wait"
                shift
                ;;
            --timeout)
                timeout="$2"
                shift 2
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                print_usage
                exit 1
                ;;
        esac
    done
    
    # Check if command and environment are provided
    if [[ -z "$command" || -z "$environment" ]]; then
        echo -e "${RED}❌ Command and environment are required${NC}"
        print_usage
        exit 1
    fi
    
    # Validate inputs
    validate_environment "$environment"
    check_prerequisites
    
    echo -e "${BLUE}📋 Deployment Configuration:${NC}"
    echo "  Command: $command"
    echo "  Environment: $environment"
    echo "  Namespace: $(get_namespace "$environment")"
    echo "  Release: $(get_release_name "$environment")"
    if [[ -n "$dry_run" ]]; then echo "  Dry Run: Yes"; fi
    if [[ -n "$debug" ]]; then echo "  Debug: Yes"; fi
    if [[ -n "$wait_flag" ]]; then echo "  Wait: Yes (timeout: $timeout)"; fi
    echo ""
    
    # Execute command
    case $command in
        "install")
            install_chart "$environment" "$dry_run" "$debug" "$wait_flag" "$timeout"
            if [[ -z "$dry_run" ]]; then
                show_status "$environment"
            fi
            ;;
        "upgrade")
            upgrade_chart "$environment" "$dry_run" "$debug" "$wait_flag" "$timeout"
            if [[ -z "$dry_run" ]]; then
                show_status "$environment"
            fi
            ;;
        "uninstall")
            uninstall_chart "$environment" "$wait_flag" "$timeout"
            ;;
        "status")
            show_status "$environment"
            ;;
        "lint")
            lint_chart
            ;;
        "template")
            generate_template "$environment" "$dry_run" "$debug"
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $command${NC}"
            print_usage
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}🎉 Operation completed successfully!${NC}"
}

# Check if sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi