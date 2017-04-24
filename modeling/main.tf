# Configure the AWS Provider
provider "aws" {
	region     = "us-east-2"
}

# Create a web server
resource "aws_spot_instance_request" "gpu" {
	ami = "ami-4c614629"  # Deep learning AMI on what-is-my-fish AWS account
	instance_type = "p2.xlarge"
	spot_price    = "0.20"
	iam_instance_profile = "Modeler"
	subnet_id = "subnet-6347d50a"
	vpc_security_group_ids = ["sg-531f533a", "sg-a51d51cc", "sg-c11c50a8"] # currently prog network, Sochor and Josiah home IPs
}

output "ip" {
  value = "${aws_spot_instance_request.gpu.public_ip}"
}