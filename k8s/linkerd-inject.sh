#!/bin/bash
# k8s/linkerd-inject.sh
# Sets up k3d cluster, installs Linkerd, and deploys services

set -e

CLUSTER_NAME="quote-mesh"

echo "=== Step 1: Create k3d cluster ==="
# Delete existing cluster if it exists
k3d cluster delete $CLUSTER_NAME 2>/dev/null || true
k3d cluster create $CLUSTER_NAME --wait

echo "=== Step 2: Build and import Docker image ==="
docker build -t quote-service:local -f quote_service/Dockerfile .
k3d image import quote-service:local -c $CLUSTER_NAME

echo "=== Step 3: Install Linkerd ==="
linkerd check --pre
# Delete conflicting k3s Gateway API CRD if present
kubectl delete crd httproutes.gateway.networking.k8s.io 2>/dev/null || true
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check

echo "=== Step 4: Install Linkerd Viz extension ==="
linkerd viz install | kubectl apply -f -
linkerd viz check

echo "=== Step 5: Deploy Consul ==="
kubectl apply -f k8s/consul.yaml
echo "Waiting for Consul to be ready..."
kubectl wait --for=condition=ready pod -l app=consul --timeout=60s

echo "=== Step 6: Deploy Quote Services (with Linkerd injection) ==="
cat k8s/deployment.yaml | linkerd inject - | kubectl apply -f -
kubectl wait --for=condition=ready pod -l app=quote-service --timeout=60s

echo "=== Step 7: Deploy Kubernetes Service ==="
kubectl apply -f k8s/service.yaml

echo ""
echo "=== Deployment complete! ==="
echo ""
echo "View Linkerd dashboard:  linkerd viz dashboard"
echo "View Consul UI:          kubectl port-forward svc/consul 8500:8500"
echo "Test quote service:      kubectl port-forward svc/quote-service 8080:80"
echo ""
echo "To clean up:  k3d cluster delete $CLUSTER_NAME"
