import boto3
import datetime

def lambda_handler(event, context):
    asg_client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2')

    asg_name = ''

    min_instance_count = 0
    max_instance_count = 5
    desired_instance_count = 0

    asg_client.update_auto_scaling_group (
        AutoScalingGroupName = asg_name,
        MinSize = min_instance_count,
        MaxSize = max_instance_count,
        DesiredCapacity = desired_instance_count
    )


    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    instances = asg_response['AutoScalingGroups'][0]['Instances']

    instance_ids = [i['InstanceId'] for i in instances]

    if instance_ids:
        ec2_client.stop_instances(InstanceIds=instance_ids)
        print(f"Instances are stopped: {instance_ids}")

    else:
        print("No instances are found in ASG....")
        