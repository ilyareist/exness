def create_ec2(client,cluster="Cluster1"):
    user_data = '''#!/bin/bash
    echo ECS_CLUSTER=Cluster1 >> /etc/ecs/ecs.config'''
    response = client.run_instances(
        ImageId="ami-64300001",
        MinCount=2,
        MaxCount=2,
        UserData=user_data,
        InstanceType="t2.micro",
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },

    )
    return response
