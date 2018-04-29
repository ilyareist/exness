import time
import requests
from .createEC2 import create_ec2
from .createECSCluster import createECSCluster
from .createTaskDefinition import createTaskDefinition
from .createECSService import *
from .elbv2Services import *
from .resources import *

# creating ECS cluster
print('Creating ECS cluster...')
ECSCluster=createECSCluster(ecs_client)
print('ECS cluster %s was created' %ECSCluster["cluster"]["clusterName"])

# creating EC2 instances
print('Creating EC2 instances...')
instances=create_ec2(ec2_client)["Instances"]

# Waiting runnins state
vpcIdList=[]
instancesIDList=[]
for instance in instances:
    instanceID=instance["InstanceId"]
    instancesIDList.append(instanceID)
    vpcIdList.append(instance["VpcId"])
    print('Creating %s instance' %instanceID)
    instance = ec2_resource.Instance(instanceID)
    while instance.state["Name"] != 'running':
        print('...instance is %s' % instance.state["Name"])
        time.sleep(3)
        instance = ec2_resource.Instance(instanceID)

print('EC2 instances %s were created \n' %instancesIDList)


#Creating a task definition
print('Creating a task definition...')
taskDefinition=createTaskDefinition(ecs_client,task_name)
print('ECS task definition %s was registered \n' %taskDefinition["taskDefinition"]["family"])

# Getting EC2 instances's subnets
subnets=getSubnets(ec2_resource,vpcIdList)

# Creating load balancer
print('Creating a load balancer')
loadBalancer=createLoadBalancer(elbv2_client,subnets)
loadBalancerARN=loadBalancer["LoadBalancers"][0]["LoadBalancerArn"]
loadBalancerName=loadBalancer["LoadBalancers"][0]["LoadBalancerName"]
loadBalancerDNSName=loadBalancer["LoadBalancers"][0]["DNSName"]
print('Load balancer %s was created \n' %loadBalancerName)

# Creating target group
print('Creating and registering target group...')
targetGroup=createTargetGroup(elbv2_client,vpcIdList[0])
targetGroupARN = targetGroup["TargetGroups"][0]["TargetGroupArn"]
targetGroupName = targetGroup["TargetGroups"][0]["TargetGroupName"]
targets=[]
for instanceID in instancesIDList:
    target={'Id':instanceID,'Port':80}
    targets.append(target)

# Registering targets
registerTargetsRespose = registerTargets(elbv2_client,targetGroupARN,targets)
print('Target group %s was created and registered with targets %s \n' % (targetGroupName,targets))

# Create listener
print('Creating listener')
listener=createListener(elbv2_client,loadBalancerARN,targetGroupARN)
print("Listener Arn is " + listener["Listeners"][0]["ListenerArn"])

# Creating service
ECSServices = listECSServices(ecs_client)["serviceArns"]
if any(service_name in s for s in ECSServices):
    print("%s already exists" % service_name)
    ECSServiceName=service_name
else:
    print('Creating service')
    ECSService = createECSService(ecs_client, targetGroupARN)
    ECSServiceName=ECSService["service"]["serviceName"]
    print('Service %s was created \n' % ECSServiceName)

# Checking health
print('Checking health')
targetsHealth=getTargetHealth(elbv2_client,targets,targetGroupARN)

for indx,targetHealth in enumerate(targetsHealth["TargetHealthDescriptions"]):
    targetState=targetHealth["TargetHealth"]["State"]
    targetId=targetHealth["Target"]["Id"]
    # targetReason=targetHealth["TargetHealth"]["Reason"]
    while targetState != 'healthy':
        print('Service %s on instance %s is in %s state' % (ECSServiceName,targetId,targetState))
        time.sleep(60)
        targetHealth = getTargetHealth(elbv2_client, targets, targetGroupARN)["TargetHealthDescriptions"][indx]
        targetState = targetHealth["TargetHealth"]["State"]
        # targetReason = targetHealth["TargetHealth"]["Reason"]
    else:
        print('Service %s on instance %s is in %s state \n' % (ECSServiceName,targetId,targetState))

# Checking via http code
r = requests.head("http://"+loadBalancerDNSName)
if r.status_code == 200:
    print("Finished successfully")
    print('Service %s was sucessfully created on %s instances' % (ECSServiceName,instancesIDList))
    print("DNS name is " + loadBalancerDNSName)
else:
    print('Error: Service %s was created on %s, but not available by %s address ' % (ECSServiceName,instancesIDList,loadBalancerDNSName))
