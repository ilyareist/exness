def createECSCluster(client,clusterName='Cluster1'):
    responseCluster = client.create_cluster(
        clusterName=clusterName
    )
    return responseCluster