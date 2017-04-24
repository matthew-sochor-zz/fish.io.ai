provider "aws" {
	region     = "${var.region}"
}

resource "aws_spot_instance_request" "gpu" {
	ami = "${var.ami}"
	instance_type = "${var.instance_type}"
	spot_price    = "${var.spot_price}"
	iam_instance_profile = "${var.profile}"
	subnet_id = "${var.subnet}"
	vpc_security_group_ids =  "${var.security_groups}"
	root_block_device = {
		volume_type = "${var.volume_type}"
		volume_size = "${var.volume_size}"
	}
}

output "ip" {
  value = "${aws_spot_instance_request.gpu.public_ip}"
}