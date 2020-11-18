import boto3

def script_handler (events, context):
    policy_arns = [
        'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore',
        'arn:aws:iam::aws:policy/AmazonSSMPatchAssociation'
    ]
    print ("InstanceId: {}".format(events["InstanceId"]))
    iam = boto3.client('iam')
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(
        InstanceIds=[events["InstanceId"]]
    )
    profile_arn = instances['Reservations'][0]["Instances"][0].get('IamInstanceProfile', {}).get('Arn', None)
    print('Profile Arn: {}'.format(profile_arn))
    if not profile_arn:
        print("No instance profile attached, skipping.")
        return "No Profile Attached"

    paginator = iam.get_paginator('list_instance_profiles')
    list_instance_profiles_iterator = paginator.paginate()

    for profiles in list_instance_profiles_iterator:
        for profile in profiles['InstanceProfiles']:
            if profile['Arn'] == profile_arn:
                print("Found matching Arn: {}".format(profile['Arn']))
                profile_role = profile['Roles'][0]['RoleName']                
                for policy in policy_arns:
                    print("Attaching {} to {}".format(policy, profile_role))
                    iam.attach_role_policy(RoleName=profile_role, PolicyArn=policy)
                return "Policies attached to {}".format(profile_role)
    
script_handler ({'InstanceId': "i-123456"}, None)

