output "ips" {
    value = ["${aws_instance.lr_test.*.public_ip}"]
}
output "tags" {
    value = ["${aws_instance.lr_test.*.tags}"]
}
