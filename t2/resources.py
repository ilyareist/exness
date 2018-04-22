import boto3

# Parameters
access_key = ""
secret_key = ""
region = "us-east-2"
cluster_name = "Cluster1"
service_name = "nginxService"
task_name = "nginxTask"

#Resources
#ec2 client
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)
#ec2 resource
ec2_resource = boto3.resource(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)
#ecs client
ecs_client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)
#elbv2 client
elbv2_client = boto3.client(
   'elbv2',
   aws_access_key_id=access_key,
   aws_secret_access_key=secret_key,
   region_name=region
)
