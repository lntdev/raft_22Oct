resource "aws_vpc" "vpc" {
    cidr_block = "${var.vpc.cidr_block}"

    tags {
        Name = "${var.owner}-${var.environment_name}"
        Environment = "${var.environment_name}"
        owner = "${var.owner}"
    }
}

resource "aws_internet_gateway" "ig" {
    vpc_id = "${aws_vpc.vpc.id}"

    tags {
        Name = "${var.owner}-${var.environment_name}-internet-gateway"
        Environment = "${var.environment_name}"
        owner = "${var.owner}"
    }
}
