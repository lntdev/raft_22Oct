resource "aws_instance" "lr_test" {
    instance_type = "${var.instance_type}"
    ami = "${var.ami}"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = "${var.count}" 

    tags {
        Name = "${var.network_id}-node${count.index}"
        Environment = "${var.environment}"
        Network = "${var.network_id}"
        sshUser = "${var.host_user}"
        sshArgs = "-o StrictHostKeyChecking=no"
        owner = "${var.owner}"
    }
}

