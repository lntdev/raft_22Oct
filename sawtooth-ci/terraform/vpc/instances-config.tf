resource "aws_instance" "validator" {
    instance_type = "t2.micro"
    ami = "ami-fce3c696"
    vpc_security_group_ids = ["${aws_security_group.public.id}"]
    associate_public_ip_address = "true"
    key_name = "sawtoothlake"
    subnet_id = "${aws_subnet.public-subnet.id}"
    count = 25

    tags {
        Name = "${var.environment_name}-validator-${count.index}"
        Environment = "${var.environment_name}"
        sshUser = "ubuntu"
    }

}
