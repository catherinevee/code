

resource "azurerm_network_interface" "nic" {
  name = "dev${count.index}-nic"
  count = 3 
  location            = var.defaultlocation
  resource_group_name = var.mexicocentralresourcegroups[2]

  ip_configuration {
    name                          = "ipconfig${count.index}"
    subnet_id                     = azurerm_subnet.mexicocentralsubnet_dev.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_virtual_machine" "main" {
  name                  = "dev${count.index}-vm"
  location              = var.defaultlocation
  resource_group_name   = var.mexicocentralresourcegroups[2]
  network_interface_ids = [azurerm_network_interface.nic[count.index].id]
  vm_size               = "Standard_DS1_v2"

  # Uncomment this line to delete the OS disk automatically when deleting the VM
  # delete_os_disk_on_termination = true

  # Uncomment this line to delete the data disks automatically when deleting the VM
  # delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "dev${count.index}-vm"
    admin_username = "admin"
    admin_password = "9827192fv9182nvnsksiq827103vnanas827301mvkz"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
  tags = var.tags
}