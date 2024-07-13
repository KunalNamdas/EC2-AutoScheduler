# EC2 Instance Scheduler

This project contains AWS Lambda functions and associated configuration to automatically start and stop EC2 instances at predefined times using Amazon EventBridge.

## Table of Contents
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Files](#files)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Guide](#step-by-step-guide)
    - [Create the Python Scripts](#create-the-python-scripts)
    - [Upload Scripts to AWS Lambda](#upload-scripts-to-aws-lambda)
    - [Set up EventBridge Rule](#set-up-eventbridge-rule)
    - [Test and Monitor](#test-and-monitor)
    - [Automate Stopping Instances](#automate-stopping-instances)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project helps in reducing costs by automating the start and stop times of EC2 instances. It uses AWS Lambda and Amazon EventBridge to schedule the operations.

## Architecture

1. **Lambda Functions**: One for starting and one for stopping EC2 instances.
2. **Amazon EventBridge**: To trigger Lambda functions at specified times.

## Files

- `instance_start_times.py`: Contains start times for EC2 instances.
- `lambda_function.py`: Lambda function to start EC2 instances.
- `instance_stop_times.py`: Contains stop times for EC2 instances.
- `lambda_stop_function.py`: Lambda function to stop EC2 instances.

## Setup

### Prerequisites

- AWS Account
- Python 3.8 or higher
- AWS CLI configured with appropriate permissions

### Step-by-Step Guide

#### Create the Python Scripts

1. **Create `instance_start_times.py`**:

   ```python
   instances_start_times = {
       'i-093267da3c1de1896': {'start_time': (9, 0)},  # Start at 9:00 AM
       'i-0bbe2f658084c8d4f': {'start_time': (14, 0)}  # Start at 2:00 PM
       # Add more instances and their start times as needed
   }

  2. **Create `lambda_function.py`**:

   ```python
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

   }
  ```

3. **Create `instance_stop_times.py`**:

   ```python
   instances_stop_times = {
       'i-093267da3c1de1896': {'stop_time': (your-time, 0)},  # stop at 5:00 AM
       'i-0bbe2f658084c8d4f': {'stop_time': (your-time, 0)}  # stop at 6:00 PM
       # Add more instances and their start times as needed
   }


4.  **lambda_stop_function.py`**:
  ```python
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

  ```


## Upload Scripts to AWS Lambda

### 1 Create a new Lambda function:

Navigate to AWS Lambda in the AWS Management Console.

- Click "Create function."

- Choose "Author from scratch."

- Name the function (e.g., EC2StartScheduler).

- Choose Python 3.8 or higher as the runtime.

- Create or select an execution role with permissions to start EC2 instances.
  

### 2 Upload the Python scripts:

In the Lambda function dashboard, go to the "Code" tab.

Click "Upload from" and select "zip file."

Create a ZIP file containing instance_start_times.py, lambda_function.py, instance_stop_times.py, and lambda_stop_function.py.

Upload the ZIP file.




##  Set up EventBridge Rule

### 1 Navigate to Amazon EventBridge:

- In the AWS Management Console, go to Amazon EventBridge.

###   2 Create a new rule for starting instances:

- Click "Create rule."

- Name the rule (e.g., EC2StartSchedulerRule).

- Choose "Schedule" as the event source.

- Define a schedule expression (e.g., rate(1 minute)).


### 3 Add the Lambda function as the target:

- Under "Targets," click "Add target."

- Select "Lambda function."

- Choose the Lambda function you created.


### 4 Configure permissions:

- Ensure EventBridge can invoke the Lambda function.

- Modify the IAM role if necessary.


### 5 Create a new rule for stopping instances:

- Repeat the above steps to create another rule for stopping instances.

- Name the rule (e.g., EC2StopSchedulerRule).

- Define a schedule expression (e.g., rate(1 minute)).

- Add the stop Lambda function (lambda_stop_function.py) as the target.



### Test and Monitor

## 1 Test the Lambda function:

- In the Lambda function dashboard, click "Test."

- Create a test event.

- Verify the function starts and stops the specified EC2 instances.
  

## 2 Monitor the EventBridge rule:

- Check CloudWatch Logs for Lambda function output.

- Ensure the rule triggers the Lambda function as expected.

# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

# License

### This project is licensed under the MIT License.

This `README.md` file includes all necessary instructions and script content, making it easy to copy and paste everything into your GitHub repository.






