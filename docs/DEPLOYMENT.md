# Deployment Guide

## Local Development

### Prerequisites
- Python 3.12+ with pip or Poetry
- Node.js 18+ with npm or yarn
- PostgreSQL 15+
- Docker and Docker Compose (optional but recommended)

### Without Docker

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Install dependencies
poetry install
# OR
pip install -r requirements.txt

# Create environment file
cp ../.env.example .env

# Edit .env with your settings
nano .env

# Initialize database
createdb catalog_db

# Run migrations (when available)
poetry run alembic upgrade head

# Seed demo data
poetry run python seed_data.py

# Start server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup (in another terminal)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:5173
```

### With Docker Compose

```bash
# From project root
cp .env.example .env

# Start all services
docker compose up --build

# Services:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:5173
# - Postgres: localhost:5432
# - API Docs: http://localhost:8000/api/docs

# View logs
docker compose logs -f

# Stop services
docker compose down

# Clean up volumes
docker compose down -v
```

---

## Production Deployment

### 1. Database Setup

#### AWS RDS PostgreSQL
```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier catalog-prod \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 15.4 \
  --master-username admin \
  --allocated-storage 100 \
  --backup-retention-period 30 \
  --enable-cloudwatch-logs-exports postgresql

# Get endpoint
ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier catalog-prod \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text)

echo "Database Endpoint: $ENDPOINT"
```

#### Database Initialization
```bash
# Connect to database
psql -h $ENDPOINT -U admin -d postgres

# Create application database
CREATE DATABASE catalog_prod;
CREATE ROLE catalog_app WITH LOGIN PASSWORD 'strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE catalog_prod TO catalog_app;

# Exit psql
\q
```

#### Run Migrations
```bash
# In backend directory
poetry run alembic upgrade head --database-url \
  postgresql://catalog_app:password@endpoint:5432/catalog_prod
```

### 2. Backend Deployment

#### Azure App Service
```bash
# Prerequisites: Azure CLI installed
az login

# Create resource group
az group create \
  --name data-governance-rg \
  --location eastus

# Create App Service Plan
az appservice plan create \
  --name governance-plan \
  --resource-group data-governance-rg \
  --sku B2 \
  --is-linux

# Create App Service
az webapp create \
  --resource-group data-governance-rg \
  --plan governance-plan \
  --name governance-api-prod \
  --runtime "PYTHON|3.12"

# Configure environment variables
az webapp config appsettings set \
  --resource-group data-governance-rg \
  --name governance-api-prod \
  --settings \
    DATABASE_URL="postgresql://..." \
    JWT_SECRET_KEY="long-random-string" \
    ENVIRONMENT="production" \
    CORS_ORIGINS="https://governance.example.com"

# Deploy from Git (or use ZIP deployment)
az webapp up --resource-group data-governance-rg \
  --name governance-api-prod \
  --location eastus
```

#### AWS ECS Fargate
```bash
# Build and push Docker image
aws ecr create-repository --repository-name governance-api

docker build -t governance-api:latest backend/
docker tag governance-api:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/governance-api:latest

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/governance-api:latest

# Create ECS cluster, task definition, service
# (See infrastructure-as-code section below)
```

### 3. Frontend Deployment

#### Azure Static Web Apps
```bash
# Build frontend
npm run build

# Deploy to Azure Static Web Apps
az staticwebapp create \
  --name governance-portal \
  --resource-group data-governance-rg \
  --source https://github.com/SriChaitanya1824/Enterprise-Data-Catalog... \
  --branch main \
  --login-with-github

# Update API endpoint in environment
echo "VITE_API_URL=https://governance-api-prod.azurewebsites.net" > .env.production
```

#### AWS S3 + CloudFront
```bash
# Create S3 bucket
aws s3 mb s3://governance-portal-prod --region us-east-1

# Build and upload
npm run build
aws s3 sync dist/ s3://governance-portal-prod --delete

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name governance-portal-prod.s3.amazonaws.com \
  --default-root-object index.html

# Update API endpoint
echo "VITE_API_URL=https://governance-api.example.com" > .env.production
```

### 4. Airflow Orchestration Deployment

#### Managed Airflow (AWS MWAA)
```bash
# Create S3 bucket for DAGs and logs
aws s3 mb s3://governance-airflow-prod

# Upload DAGs
aws s3 cp airflow/dags/ s3://governance-airflow-prod/dags/ --recursive

# Create Airflow environment
aws mwaa create-environment \
  --name governance-metadata-prod \
  --airflow-version 2.7 \
  --execution-role-arn arn:aws:iam::...:role/mwaa-role \
  --dag-s3-path s3://governance-airflow-prod/dags \
  --environment-class mw1.small
```

#### Kubernetes Deployment
```bash
# Create namespace
kubectl create namespace governance

# Create ConfigMap for DAGs
kubectl create configmap airflow-dags \
  --from-file=airflow/dags/ \
  -n governance

# Deploy Airflow Helm chart
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow \
  --namespace governance \
  --values airflow-values.yaml

# Verify deployment
kubectl get pods -n governance
kubectl logs -f deployment/airflow-scheduler -n governance
```

### 5. Infrastructure as Code

#### Terraform Example
```hcl
# main.tf - Azure Deployment

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "governance" {
  name     = "data-governance-prod"
  location = "East US"
}

# App Service Plan
resource "azurerm_service_plan" "governance" {
  name                = "governance-plan"
  resource_group_name = azurerm_resource_group.governance.name
  location            = azurerm_resource_group.governance.location
  os_type             = "Linux"
  sku_name            = "B2"
}

# App Service (Backend)
resource "azurerm_linux_web_app" "backend" {
  name                = "governance-api-prod"
  resource_group_name = azurerm_resource_group.governance.name
  location            = azurerm_resource_group.governance.location
  service_plan_id     = azurerm_service_plan.governance.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    DATABASE_URL      = azurerm_postgresql_server.governance.connection_string
    JWT_SECRET_KEY    = random_password.jwt_secret.result
    ENVIRONMENT       = "production"
  }

  https_only = true
}

# PostgreSQL Database
resource "azurerm_postgresql_server" "governance" {
  name                = "governance-db-prod"
  location            = azurerm_resource_group.governance.location
  resource_group_name = azurerm_resource_group.governance.name

  administrator_login          = "pgadmin"
  administrator_login_password = random_password.db_password.result

  sku_name   = "B_Gen5_2"
  version    = "15"
  storage_mb = 102400

  backup_retention_days        = 30
  geo_redundant_backup_enabled = true
  ssl_enforcement_enabled      = true
}

# Static Web App (Frontend)
resource "azurerm_static_web_app" "frontend" {
  name                = "governance-portal-prod"
  resource_group_name = azurerm_resource_group.governance.name
  location            = azurerm_resource_group.governance.location

  sku_tier = "Standard"
  sku_size = "Standard"
}

# Application Insights
resource "azurerm_application_insights" "governance" {
  name                = "governance-insights"
  location            = azurerm_resource_group.governance.location
  resource_group_name = azurerm_resource_group.governance.name
  application_type    = "web"
}

# Random Passwords
resource "random_password" "jwt_secret" {
  length  = 32
  special = true
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Outputs
output "backend_url" {
  value = azurerm_linux_web_app.backend.default_hostname
}

output "frontend_url" {
  value = azurerm_static_web_app.frontend.default_host_name
}

output "database_host" {
  value = azurerm_postgresql_server.governance.fqdn
}
```

#### Bicep Example
```bicep
// main.bicep - Azure Deployment

param location string = resourceGroup().location
param environment string = 'prod'

var resourceNamePrefix = 'governance-${environment}'

// App Service Plan
resource servicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${resourceNamePrefix}-plan'
  location: location
  sku: {
    name: 'B2'
    tier: 'Basic'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Backend App Service
resource backendApp 'Microsoft.Web/sites@2022-03-01' = {
  name: '${resourceNamePrefix}-api'
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: servicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      alwaysOn: true
      http20Enabled: true
    }
    httpsOnly: true
  }
}

// PostgreSQL Server
resource postgresqlServer 'Microsoft.DBforPostgreSQL/servers@2017-12-01' = {
  name: '${resourceNamePrefix}-db'
  location: location
  sku: {
    name: 'B_Gen5_2'
    tier: 'Basic'
    capacity: 2
    family: 'Gen5'
  }
  properties: {
    createMode: 'Default'
    version: '15'
    administratorLogin: 'pgadmin'
    administratorLoginPassword: 'ChangeMe!2024'
    backupRetentionDays: 30
    geoRedundantBackup: 'Enabled'
    sslEnforcement: 'ENABLED'
  }
}
```

### 6. Security Configuration

#### SSL/TLS Certificates
```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone \
  -d governance.example.com \
  -d api.governance.example.com

# Import certificate to cloud provider
az webapp config ssl upload \
  --resource-group data-governance-rg \
  --name governance-api-prod \
  --certificate-file /etc/letsencrypt/live/.../fullchain.pem
```

#### Network Security
```bash
# Configure network security group (Azure)
az network nsg create \
  --resource-group data-governance-rg \
  --name governance-nsg

# Allow HTTPS only
az network nsg rule create \
  --resource-group data-governance-rg \
  --nsg-name governance-nsg \
  --name AllowHTTPS \
  --priority 100 \
  --direction Inbound \
  --protocol Tcp \
  --source-port-ranges '*' \
  --destination-port-ranges 443 \
  --access Allow

# Deny HTTP
az network nsg rule create \
  --resource-group data-governance-rg \
  --nsg-name governance-nsg \
  --name DenyHTTP \
  --priority 200 \
  --direction Inbound \
  --protocol Tcp \
  --source-port-ranges '*' \
  --destination-port-ranges 80 \
  --access Deny
```

#### Database Authentication
```bash
# Enable managed identity for App Service
az webapp identity assign \
  --resource-group data-governance-rg \
  --name governance-api-prod

# Grant database permissions
# In PostgreSQL:
CREATE USER "governance-api-prod" WITH PASSWORD 'oauth_token';
GRANT CONNECT ON DATABASE catalog_prod TO "governance-api-prod";
GRANT USAGE ON SCHEMA public TO "governance-api-prod";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "governance-api-prod";
```

### 7. Monitoring & Logging

#### Application Performance
```bash
# Enable Application Insights
az webapp config set \
  --resource-group data-governance-rg \
  --name governance-api-prod \
  --use-32bit-worker-process false

# Configure logging
az webapp log config \
  --resource-group data-governance-rg \
  --name governance-api-prod \
  --application-logging true \
  --detailed-error-messages true
```

#### Log Analytics
```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group data-governance-rg \
  --workspace-name governance-logs

# Connect App Service to Log Analytics
az monitor diagnostics-settings create \
  --resource /subscriptions/{id}/resourceGroups/governance-rg/providers/Microsoft.Web/sites/governance-api-prod \
  --workspace /subscriptions/{id}/resourceGroups/governance-rg/providers/microsoft.operationalinsights/workspaces/governance-logs \
  --metrics "[{category:'AllMetrics',enabled:true}]" \
  --logs "[{category:'AppServiceHTTPLogs',enabled:true}]"
```

#### Alerting
```bash
# Create alert for high CPU
az monitor metrics alert create \
  --resource-group data-governance-rg \
  --name governance-api-high-cpu \
  --scopes /subscriptions/{id}/resourceGroups/governance-rg/providers/Microsoft.Web/sites/governance-api-prod \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m
```

---

## Backup & Disaster Recovery

### Database Backups
```bash
# Azure Automated backups (configured in Terraform)
# Retention: 30 days

# Manual backup
az postgres server backup create \
  --resource-group data-governance-rg \
  --server-name governance-db-prod \
  --backup-name pre-migration-backup
```

### Point-in-Time Restore
```bash
# Restore to specific point in time
az postgres server restore \
  --resource-group data-governance-rg \
  --name governance-db-restored \
  --source-server governance-db-prod \
  --restore-point-in-time "2024-10-15T14:00:00Z"
```

---

## Maintenance & Operations

### Regular Tasks
- **Daily**: Monitor application logs and alerts
- **Weekly**: Review assessment metrics and gaps
- **Monthly**: Database backups, certificate expiry checks
- **Quarterly**: Security patches, dependency updates
- **Annual**: Capacity planning, cost optimization

### Database Maintenance
```bash
# Vacuum and analyze
psql -h $ENDPOINT -U admin -d catalog_prod -c "VACUUM ANALYZE;"

# Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Update Procedures
```bash
# Backend update
az webapp deployment source config-zip \
  --resource-group data-governance-rg \
  --name governance-api-prod \
  --src deployment.zip

# Frontend update
npm run build
az storage blob upload-batch \
  --account-name govportal \
  --source dist \
  --destination '$web' \
  --overwrite
```

---

**Deployment Guide Version**: 1.0  
**Last Updated**: October 2, 2026  
**Maintained By**: Platform Engineering Team
