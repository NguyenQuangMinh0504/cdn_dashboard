provider "google" {
    credentials = file("~/.config/gcloud/application_default_credentials.json")
    project = "cdn-demo-1"
    region = "us-central1"
}

resource "google_compute_instance" "default" {
    name = "cdn-dashboard"
    machine_type = "e2-small"
    zone = "us-central1-a"
    boot_disk {
      initialize_params {
        image = "debian-cloud/debian-12"
      }
    }
    network_interface {
      network = "default"
      access_config {
        
      }
    }
    tags = ["http-server","https-server"]
}

resource "google_compute_firewall" "allow_redis" {
  name    = "allow-redis"
  network = "default"
  allow {
    ports    = ["6379"]
    protocol = "tcp"
  }
  priority    = 1000
  direction = "INGRESS"
  source_ranges = ["0.0.0.0/0"]
}