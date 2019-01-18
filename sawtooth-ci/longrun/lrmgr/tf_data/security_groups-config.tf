resource "aws_security_group" "public" {
    name = "${var.owner}-${var.environment}-public"

    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
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
        Name = "${var.owner}-${var.environment}-public-security-group"
        Environment = "${var.environment}"
        owner = "${var.owner}"
    }
}

variable "validator_ingress" {
    default = "8.8.8.8/32"
}
