resource "aws_volume_attachment" "ebs_att" {
    device_name = "/dev/sdf"
    volume_id = "vol-5890f889"
    instance_id = "${aws_instance.login_host.id}"
}
