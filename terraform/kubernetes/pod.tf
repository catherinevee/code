resource "Kubernetes_service_v1" "sv" {
  metadata {
    name = "sv-nginx"
    namespace = "terraform"
  }
  spec {
    selector = {
      appName = kubernetes_deployment_v1.k8s-deployment.spec[0].match_labels.appName
    port = {
      port = 80
      target_port = 90
    }
    type = "ClusterIP"
    }
  }
}
