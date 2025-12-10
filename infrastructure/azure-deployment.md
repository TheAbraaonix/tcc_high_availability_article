# Azure Deployment Guide

This guide provides step-by-step instructions for deploying the BLIP image captioning API on Azure Container Apps, replicating the experimental setup from the research paper.

## Prerequisites

- Azure CLI installed and configured
- Docker installed locally
- Azure subscription with appropriate permissions

## Region Selection

The experiments use **East US 2** to match AWS us-east-1 (Virginia) geographic location.

## Step 1: Create Resource Group

```bash
az group create \
    --name rg-blip-caption \
    --location eastus2
```

## Step 2: Create Azure Container Registry (ACR)

```bash
# Create ACR
az acr create \
    --resource-group rg-blip-caption \
    --name <YOUR_REGISTRY_NAME> \
    --sku Basic \
    --location eastus2

# Enable admin access (for deployment)
az acr update \
    --name <YOUR_REGISTRY_NAME> \
    --admin-enabled true

# Get login credentials
az acr credential show \
    --name <YOUR_REGISTRY_NAME>

# Login to ACR
az acr login --name <YOUR_REGISTRY_NAME>
```

## Step 3: Build and Push Docker Image

```bash
cd tcc_high_availability_api

# Build image
docker build -t blip-caption-api:latest .

# Tag for ACR
docker tag blip-caption-api:latest \
    <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest

# Push to ACR
docker push <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest
```

## Step 4: Create Container Apps Environment

```bash
# Install Container Apps extension
az extension add --name containerapp

# Create environment
az containerapp env create \
    --name blip-caption-env \
    --resource-group rg-blip-caption \
    --location eastus2
```

## Step 5: Deploy Container Apps

### Configuration B2 - Baseline (1 Worker, 1 Replica)

```bash
az containerapp create \
    --name blip-baseline \
    --resource-group rg-blip-caption \
    --environment blip-caption-env \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --target-port 8000 \
    --ingress external \
    --cpu 4 \
    --memory 8Gi \
    --min-replicas 1 \
    --max-replicas 1 \
    --env-vars \
        WORKERS=1 \
        PORT=8000
```

### Configuration WS3 - Worker Scaling (2 Workers, 1 Replica)

```bash
az containerapp create \
    --name blip-worker-2 \
    --resource-group rg-blip-caption \
    --environment blip-caption-env \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --target-port 8000 \
    --ingress external \
    --cpu 4 \
    --memory 8Gi \
    --min-replicas 1 \
    --max-replicas 1 \
    --env-vars \
        WORKERS=2 \
        PORT=8000
```

### Configuration WS4 - Worker Scaling (4 Workers, 1 Replica)

```bash
az containerapp create \
    --name blip-worker-4 \
    --resource-group rg-blip-caption \
    --environment blip-caption-env \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --target-port 8000 \
    --ingress external \
    --cpu 4 \
    --memory 8Gi \
    --min-replicas 1 \
    --max-replicas 1 \
    --env-vars \
        WORKERS=4 \
        PORT=8000
```

### Configuration HS3 - Horizontal Scaling (1 Worker, 2 Replicas)

```bash
az containerapp create \
    --name blip-horizontal-2 \
    --resource-group rg-blip-caption \
    --environment blip-caption-env \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --target-port 8000 \
    --ingress external \
    --cpu 4 \
    --memory 8Gi \
    --min-replicas 2 \
    --max-replicas 2 \
    --env-vars \
        WORKERS=1 \
        PORT=8000
```

### Configuration HS4 - Horizontal Scaling (1 Worker, 4 Replicas)

```bash
az containerapp create \
    --name blip-horizontal-4 \
    --resource-group rg-blip-caption \
    --environment blip-caption-env \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --target-port 8000 \
    --ingress external \
    --cpu 4 \
    --memory 8Gi \
    --min-replicas 4 \
    --max-replicas 4 \
    --env-vars \
        WORKERS=1 \
        PORT=8000
```

## Step 6: Get Application URLs

```bash
# List all container apps and their URLs
az containerapp list \
    --resource-group rg-blip-caption \
    --query "[].{Name:name, URL:properties.configuration.ingress.fqdn}" \
    --output table
```

Each app will have a URL like: `https://<APP_NAME>.<UNIQUE_ID>.eastus2.azurecontainerapps.io`

## Step 7: Verify Deployment

### Check App Status

```bash
az containerapp show \
    --name blip-baseline \
    --resource-group rg-blip-caption \
    --query "{Name:name, Status:properties.runningStatus, Replicas:properties.template.scale}" \
    --output table
```

### Test Health Endpoint

```bash
# Get app URL
FQDN=$(az containerapp show \
    --name blip-baseline \
    --resource-group rg-blip-caption \
    --query properties.configuration.ingress.fqdn \
    --output tsv)

# Test health endpoint
curl https://$FQDN/api/health
```

### Test Caption Endpoint

```bash
# Upload image file via form data
curl -X POST https://$FQDN/api/caption \
    -F "file=@test-image.jpg"
```

## Step 8: View Logs

### Stream logs in real-time

```bash
az containerapp logs show \
    --name blip-baseline \
    --resource-group rg-blip-caption \
    --follow
```

### Query logs with Log Analytics

```bash
# Get Log Analytics workspace ID
WORKSPACE_ID=$(az containerapp env show \
    --name blip-caption-env \
    --resource-group rg-blip-caption \
    --query properties.appLogsConfiguration.logAnalyticsConfiguration.customerId \
    --output tsv)

# Query logs (use Azure Portal or CLI)
az monitor log-analytics query \
    --workspace $WORKSPACE_ID \
    --analytics-query "ContainerAppConsoleLogs_CL | where ContainerAppName_s == 'blip-baseline' | project TimeGenerated, Log_s | order by TimeGenerated desc | take 100"
```

## Scaling Notes

### Built-in Load Balancing

Azure Container Apps automatically provides load balancing when `min-replicas` > 1. No additional configuration required.

**How it works:**
- Requests are distributed round-robin across replicas
- Health checks performed automatically on `/api/health`
- Unhealthy replicas are automatically replaced
- No explicit load balancer resource needed (unlike AWS ALB)

### Manual Scaling

To change replica count after deployment:

```bash
az containerapp update \
    --name blip-horizontal-2 \
    --resource-group rg-blip-caption \
    --min-replicas 2 \
    --max-replicas 2
```

## Cost Considerations

### Container Apps Pricing (East US 2, on-demand)
- vCPU: $0.108 per vCPU-hour
- Memory: $0.01188 per GB-hour
- **4 vCPU / 8GB**: ~$0.439 per hour per replica

### No Load Balancer Charges
Unlike AWS, Azure Container Apps includes load balancing at no extra cost.

### Total Hourly Costs
- **B2, WS3, WS4** (1 replica): $0.439/hour
- **HS3** (2 replicas): $0.878/hour
- **HS4** (4 replicas): $1.756/hour

**Note**: Azure is ~5.4× more expensive than AWS for equivalent configurations (4 vCPU / 8GB).

## Alternative: Use Container Instances for Worker Scaling

For configurations that don't need horizontal scaling (B2, WS3, WS4), you can use Azure Container Instances instead of Container Apps for potentially lower costs:

```bash
az container create \
    --name blip-baseline-aci \
    --resource-group rg-blip-caption \
    --image <YOUR_REGISTRY_NAME>.azurecr.io/blip-caption-api:latest \
    --registry-login-server <YOUR_REGISTRY_NAME>.azurecr.io \
    --registry-username <ACR_USERNAME> \
    --registry-password <ACR_PASSWORD> \
    --cpu 4 \
    --memory 8 \
    --ports 8000 \
    --dns-name-label blip-baseline-aci \
    --environment-variables \
        WORKERS=1 \
        PORT=8000
```

**ACI Pricing** (generally lower than Container Apps for single instances):
- vCPU: $0.0000125 per vCPU-second (~$0.045 per vCPU-hour)
- Memory: $0.0000014 per GB-second (~$0.005 per GB-hour)

## Cleanup

```bash
# Delete all container apps
az containerapp delete --name blip-baseline --resource-group rg-blip-caption --yes
az containerapp delete --name blip-worker-2 --resource-group rg-blip-caption --yes
az containerapp delete --name blip-worker-4 --resource-group rg-blip-caption --yes
az containerapp delete --name blip-horizontal-2 --resource-group rg-blip-caption --yes
az containerapp delete --name blip-horizontal-4 --resource-group rg-blip-caption --yes

# Delete environment
az containerapp env delete \
    --name blip-caption-env \
    --resource-group rg-blip-caption \
    --yes

# Delete ACR
az acr delete \
    --name <YOUR_REGISTRY_NAME> \
    --resource-group rg-blip-caption \
    --yes

# Delete resource group (removes everything)
az group delete --name rg-blip-caption --yes
```

## Troubleshooting

### App Won't Start
- Check logs: `az containerapp logs show --name <APP_NAME> --resource-group rg-blip-caption --follow`
- Verify ACR credentials are correct
- Check container resource limits (CPU/memory)

### Health Check Failing
- Verify ingress is configured correctly
- Check target port matches container port (8000)
- Ensure `/api/health` endpoint is accessible
- Review application logs for startup errors

### High Response Times
- Check replica count matches expected configuration
- Monitor CPU/memory utilization in Azure Portal
- Verify thread limiting is working (check logs for threads per worker)
- Compare with AWS performance for same configuration

### Scaling Plateau (HS4 performance same as HS3)
This is a known finding from the research:
- Azure Container Apps shows performance plateau beyond 2 replicas
- 4 replicas provide no additional performance benefit
- Recommend staying at 2 replicas maximum for Azure horizontal scaling

## Monitoring

### Azure Monitor Metrics to Track
- CPU Percentage
- Memory Working Set Percentage
- Requests
- Response Time
- Replica Count

### Log Analytics Queries

**Average response time:**
```kusto
ContainerAppConsoleLogs_CL
| where ContainerAppName_s == "blip-baseline"
| where Log_s contains "Timings"
| extend TotalTime = extract("Total: ([0-9.]+)s", 1, Log_s)
| summarize avg(todouble(TotalTime)) by bin(TimeGenerated, 1m)
```

**Request distribution across replicas:**
```kusto
ContainerAppConsoleLogs_CL
| where ContainerAppName_s contains "horizontal"
| where Log_s contains "Generated caption"
| extend WorkerPID = extract("worker_pid=([0-9]+)", 1, Log_s)
| summarize count() by WorkerPID
```

**Error rate:**
```kusto
ContainerAppConsoleLogs_CL
| where ContainerAppName_s == "blip-baseline"
| where Log_s contains "error" or Log_s contains "failed"
| summarize ErrorCount = count() by bin(TimeGenerated, 5m)
```

## Best Practices

1. **Use Container Apps for horizontal scaling** (HS3, HS4)
2. **Consider ACI for worker scaling** (B2, WS3, WS4) to save costs
3. **Monitor replica distribution** to verify load balancing
4. **Set appropriate health check timeouts** (model loading takes ~30s)
5. **Use Log Analytics** for debugging and performance analysis
6. **Enable Application Insights** for detailed telemetry (optional)

## Comparison with AWS

| Feature | AWS ECS + Fargate | Azure Container Apps |
|---------|------------------|---------------------|
| Load Balancer | Explicit ALB required | Built-in, automatic |
| Cost (4 vCPU/8GB) | $0.081/hour | $0.439/hour |
| Configuration Complexity | Higher (ALB setup) | Lower (managed) |
| Horizontal Scaling | Excellent (3.42× @ 4R) | Limited (1.50× @ 4R) |
| Worker Scaling | Good (1.69× @ 4W) | Good (1.45× @ 4W) |

**Key Finding**: AWS horizontal scaling vastly outperforms Azure, but Azure has simpler configuration. For worker scaling, both platforms perform similarly.
