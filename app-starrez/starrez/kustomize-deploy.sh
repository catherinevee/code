#!/bin/bash
# kustomize-deploy.sh - Deployment script using Kustomize

set -e

# Configuration
ENVIRONMENTS=("development" "staging" "production")
DEFAULT_ENV="development"
REGISTRY="catherinevee"
IMAGE_NAME="catherinevee"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              StarRez Housing - Kustomize Deploy             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo -e "${YELLOW}Usage: $0 [ENVIRONMENT] [IMAGE_TAG]${NC}"
    echo ""
    echo "Environments:"
    for env in "${ENVIRONMENTS[@]}"; do
        echo "  - $env"
    done
    echo ""
    echo "Examples:"
    echo "  $0 development latest"
    echo "  $0 staging v1.2.0"
    echo "  $0 production v1.0.0"
    echo ""
    echo "Options:"
    echo "  --dry-run    Show what would be deployed without applying"
    echo "  --diff       Show differences with current deployment"
    echo "  --help       Show this help message"
}

check_prerequisites() {
    echo -e "${BLUE}📋 Checking prerequisites...${NC}"
    
    local missing_tools=()
    
    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi
    
    if ! command -v kustomize &> /dev/null; then
        missing_tools+=("kustomize")
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

build_manifests() {
    local env=$1
    local tag=$2
    local dry_run=$3
    
    echo -e "${BLUE}🔨 Building manifests for ${env} environment...${NC}"
    
    # Create temporary kustomization with updated image tag
    local temp_dir="/tmp/kustomize-housing-${env}-$$"
    mkdir -p "$temp_dir"
    
    # Copy overlay files
    cp -r "overlays/${env}" "$temp_dir/"
    
    # Update image tag in the temporary kustomization
    cd "$temp_dir/${env}"
    
    # Use kustomize edit to set image
    kustomize edit set image housing-frontend="${REGISTRY}/${IMAGE_NAME}:${tag}"
    
    # Build and output manifests
    echo -e "${BLUE}📋 Generated manifests:${NC}"
    echo "---"
    
    if [[ "$dry_run" == "true" ]]; then
        kustomize build .
    else
        kustomize build . > "${temp_dir}/manifests.yaml"
        cat "${temp_dir}/manifests.yaml"
    fi
    
    echo "---"
    echo -e "${GREEN}✅ Manifests built successfully${NC}"
    
    # Return path to manifests
    echo "${temp_dir}/manifests.yaml"
}

show_diff() {
    local env=$1
    local tag=$2
    
    echo -e "${BLUE}🔍 Showing differences for ${env} environment...${NC}"
    
    # Build current manifests
    local manifests_file
    manifests_file=$(build_manifests "$env" "$tag" "false")
    
    # Get current resources
    local namespace
    case $env in
        "development")
            namespace="housing-department-dev"
            ;;
        "staging")
            namespace="housing-department-staging"
            ;;
        "production")
            namespace="housing-department"
            ;;
    esac
    
    # Show diff if namespace exists
    if kubectl get namespace "$namespace" &> /dev/null; then
        echo -e "${YELLOW}Differences:${NC}"
        kubectl diff -f "$manifests_file" || true
    else
        echo -e "${YELLOW}Namespace ${namespace} doesn't exist - this will be a new deployment${NC}"
    fi
    
    # Cleanup
    rm -rf "$(dirname "$manifests_file")"
}

deploy_manifests() {
    local env=$1
    local tag=$2
    local dry_run=$3
    
    echo -e "${BLUE}🚀 Deploying to ${env} environment...${NC}"
    
    # Build manifests
    local manifests_file
    manifests_file=$(build_manifests "$env" "$tag" "$dry_run")
    
    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}🔍 Dry run completed - no changes applied${NC}"
        return
    fi
    
    # Apply manifests
    echo -e "${BLUE}📦 Applying manifests...${NC}"
    kubectl apply -f "$manifests_file"
    
    # Get namespace for this environment
    local namespace
    case $env in
        "development")
            namespace="housing-department-dev"
            ;;
        "staging")
            namespace="housing-department-staging"
            ;;
        "production")
            namespace="housing-department"
            ;;
    esac
    
    # Wait for deployment
    echo -e "${BLUE}⏳ Waiting for deployment to be ready...${NC}"
    
    local deployment_name
    case $env in
        "development")
            deployment_name="dev-housing-frontend-dev"
            ;;
        "staging")
            deployment_name="staging-housing-frontend-staging"
            ;;
        "production")
            deployment_name="housing-frontend"
            ;;
    esac
    
    if kubectl get deployment "$deployment_name" -n "$namespace" &> /dev/null; then
        kubectl wait --for=condition=available --timeout=300s deployment/"$deployment_name" -n "$namespace"
        kubectl rollout status deployment/"$deployment_name" -n "$namespace"
    fi
    
    echo -e "${GREEN}✅ Deployment completed successfully${NC}"
    
    # Cleanup temporary files
    rm -rf "$(dirname "$manifests_file")"
}

show_status() {
    local env=$1
    
    echo -e "${BLUE}📊 Deployment Status for ${env} environment:${NC}"
    
    local namespace
    case $env in
        "development")
            namespace="housing-department-dev"
            ;;
        "staging")
            namespace="housing-department-staging"
            ;;
        "production")
            namespace="housing-department"
            ;;
    esac
    
    if ! kubectl get namespace "$namespace" &> /dev/null; then
        echo -e "${YELLOW}⚠️  Namespace ${namespace} doesn't exist${NC}"
        return
    fi
    
    echo ""
    echo -e "${YELLOW}Pods:${NC}"
    kubectl get pods -n "$namespace" -o wide
    
    echo ""
    echo -e "${YELLOW}Services:${NC}"
    kubectl get services -n "$namespace"
    
    echo ""
    echo -e "${YELLOW}Ingress:${NC}"
    kubectl get ingress -n "$namespace"
    
    echo ""
    echo -e "${YELLOW}HPA:${NC}"
    kubectl get hpa -n "$namespace"
    
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

main() {
    print_banner
    
    # Parse arguments
    local environment="$DEFAULT_ENV"
    local image_tag="latest"
    local dry_run="false"
    local show_diff_only="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run="true"
                shift
                ;;
            --diff)
                show_diff_only="true"
                shift
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            -*)
                echo -e "${RED}Unknown option: $1${NC}"
                print_usage
                exit 1
                ;;
            *)
                if [[ -z "$environment" || "$environment" == "$DEFAULT_ENV" ]]; then
                    environment="$1"
                elif [[ "$image_tag" == "latest" ]]; then
                    image_tag="$1"
                fi
                shift
                ;;
        esac
    done
    
    # Validate inputs
    validate_environment "$environment"
    check_prerequisites
    
    echo -e "${BLUE}📋 Deployment Configuration:${NC}"
    echo "  Environment: $environment"
    echo "  Image Tag: $image_tag"
    echo "  Registry: $REGISTRY"
    echo ""
    
    if [[ "$show_diff_only" == "true" ]]; then
        show_diff "$environment" "$image_tag"
    elif [[ "$dry_run" == "true" ]]; then
        build_manifests "$environment" "$image_tag" "$dry_run"
    else
        # Confirm deployment
        read -p "$(echo -e ${YELLOW})Continue with deployment? (y/N): $(echo -e ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            deploy_manifests "$environment" "$image_tag" "$dry_run"
            show_status "$environment"
        else
            echo -e "${YELLOW}❌ Deployment cancelled${NC}"
            exit 0
        fi
    fi
    
    echo -e "${GREEN}🎉 Operation completed successfully!${NC}"
}

# Check if sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi