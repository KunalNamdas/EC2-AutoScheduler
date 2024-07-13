import boto3
import datetime
from instance_stop_times import instances_stop_times

client = boto3.client('ec2')

def stop_ec2_instance(instance_id):
    response = client.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}")

def lambda_handler(event, context):
    current_time = datetime.datetime.now().time()
    
    for instance_id, instance_info in instances_stop_times.items():
        stop_hour, stop_minute = instance_info['stop_time']
        if current_time.hour == stop_hour and current_time.minute == stop_minute:
            stop_ec2_instance(instance_id)
            print(f"Stopped instance {instance_id} at {stop_hour}:{stop_minute}.")

    return {
        'statusCode': 200,
        'body': 'Function execution completed.'
    }
