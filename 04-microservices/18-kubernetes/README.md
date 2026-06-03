# Module 18: Kubernetes Deployment

## 🎯 Learning Objectives
- Understand Kubernetes architecture and concepts
- Deploy Python applications to Kubernetes
- Create and manage Pods, Deployments, and Services
- Implement ConfigMaps and Secrets
- Set up Ingress for external access
- Implement auto-scaling and health checks
- Monitor and troubleshoot Kubernetes applications

## 📖 Kubernetes Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  KUBERNETES ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              CONTROL PLANE (Master)                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │   API    │  │Scheduler │  │Controller│        │    │
│  │  │  Server  │  │          │  │ Manager  │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘        │    │
│  │  ┌──────────────────────────────────────┐        │    │
│  │  │            etcd (Storage)             │        │    │
│  │  └──────────────────────────────────────┘        │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │                  WORKER NODES                       │    │
│  │                                                      │    │
│  │  ┌─────────────────┐    ┌─────────────────┐       │    │
│  │  │   Node 1        │    │   Node 2        │       │    │
│  │  │  ┌───────────┐  │    │  ┌───────────┐  │       │    │
│  │  │  │   Pod 1   │  │    │  │   Pod 3   │  │       │    │
│  │  │  │ Container │  │    │  │ Container │  │       │    │
│  │  │  └───────────┘  │    │  └───────────┘  │       │    │
│  │  │  ┌───────────┐  │    │  ┌───────────┐  │       │    │
│  │  │  │   Pod 2   │  │    │  │   Pod 4   │  │       │    │
│  │  │  │ Container │  │    │  │ Container │  │       │    │
│  │  │  └───────────┘  │    │  └───────────┘  │       │    │
│  │  │                 │    │                 │       │    │
│  │  │  Kubelet        │    │  Kubelet        │       │    │
│  │  │  Kube-proxy     │    │  Kube-proxy     │       │    │
│  │  └─────────────────┘    └─────────────────┘       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔑 Key Kubernetes Concepts

### Core Components

| Component | Description |
|-----------|-------------|
| **Pod** | Smallest deployable unit, contains one or more containers |
| **Deployment** | Manages ReplicaSets and provides declarative updates |
| **Service** | Exposes Pods as a network service |
| **ConfigMap** | Store configuration data as key-value pairs |
| **Secret** | Store sensitive data (passwords, tokens) |
| **Ingress** | Manages external access to services (HTTP/HTTPS) |
| **Namespace** | Virtual cluster for resource isolation |
| **PersistentVolume** | Storage resource in the cluster |

## 🚀 Basic Kubernetes Commands

```bash
# Cluster Info
kubectl cluster-info
kubectl get nodes
kubectl get namespaces

# Pods
kubectl get pods
kubectl get pods -n namespace
kubectl describe pod pod-name
kubectl logs pod-name
kubectl exec -it pod-name -- /bin/bash

# Deployments
kubectl get deployments
kubectl create deployment name --image=image
kubectl scale deployment name --replicas=3
kubectl rollout status deployment/name
kubectl rollout undo deployment/name

# Services
kubectl get services
kubectl expose deployment name --port=80 --target-port=8080

# Apply/Delete Resources
kubectl apply -f file.yaml
kubectl delete -f file.yaml
kubectl delete pod pod-name
```

## 📦 Deploying Flask Application

### 1. Pod Definition

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: flask-app-pod
  labels:
    app: flask-app
spec:
  containers:
  - name: flask-container
    image: your-registry/flask-app:latest
    ports:
    - containerPort: 5000
    env:
    - name: FLASK_ENV
      value: "production"
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "200m"
```

### 2. Deployment Definition

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-deployment
  labels:
    app: flask-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: your-registry/flask-app:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 3. Service Definition

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

### 4. ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_NAME: "Flask Application"
  LOG_LEVEL: "INFO"
  MAX_CONNECTIONS: "100"
  config.json: |
    {
      "feature_flags": {
        "new_ui": true,
        "beta_features": false
      }
    }
```

### 5. Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # Base64 encoded values
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0BkYjozMjc2OC9teWRi
  api-key: c3VwZXItc2VjcmV0LWtleQ==
stringData:
  # Plain text (will be encoded automatically)
  jwt-secret: "my-jwt-secret-key"
```

Create secrets from command line:
```bash
kubectl create secret generic app-secrets \
  --from-literal=database-url='postgresql://user:pass@db:5432/mydb' \
  --from-literal=api-key='super-secret-key'
```

### 6. Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.example.com
    secretName: flask-app-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-app-service
            port:
              number: 80
```

## 🔄 Complete Application Deployment

### all-in-one.yaml

```yaml
---
# Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: flask-app

---
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: flask-app
data:
  APP_NAME: "Flask API"
  LOG_LEVEL: "INFO"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: flask-app
type: Opaque
stringData:
  database-url: "postgresql://user:pass@postgres:5432/mydb"
  redis-url: "redis://redis:6379/0"

---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  namespace: flask-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: your-registry/flask-app:v1.0.0
        ports:
        - containerPort: 5000
        env:
        - name: APP_NAME
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_NAME
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
  namespace: flask-app
spec:
  selector:
    app: flask-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: ClusterIP

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-app-ingress
  namespace: flask-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-app-service
            port:
              number: 80
```

Deploy:
```bash
kubectl apply -f all-in-one.yaml
```

## 📈 Auto-Scaling

### Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
  namespace: flask-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 🔍 Health Checks

### Liveness and Readiness Probes

```yaml
spec:
  containers:
  - name: flask-app
    image: flask-app:latest
    # Liveness: Is the container alive?
    livenessProbe:
      httpGet:
        path: /health
        port: 5000
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    
    # Readiness: Is the container ready to serve traffic?
    readinessProbe:
      httpGet:
        path: /ready
        port: 5000
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    
    # Startup: Has the container started?
    startupProbe:
      httpGet:
        path: /health
        port: 5000
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 30
```

### Health Check Endpoints in Flask

```python
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/health')
def health():
    """Liveness probe - basic health check"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/ready')
def ready():
    """Readiness probe - check dependencies"""
    try:
        # Check database connection
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        
        # Check other dependencies
        # ...
        
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        return jsonify({'status': 'not ready', 'error': str(e)}), 503
```

## 💾 Persistent Storage

### PersistentVolumeClaim

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: flask-app
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard
```

### Using PVC in Deployment

```yaml
spec:
  containers:
  - name: postgres
    image: postgres:15
    volumeMounts:
    - name: postgres-storage
      mountPath: /var/lib/postgresql/data
  volumes:
  - name: postgres-storage
    persistentVolumeClaim:
      claimName: postgres-pvc
```

## 🔧 Troubleshooting Commands

```bash
# Get pod details
kubectl describe pod pod-name

# View logs
kubectl logs pod-name
kubectl logs pod-name -f  # Follow logs
kubectl logs pod-name --previous  # Previous container logs

# Execute commands in pod
kubectl exec -it pod-name -- /bin/bash
kubectl exec pod-name -- env

# Port forwarding
kubectl port-forward pod-name 8080:5000

# Get events
kubectl get events --sort-by=.metadata.creationTimestamp

# Debug with temporary pod
kubectl run debug --image=busybox -it --rm -- /bin/sh
```

## 📊 Monitoring and Logging

### Resource Monitoring

```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods
kubectl top pods -n flask-app

# Deployment resources
kubectl top deployment flask-app
```

## 🎯 Best Practices

### 1. Resource Limits

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 2. Health Checks

Always implement liveness and readiness probes.

### 3. Use Namespaces

Organize resources by environment or team.

### 4. Labels and Selectors

```yaml
metadata:
  labels:
    app: flask-app
    version: v1.0.0
    environment: production
    team: backend
```

### 5. Rolling Updates

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### 6. Security

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
```

## 🎯 Key Takeaways

1. **Pods are ephemeral** - Design for failure
2. **Use Deployments** - Not bare Pods
3. **Implement health checks** - Liveness and readiness
4. **Set resource limits** - Prevent resource exhaustion
5. **Use ConfigMaps/Secrets** - Separate config from code
6. **Enable auto-scaling** - Handle variable load
7. **Monitor and log** - Observability is crucial
8. **Use namespaces** - Organize resources

## 🔗 Next Module

[Module 19: CI/CD Pipeline →](../19-cicd/)

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Patterns](https://k8spatterns.io/)