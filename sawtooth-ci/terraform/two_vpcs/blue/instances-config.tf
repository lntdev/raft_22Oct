# Instances in the second VPC

#vgroup0
resource "aws_instance" "vgroup0" {
    instance_type = "m3.medium"
    ami = "${lookup(var.amis, var.region)}"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = 1

    tags {
        Name = "${var.owner}-${var.environment_name}-vgroup0-node${count.index}"
        Environment = "${var.environment_name}"
        sshUser = "ubuntu"
        sshArgs = "-o StrictHostKeyChecking=no"
        sawtooth_validator_ledger_url = "**none**"
        sawtooth_validator_genesis_ledger = "true"
        ansible_groups = "vgroup0"
        owner = "${var.owner}"
    }
}

#vgroup1
resource "aws_instance" "vgroup1" {
    instance_type = "m3.medium"
    ami = "${lookup(var.amis, var.region)}"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = 2

    tags {
        Name = "${var.owner}-${var.environment_name}-vgroup1-node${count.index}"
        Environment = "${var.environment_name}"
        sshUser = "ubuntu"
        sshArgs = "-o StrictHostKeyChecking=no"
        ansible_groups = "vgroup1"
        owner = "${var.owner}"
    }
}

#vgroup2
resource "aws_instance" "vgroup2" {
    instance_type = "m3.medium"
    ami = "${lookup(var.amis, var.region)}"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = 2

    tags {
        Name = "${var.owner}-${var.environment_name}-vgroup2-node${count.index}"
        Environment = "${var.environment_name}"
        sshUser = "ubuntu"
        sshArgs = "-o StrictHostKeyChecking=no"
        ansible_groups = "vgroup2"
        owner = "${var.owner}"
    }
}

#clients
resource "aws_instance" "client" {
    instance_type = "m3.medium"
    ami = "${lookup(var.amis, var.region)}"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = 1

    tags {
        Name = "${var.owner}-${var.environment_name}-client-node${count.index}"
        Environment = "${var.environment_name}"
        sshUser = "ubuntu"
        sshArgs = "-o StrictHostKeyChecking=no"
        ansible_groups = "test-client"
        owner = "${var.owner}"
    }
}
