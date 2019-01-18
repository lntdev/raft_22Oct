resource "aws_instance" "login_host" {
    ami = "${lookup(var.amis, var.region)}"
    instance_type = "t2.medium"
	key_name = "sawtoothlake"

	tags {
	  Name = "frost (login host)"
    }
}
