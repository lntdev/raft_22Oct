resource "aws_security_group" "public" {
    name = "${var.owner}-${var.environment_name}-public"

    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["52.202.97.218/32"]
    }
    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["${split(",", var.validator_ingress)}"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    vpc_id = "${aws_vpc.vpc.id}"
    tags {
        Name = "${var.owner}-${var.environment_name}-public-security-group"
        Environment = "${var.environment_name}"
        owner = "${var.owner}"
    }
}
