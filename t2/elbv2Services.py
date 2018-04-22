def getSubnets(resource,vpcIdList):
    subnetsList=[]
    for vpc in resource.vpcs.all():
        for subnet in vpc.subnets.all():
            if vpc.id in vpcIdList:
                subnetsList.append(subnet.id)
    return subnetsList

def createLoadBalancer(client,subnetsList):
    response = client.create_load_balancer(
        Name='elbv2',
        Subnets=subnetsList,
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    return response



def createTargetGroup(client,vpcId,name='nginxTargets'):
    response = client.create_target_group(
        Name=name,
        Protocol='HTTP',
        Port=80,
        VpcId=vpcId,
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=5,
        HealthCheckTimeoutSeconds=4,
        HealthyThresholdCount=2,
        UnhealthyThresholdCount=2,
        TargetType='instance'
    )
    return response

def registerTargets(client,targetGroupArn,targets):
    response = client.register_targets(
        TargetGroupArn=targetGroupArn,
        # Targets=[
        #     {
        #         'Id': 'i-030192a8602ba66bf',
        #         'Port': 80
        #     },
        # ]
        Targets=targets
    )
    return response

def createListener(client,loadBalancerArn,targetGroupArn):
    response = client.create_listener(
       LoadBalancerArn=loadBalancerArn,
       Protocol='HTTP',
       Port=80,
       DefaultActions=[
           {
               'Type': 'forward',
               'TargetGroupArn': targetGroupArn
           },
       ]
    )
    return response

def getTargetHealth(client,targets,targetGroupARN):
    response = client.describe_target_health(
        TargetGroupArn=targetGroupARN,
        Targets=targets
    )
    return response

