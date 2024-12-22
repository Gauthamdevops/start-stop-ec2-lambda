
import boto3
import datetime

def lambda_handler(event, context):
    asg_client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2')
    
    # Replace 'your-asg-name' with your actual Auto Scaling Group name
    asg_name = 'StartStopEC2LambdaASG'
    
    # Define desired instance counts
    min_instance_count = 1  # Set the minimum number of instances
    max_instance_count = 5  # Set the maximum number of instances
    desired_instance_count = 3  # Set the desired number of instances
    
    # Update the ASG with new instance counts
    asg_client.update_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        MinSize=min_instance_count,
        MaxSize=max_instance_count,
        DesiredCapacity=desired_instance_count
    )
    
    # Get the list of instances in the ASG
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    instances = asg_response['AutoScalingGroups'][0]['Instances']
    
    # Extract instance IDs
    instance_ids = [i['InstanceId'] for i in instances]

    if instance_ids:
        ec2_client.start_instances(InstanceIds=instance_ids)
        print(f"Started instances: {instance_ids}")
    else:
        print("No instances found in the ASG.")
    
    return {
        'statusCode': 200,
        'body': 'Instances started and ASG updated successfully'
    }

