# Data Challenge

## Environment Setup

1. Start Docker and Kubernetes

2. Deploy Apache Nifi Helm Chart
```
helm repo add cetic https://cetic.github.io/helm-charts
helm install tweets cetic/nifi
```

3. Deploy Apache Kafka Helm Chart
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install tweets-kafka bitnami/kafka --set zookeeper.enabled=false,externalZookeeper.servers=tweets-zookeeper:2181
```

4. Deploy Cassandra Helm Chart
```
helm install tweets-db --set dbUser.user=admin,dbUser.password=<password> bitnami/cassandra
```

5. Upload Nifi template via UI

6. Insert Tweeter API tokens
