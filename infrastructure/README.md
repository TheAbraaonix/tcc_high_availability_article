# Infrastructure and Deployment Scripts

This directory contains deployment scripts and infrastructure configuration for reproducing the experimental setup described in the paper "AWS vs Azure Performance Comparison for CPU-Intensive Transformer-Based Inference: A Controlled Experimental Study".

## Repository Links

- **Backend API**: https://github.com/TheAbraaonix/tcc_high_availability_api
- **Frontend Testing Application**: https://github.com/TheAbraaonix/tcc_high_availability_front

## Prerequisites

- Docker and Docker Compose installed
- AWS CLI configured (for AWS deployment)
- Azure CLI configured (for Azure deployment)
- Node.js 18+ (for running frontend locally)
- Python 3.12+ (for local development)

## Quick Start

### 1. Clone Repositories

```bash
git clone https://github.com/TheAbraaonix/tcc_high_availability_api.git
git clone https://github.com/TheAbraaonix/tcc_high_availability_front.git
```

### 2. Build Backend Docker Image

```bash
cd tcc_high_availability_api
docker build -t blip-caption-api:latest .
```

### 3. Run Backend Locally

**Baseline (1 worker):**
```bash
docker run -p 8000:8000 -e WORKERS=1 blip-caption-api:latest
```

**Worker Scaling (2 workers):**
```bash
docker run -p 8000:8000 -e WORKERS=2 blip-caption-api:latest
```

**Worker Scaling (4 workers):**
```bash
docker run -p 8000:8000 -e WORKERS=4 blip-caption-api:latest
```

### 4. Run Frontend Locally

```bash
cd tcc_high_availability_front
npm install
npm run dev
```

Access at `http://localhost:5173`

## Cloud Deployment

### AWS Deployment (ECS with Fargate)

See [aws-deployment.md](./aws-deployment.md) for detailed AWS deployment instructions including:
- ECR repository creation
- ECS cluster setup
- Task definitions for each configuration
- Application Load Balancer configuration
- Service deployment and scaling

### Azure Deployment (Container Apps)

See [azure-deployment.md](./azure-deployment.md) for detailed Azure deployment instructions including:
- Azure Container Registry setup
- Container Apps environment creation
- App deployment for each configuration
- Built-in load balancer configuration
- Scaling rules

## Configuration Matrix

The experiments evaluate 10 configurations across both platforms:

### AWS Configurations
- **B1 (Baseline)**: 1 replica, 1 worker, 4 vCPU, 8GB RAM
- **WS1**: 1 replica, 2 workers, 4 vCPU, 8GB RAM
- **WS2**: 1 replica, 4 workers, 4 vCPU, 8GB RAM
- **HS1**: 2 replicas, 1 worker each, 4 vCPU, 8GB RAM (with ALB)
- **HS2**: 4 replicas, 1 worker each, 4 vCPU, 8GB RAM (with ALB)

### Azure Configurations
- **B2 (Baseline)**: 1 replica, 1 worker, 4 vCPU, 8GB RAM
- **WS3**: 1 replica, 2 workers, 4 vCPU, 8GB RAM
- **WS4**: 1 replica, 4 workers, 4 vCPU, 8GB RAM
- **HS3**: 2 replicas, 1 worker each, 4 vCPU, 8GB RAM
- **HS4**: 4 replicas, 1 worker each, 4 vCPU, 8GB RAM

## Environment Variables

### Backend API

- `WORKERS`: Number of Gunicorn worker processes (default: 1)
- `HOST`: Bind address (default: 0.0.0.0)
- `PORT`: Port number (default: 8000)
- `HF_MODEL`: Hugging Face model identifier (default: Salesforce/blip-image-captioning-base)

### Thread Limiting (Critical for Multi-Worker Deployments)

The backend automatically configures thread limits based on the `WORKERS` environment variable:
- **1 worker**: Uses all available vCPUs (default PyTorch behavior)
- **2+ workers**: Dynamically allocates `vCPUs / workers` threads per worker

This prevents thread oversubscription (e.g., 4 workers × 4 threads = 16 threads on 4 vCPUs).

Environment variables set automatically by `app.py`:
- `OMP_NUM_THREADS`
- `MKL_NUM_THREADS`
- `OPENBLAS_NUM_THREADS`
- `NUMEXPR_NUM_THREADS`

## Testing Protocol

### Dataset Preparation

1. Download 300 unique images from Pexels:
   - 100 medium-resolution (12MP)
   - 200 high-resolution (24MP)
   
2. Upload images using the frontend's image uploader

### Experiment Execution

1. Configure API endpoints in the frontend:
   - AWS endpoint: `http://<aws-alb-dns>/api`
   - Azure endpoint: `https://<azure-app-name>.azurewebsites.net/api`

2. Load all 300 images in browser memory

3. Run test with 300 iterations:
   - Frontend submits all 300 requests concurrently
   - Measures response time for each request
   - Records success/failure status

4. Repeat experiment 3 times for each configuration

5. Export results to CSV for analysis

### Metrics Collected

For each request:
- Response time (milliseconds)
- Status code
- Success/failure
- Caption generated
- Timestamp
- Provider identifier

Aggregated metrics:
- Average response time
- Standard deviation
- Min/Max response time
- Median response time
- Success rate

## License

MIT License - See individual repositories for details.

## Citation

If you use this infrastructure for your research, please cite:

```
@mastersthesis{holanda2025aws,
  author = {Dordenoni Holanda, Carlos Abraão; Depes Bilharinho, Natan; Martins de Jesus, Gabriela},
  title = {AWS vs Azure Performance Comparison for CPU-Intensive Transformer-Based Inference: A Controlled Experimental Study},
  school = {[Universidade Vila Velha]},
  year = {2025}
}
```

## Support

For questions or issues:
- Backend API: https://github.com/TheAbraaonix/tcc_high_availability_api/issues
- Frontend: https://github.com/TheAbraaonix/tcc_high_availability_front/issues
