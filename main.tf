terraform {
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.53.0"
    }
  }
}

# 凭证将通过 Jenkins 环境变量自动注入，这里无需明文填写
provider "openstack" {}

resource "openstack_compute_instance_v2" "ak_app_server" {
  name            = "AK-App-Server"
  image_name      = "ubuntu-20.04"
  flavor_name     = "m1.small"
  key_pair        = "Akbar-ssh-key"
  security_groups = ["students-general", "default"]

  network {
    name = "sutdents-net"
  }
}

# 输出新服务器的 IP，方便给接下来的 Ansible 使用
output "app_server_ip" {
  value = openstack_compute_instance_v2.ak_app_server.access_ip_v4
}
