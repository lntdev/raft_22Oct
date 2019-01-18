variable "environment_name" {
    default = "green"
}

variable "region" {
	default = "us-east-1"
}

variable "amis" {
    default = {
        us-east-1 = "ami-fce3c696"
        us-west-2 = "ami-9abea4fb"
    }
}

variable "owner" {
	#passed in by wrapper scripts
}
