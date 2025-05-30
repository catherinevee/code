# Variables
IMAGE_NAME = college-website
IMAGE_TAG = latest
REGISTRY = your-registry-here
NAMESPACE = college-dev

# Build and push image
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

push: build
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

# Deploy with Helm
deploy: push
	helm upgrade --install college-website ./helm-chart/college-website \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--set image.repository=$(REGISTRY)/$(IMAGE_NAME) \
		--set image.tag=$(IMAGE_TAG)

# Local development
dev:
	docker run -p 8080:80 $(IMAGE_NAME):$(IMAGE_TAG)

# Cleanup
clean:
	helm uninstall college-website --namespace $(NAMESPACE)