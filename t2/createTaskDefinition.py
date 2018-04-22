def createTaskDefinition(client,taskName='nginxTask'):
    response = client.register_task_definition(
        containerDefinitions=[
            {
              "name": "nginx",
              "image": "ubuntu:16.04",
              "entryPoint": [
                "/bin/bash",
                "-c",
                "apt-get update && apt-get install -y nginx && /usr/sbin/nginx -g 'daemon off;'"
              ],
              "command": [""],
              "environment": [],
              "mountPoints": [],
              "volumesFrom": [],
              "portMappings": [
                {
                  "containerPort": 80,
                  "hostPort": 80
                }
              ],
              "memory": 256,
              "cpu": 512
            }
        ],
        family=taskName
    )
    return response