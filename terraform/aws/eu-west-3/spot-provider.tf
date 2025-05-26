# set credential Azure
resource "spotinst_credentials_azure" "credential" {
  account_id      = var.spotinst_account
  expiration_date = "2027-05-25T23:59:00.000Z"
}