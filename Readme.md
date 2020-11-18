# aws-ssm-quicksetup-for-existing-roles

This CloudFormation template deploys resources to automatically attach `AmazonSSMManagedInstanceCore`  and `AmazonSSMPatchAssociation` policies to any existing EC2 instance roles that are attached to EC2 instances, so that the SSM Agent is able to communicate with the AWS Systems Manager service. It addresses scenarios where EC2 instances already have an IAM role attached that should not be replaced with the SSM QuickSetup role. 

**Note:** This template is meant to be used **in conjuction** with SSM QuickSetup, which creates an EC2 instance role and applies it to instances that do not already have a role attached. It is recommended you use both to ensure all EC2 instances are able to communicate with Systems Manager.

## How it Works
Once deployed, the following occurs:
1. A Systems Manager State Manager Association targets EC2 instances with an Systems Manager Automation Document.
2. The Automation Document executes a script that checks if the EC2 instance already has an Instance Profile attached. 
3. If a profile is attached, it finds the associated IAM Role and attached the AmazonSSMManagedInstanceCore policy to the role.
4. The SSM Agent will begin communicating with the Systems Manager Service.

**Note:** The automation uses an IAM role with scoped permissions to perform these operations

The State Manager association is configured to run immediately on any newly targeted instance, and repeat once per day.

![Architecture Diagram](/images/diagram.png)