resource "aws_subnet" "public-subnet" {
    vpc_id = "${aws_vpc.environment.id}"
    cidr_block = "${var.vpc_public_subnet.cidr_block}"
    availability_zone = "us-east-1a"

    tags {
        Name = "${var.environment_name}-public-subnet"
        Environment = "${var.environment_name}"
    }
}
