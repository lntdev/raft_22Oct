resource "aws_eip" "ip" {
    instance = "${aws_instance.login_host.id}"
}
