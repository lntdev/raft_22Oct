# Publishing a Sawtooth AMI

You'll need a couple of things before getting started:

1. Correctly configured AWS config and credentials files. Instructions and examples can be found here: http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html

	Set your region to the us-east-1 values specified in credentials, which should be for the 863073748941 account

2. The script assumes you have the ami_creation.pem private key in your ~/.ssh folder.

3. Login access to the tci-lustre (863110175750) Intel AWS account.


## Building the AMI
First, build the Docker image we'll use to create the AMI:

```
$ cd sawtooth-ci/ami
$ docker build -t build_ami docker/
```

Generate the AMI for submission:

```
$ cd sawtooth-ci/ami
$ docker run -it --rm \
  -v ~/.aws/:/root/.aws/ \
  -v $(pwd)/:/project \
  -v ~/.ssh/:/root/.ssh \
  build_ami
```

Once the script completes (usually 5-6 min), make note of the output values at the end. We'll use these to identify the AMI we want to publish.

```
...
[--- AMI Info ---]

AMI Name: Sawtooth 0.8 20170919
AMI ID: ami-5a698520
```

## Copy the AMI to the tci-lustre account

+ Log into the tci-lustre AWS account at http://awslogin.intel.com.
After logging in, click [here](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Images:visibility=private-images;sort=name) to navigate to the private AMI listings page.
+ Enter the AMI Name or AMI ID in the search box.
+ Right click anywhere in the row and choose *Copy AMI*.
+ Remove _[Copied ami-XXXXXX from us-east-1]_ from the description. The destination region MUST be **US East (N. Virginia)**.


## Update the listing

+ Visit the [Self-Service Listings](https://aws.amazon.com/marketplace/management/products/?#) page.
+ Find Hyperledger Sawtooth in the _Current Listings_ section at the bottom of the page. 
+ Choose _Edit listing_ from the _Select action_ dropdown.
+ Make any updates here. You can use the _Prev_ and _Next_ buttons to move from section to section or use the headers on top.
+ Click _Review_ on the final page once your updates are complete.
