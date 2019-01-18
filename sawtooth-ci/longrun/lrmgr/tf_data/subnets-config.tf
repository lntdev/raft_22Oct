resource "aws_subnet" "public-subnet" {
    vpc_id = "${aws_vpc.vpc.id}"
    cidr_block = "10.66.0.0/24"
    availability_zone = "${var.availability_zone}"

    tags {
        Name = "${var.owner}-${var.environment}-public-subnet"
        Environment = "${var.environment}"
        owner = "${var.owner}"
    }
}

