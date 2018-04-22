def listECSServices(client,clusterName='Cluster1'):
    response = client.list_services(
        cluster=clusterName,
        maxResults=99,
        launchType='EC2'
    )
    return response

def createECSService(client,targetGroupArn,clusterName='Cluster1',taskDefinition='nginxTask',serviceName='nginxService'):
    response = client.create_service(
        cluster=clusterName,
        serviceName=serviceName,
        taskDefinition=taskDefinition,
        desiredCount=2,
        clientToken='request_identifier_string',
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        },
        loadBalancers=[
            {
                'targetGroupArn': targetGroupArn,
                # 'loadBalancerName': loadBalancerName,
                'containerName': 'nginx',
                'containerPort': 80
            },
        ]
    )
    return response