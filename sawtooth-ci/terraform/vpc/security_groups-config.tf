resource "aws_security_group" "public" {
    name = "${var.environment_name}-public"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["52.202.97.218/32"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["${var.vpc.cidr_block}"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    vpc_id = "${aws_vpc.environment.id}"
    tags {
        Name = "${var.environment_name}-public-security-group"
        Environment = "${var.environment_name}"
    }
}
