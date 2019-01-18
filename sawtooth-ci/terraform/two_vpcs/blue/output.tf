output "ips0" {
    value = "${join("/32,", aws_instance.vgroup0.*.public_ip)}"
}

output "ips1" {
    value = "${join("/32,", aws_instance.vgroup1.*.public_ip)}"
}

output "ips2" {
    value = "${join("/32,", aws_instance.vgroup2.*.public_ip)}"
}

output "client_ips" {
    value = "${join("/32,", aws_instance.client.*.public_ip)}"
}
