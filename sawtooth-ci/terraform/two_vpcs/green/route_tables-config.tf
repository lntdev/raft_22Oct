resource "aws_route_table" "public-subnet" {
    vpc_id = "${aws_vpc.vpc.id}"

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.ig.id}"
    }

    tags {
        Name = "${var.owner}-${var.environment_name}-public-subnet-route-table"
        Environment = "${var.environment_name}"
        owner = "${var.owner}"
    }
}

resource "aws_route_table_association" "public-subnet" {
    subnet_id = "${aws_subnet.public-subnet.id}"
    route_table_id = "${aws_route_table.public-subnet.id}"
}
