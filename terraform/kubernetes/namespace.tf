resource "kubernetes_namespace_v1" "ns-terraform" {
  metadata {
   labels = {
     dev-owner = "CathyVee"
   }
   name = "terraform"
  }
}
