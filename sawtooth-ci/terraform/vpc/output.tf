output "ips" {
    value = "${join(", ", aws_instance.validator.*.public_ip)}"
}
