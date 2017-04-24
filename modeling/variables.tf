variable "ami" {
	type = "string"
	default = "ami-b54364d0"
}

variable "spot_price" {
	type = "string"
	default = "0.20"
}

variable "profile" {
	type = "string"
	default = "Modeler"
}

variable "subnet" {
	type = "string"
	default = "subnet-6347d50a"
}

# These allow Josiah home, Sochor home and prog network IPs ssh access
variable "security_groups" {
	type = "list"
	default = ["sg-531f533a", "sg-a51d51cc", "sg-c11c50a8"] 
}

variable "volume_type" {
	type = "string"
	default = "gp2"
}

variable "volume_size" {
	type = "string"
	default = "128"
}

variable "region" {
	type = "string"
	default = "us-east-2"
}

variable "instance_type" {
	type = "string"
	default = "p2.xlarge"
}