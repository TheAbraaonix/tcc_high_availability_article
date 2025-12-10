# AWS Deployment Guide

This guide provides step-by-step instructions for deploying the BLIP image captioning API on Amazon ECS with Fargate launch type, replicating the experimental setup from the research paper.

## Prerequisites

- AWS CLI installed and configured
- Docker installed locally
- AWS account with appropriate permissions (ECS, ECR, ALB, IAM)

## Region Selection

The experiments use **us-east-1 (Virginia)** to match Azure East US 2 geographic location and avoid Fargate vCPU quota limitations.

## Step 1: Create ECR Repository

```bash
# Create repository
aws ecr create-repository \
    --repository-name blip-caption-api \
    --region us-east-1

# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS \
    --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

## Step 2: Build and Push Docker Image

```bash
cd tcc_high_availability_api

# Build image
docker build -t blip-caption-api:latest .

# Tag for ECR
docker tag blip-caption-api:latest \
    <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/blip-caption-api:latest

# Push to ECR
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/blip-caption-api:latest
```

## Step 3: Create ECS Cluster

```bash
aws ecs create-cluster \
    --cluster-name blip-caption-cluster \
    --region us-east-1
```

## Step 4: Create Task Execution Role

Create IAM role for ECS task execution:

```bash
# Create trust policy file
cat > task-execution-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create role
aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://task-execution-trust-policy.json

# Attach AWS managed policy
aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

## Step 5: Create Task Definitions

### Configuration B1 - Baseline (1 Worker)

```bash
cat > task-def-baseline.json <<EOF
{
  "family": "blip-caption-baseline",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "8192",
  "executionRoleArn": "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "blip-api",
      "image": "<YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/blip-caption-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORKERS",
          "value": "1"
        },
        {
          "name": "PORT",
          "value": "8000"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/blip-caption",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "baseline"
        }
      }
    }
  ]
}
EOF

aws ecs register-task-definition \
    --cli-input-json file://task-def-baseline.json \
    --region us-east-1
```

### Configuration WS1 - Worker Scaling (2 Workers)

```bash
cat > task-def-worker-2.json <<EOF
{
  "family": "blip-caption-worker-2",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "8192",
  "executionRoleArn": "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "blip-api",
      "image": "<YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/blip-caption-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORKERS",
          "value": "2"
        },
        {
          "name": "PORT",
          "value": "8000"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/blip-caption",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "worker-2"
        }
      }
    }
  ]
}
EOF

aws ecs register-task-definition \
    --cli-input-json file://task-def-worker-2.json \
    --region us-east-1
```

### Configuration WS2 - Worker Scaling (4 Workers)

```bash
cat > task-def-worker-4.json <<EOF
{
  "family": "blip-caption-worker-4",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "8192",
  "executionRoleArn": "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "blip-api",
      "image": "<YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/blip-caption-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORKERS",
          "value": "4"
        },
        {
          "name": "PORT",
          "value": "8000"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/blip-caption",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "worker-4"
        }
      }
    }
  ]
}
EOF

aws ecs register-task-definition \
    --cli-input-json file://task-def-worker-4.json \
    --region us-east-1
```

### Configuration HS1/HS2 - Horizontal Scaling (1 Worker per Replica)

Use the baseline task definition (`blip-caption-baseline`) with 2 or 4 replicas configured in the ECS service.

## Step 6: Create Application Load Balancer (for Horizontal Scaling)

**Note**: Only needed for configurations HS1 and HS2. Worker scaling configurations (B1, WS1, WS2) don't require ALB.

```bash
# Create security group for ALB
aws ec2 create-security-group \
    --group-name blip-alb-sg \
    --description "Security group for BLIP ALB" \
    --vpc-id <YOUR_VPC_ID> \
    --region us-east-1

# Allow inbound HTTP
aws ec2 authorize-security-group-ingress \
    --group-id <ALB_SG_ID> \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --region us-east-1

# Create ALB
aws elbv2 create-load-balancer \
    --name blip-caption-alb \
    --subnets <SUBNET_ID_1> <SUBNET_ID_2> \
    --security-groups <ALB_SG_ID> \
    --region us-east-1

# Create target group
aws elbv2 create-target-group \
    --name blip-caption-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id <YOUR_VPC_ID> \
    --target-type ip \
    --health-check-path /api/health \
    --health-check-interval-seconds 30 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3 \
    --region us-east-1

# Create listener
aws elbv2 create-listener \
    --load-balancer-arn <ALB_ARN> \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=<TARGET_GROUP_ARN> \
    --region us-east-1
```

## Step 7: Create CloudWatch Log Group

```bash
aws logs create-log-group \
    --log-group-name /ecs/blip-caption \
    --region us-east-1
```

## Step 8: Deploy ECS Services

### Worker Scaling Configurations (No ALB)

**Baseline (B1):**
```bash
aws ecs create-service \
    --cluster blip-caption-cluster \
    --service-name blip-baseline \
    --task-definition blip-caption-baseline \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SG_ID>],assignPublicIp=ENABLED}" \
    --region us-east-1
```

**Worker Scaling 2 (WS1):**
```bash
aws ecs create-service \
    --cluster blip-caption-cluster \
    --service-name blip-worker-2 \
    --task-definition blip-caption-worker-2 \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SG_ID>],assignPublicIp=ENABLED}" \
    --region us-east-1
```

**Worker Scaling 4 (WS2):**
```bash
aws ecs create-service \
    --cluster blip-caption-cluster \
    --service-name blip-worker-4 \
    --task-definition blip-caption-worker-4 \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SG_ID>],assignPublicIp=ENABLED}" \
    --region us-east-1
```

### Horizontal Scaling Configurations (With ALB)

**Horizontal Scaling 2 Replicas (HS1):**
```bash
aws ecs create-service \
    --cluster blip-caption-cluster \
    --service-name blip-horizontal-2 \
    --task-definition blip-caption-baseline \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SG_ID>]}" \
    --load-balancers "targetGroupArn=<TARGET_GROUP_ARN>,containerName=blip-api,containerPort=8000" \
    --health-check-grace-period-seconds 60 \
    --region us-east-1
```

**Horizontal Scaling 4 Replicas (HS2):**
```bash
aws ecs create-service \
    --cluster blip-caption-cluster \
    --service-name blip-horizontal-4 \
    --task-definition blip-caption-baseline \
    --desired-count 4 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SG_ID>]}" \
    --load-balancers "targetGroupArn=<TARGET_GROUP_ARN>,containerName=blip-api,containerPort=8000" \
    --health-check-grace-period-seconds 60 \
    --region us-east-1
```

## Step 9: Verify Deployment

### Check Service Status

```bash
aws ecs describe-services \
    --cluster blip-caption-cluster \
    --services blip-baseline \
    --region us-east-1
```

### Test Health Endpoint

**Worker Scaling (direct public IP):**
```bash
# Get task public IP
aws ecs list-tasks \
    --cluster blip-caption-cluster \
    --service-name blip-baseline \
    --region us-east-1

aws ecs describe-tasks \
    --cluster blip-caption-cluster \
    --tasks <TASK_ARN> \
    --region us-east-1

# Test health endpoint
curl http://<TASK_PUBLIC_IP>:8000/api/health
```

**Horizontal Scaling (via ALB):**
```bash
# Get ALB DNS name
aws elbv2 describe-load-balancers \
    --names blip-caption-alb \
    --region us-east-1 \
    --query 'LoadBalancers[0].DNSName' \
    --output text

# Test health endpoint
curl http://<ALB_DNS_NAME>/api/health
```

### Test Caption Endpoint

```bash
# Create test image file
echo '{"imageUrl":"https://example.com/image.jpg"}' > test.json

# Send request (replace URL with actual endpoint)
curl -X POST http://<ENDPOINT>/api/caption \
    -H "Content-Type: application/json" \
    -d @test.json
```

## Cost Considerations

### Fargate Pricing (us-east-1, on-demand)
- vCPU: $0.04048 per vCPU-hour
- Memory: $0.004445 per GB-hour
- **4 vCPU / 8GB**: ~$0.081 per hour per task

### ALB Pricing (us-east-1)
- ALB-hour: $0.0225 per hour
- LCU-hour: $0.008 per LCU-hour (varies with traffic)

### Total Hourly Costs
- **B1, WS1, WS2** (1 replica, no ALB): $0.081/hour
- **HS1** (2 replicas + ALB): ~$0.185/hour
- **HS2** (4 replicas + ALB): ~$0.345/hour

## Cleanup

```bash
# Delete services
aws ecs delete-service --cluster blip-caption-cluster --service blip-baseline --force
aws ecs delete-service --cluster blip-caption-cluster --service blip-worker-2 --force
aws ecs delete-service --cluster blip-caption-cluster --service blip-worker-4 --force
aws ecs delete-service --cluster blip-caption-cluster --service blip-horizontal-2 --force
aws ecs delete-service --cluster blip-caption-cluster --service blip-horizontal-4 --force

# Delete ALB
aws elbv2 delete-load-balancer --load-balancer-arn <ALB_ARN>
aws elbv2 delete-target-group --target-group-arn <TARGET_GROUP_ARN>

# Delete cluster
aws ecs delete-cluster --cluster blip-caption-cluster

# Delete ECR repository
aws ecr delete-repository --repository-name blip-caption-api --force

# Delete CloudWatch log group
aws logs delete-log-group --log-group-name /ecs/blip-caption
```

## Troubleshooting

### Task Won't Start
- Check CloudWatch logs: `aws logs tail /ecs/blip-caption --follow`
- Verify task execution role has ECR pull permissions
- Check vCPU quota limits for Fargate

### Health Check Failing
- Verify security group allows traffic on port 8000
- Check container logs for startup errors
- Ensure `/api/health` endpoint is accessible

### High Response Times
- Check CloudWatch metrics for CPU/memory utilization
- Verify thread limiting configuration (logs show threads per worker)
- Monitor ALB metrics for connection counts and latency

## Monitoring

### CloudWatch Metrics to Track
- `CPUUtilization`
- `MemoryUtilization`
- `TargetResponseTime` (ALB)
- `HealthyHostCount` / `UnHealthyHostCount` (ALB)
- `RequestCount` (ALB)

### Useful CloudWatch Insights Queries

**Average response time per worker:**
```
fields @timestamp, worker_pid, Total
| filter @message like /Timings/
| stats avg(Total) by worker_pid
```

**Request distribution across workers:**
```
fields @timestamp, worker_pid
| filter @message like /Generated caption/
| stats count() by worker_pid
```
