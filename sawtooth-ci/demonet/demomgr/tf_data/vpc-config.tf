resource "aws_vpc" "vpc" {
    cidr_block = "10.66.0.0/16"

    tags {
        Name = "${var.owner}-${var.environment}"
        Environment = "${var.environment}"
        owner = "${var.owner}"
    }
}

resource "aws_internet_gateway" "ig" {
    vpc_id = "${aws_vpc.vpc.id}"

    tags {
        Name = "${var.owner}-${var.environment}-internet-gateway"
        Environment = "${var.environment}"
        owner = "${var.owner}"
    }
}
