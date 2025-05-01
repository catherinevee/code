resource "kubernetes_deployment_v1" "k8s_deployment" {
  depends_on = [
    kubernetes_namespace_v1.ns_terraform 
  ]
  metadata {
    name = "cathykb"
    labels = {
      test = "cate-k8"
    }
  }
  spec {
    replicas = 3
    
    selector {
      match_labels = "cate-k8"
    }
    template {
      metadata {
        labels = {
          appName= "cate-k8"
        }
      }
      spec {
        container {
          image = "nginx"
          name = "sdfs"
        }
        }
      }
    }
  }
  
}

