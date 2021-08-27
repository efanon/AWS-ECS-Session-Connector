# AWS SESSION MANAGER CONNECTOR

It is a simple script to help with execute command or connect to ECS instances.

## Using
This script use aws profiles to manage multi-account architecture and etc. 
To use it you have to use credentails file https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

```python3 ./aws_session_connector.py {region} {command}```

### arguments
- region - code of AWS region (required)
- command - command to execute (default: /bin/sh)

## Requirements
- python v3.6 or upper
- boto3, simple_term_menu ``` python3 -m pip install boto3 simple-term-menu ```
- aws-cli v2 - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
- Session Manager plugin for the AWS CLI - https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

## Troubleshooting
- ```No items to show. Exit``` - there is no clusters or services or tasks or containers to show
- ```Region not set, please pass region as first argument.``` - you must pass region at first argument
- ```Client error...``` - there is problem with communication with aws. Token expired?
- ```An error occurred (InvalidParameterException) when calling the ExecuteCommand operation: The execute command failed because execute command was not enabled when the task was run or the execute command agent isn’t running. Wait and try again or run a new task with execute command enabled and try again.``` - Command execute is disabled. Every problem with connection to container you can check using awsome tool: https://github.com/aws-containers/amazon-ecs-exec-checker  