import boto3
import datetime
from instance_start_times import instances_start_times

client = boto3.client('ec2')

def start_ec2_instance(instance_id):
    response = client.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}")

def lambda_handler(event, context):
    current_time = datetime.datetime.now().time()
    
    for instance_id, instance_info in instances_start_times.items():
        start_hour, start_minute = instance_info['start_time']
        if current_time.hour == start_hour and current_time.minute == start_minute:
            start_ec2_instance(instance_id)
            print(f"Started instance {instance_id} at {start_hour}:{start_minute}.")

    return {
        'statusCode': 200,
        'body': 'Function execution completed.'
    }
