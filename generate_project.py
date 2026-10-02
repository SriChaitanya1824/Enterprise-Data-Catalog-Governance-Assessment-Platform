#!/usr/bin/env python3
"""
Complete Enterprise Data Catalog implementation.
This script generates all necessary files for the project.
"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE = Path("/Users/jyothi/Desktop/CODe/DeutchBank/3")

def write_file(path, content):
    """Write content to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ {path.relative_to(BASE)}")

# ==============================================================================
# CORE BACKEND FILES
# ==============================================================================

# Create __init__ files
for pkg in [
    "backend/app",
    "backend/app/core",
    "backend/app/api/v1",
    "backend/app/repositories",
    "backend/app/services",
    "backend/app/catalog",
    "backend/app/glossary",
    "backend/app/lineage",
    "backend/app/assessment",
    "backend/app/certification",
    "backend/tests",
]:
    write_file(BASE / pkg / "__init__.py", "")

# ==============================================================================
# CORE SERVICES
# ==============================================================================

assessment_service = '''"""Governance assessment service."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models import (
    DataAsset, GovernanceAssessment, GovernanceRequirement,
    AssessmentResult, GovernanceGap, DataField, Review,
    BusinessTerm, RegulatoryReference, AssetRegulatoryMapping
)


class GovernanceAssessmentService:
    """Service for governance assessment."""

    def __init__(self, db: AsyncSession):
        """Initialize service."""
        self.db = db

    async def assess_asset(self, asset_id: int, user_id: int) -> dict:
        """Run governance assessment for an asset."""
        # Fetch asset
        result = await self.db.execute(
            select(DataAsset).where(DataAsset.id == asset_id)
        )
        asset = result.scalar_one_or_none()
        if not asset:
            return {"error": "Asset not found"}

        # Evaluate requirements
        requirements_result = await self.db.execute(
            select(GovernanceRequirement).where(
                GovernanceRequirement.is_mandatory == True
            )
        )
        requirements = requirements_result.scalars().all()

        assessment_results = []
        passed_count = 0

        for req in requirements:
            passed = await self._evaluate_requirement(asset, req)
            assessment_results.append({
                "requirement_id": req.id,
                "passed": passed
            })
            if passed:
                passed_count += 1

        # Calculate score
        total_reqs = len(requirements)
        score = (passed_count / total_reqs * 100) if total_reqs > 0 else 0
        maturity = self._calculate_maturity(score)

        # Save assessment
        assessment = GovernanceAssessment(
            asset_id=asset_id,
            executed_by_id=user_id,
            score=score,
            maturity_level=maturity,
            requirements_checked=total_reqs,
            requirements_passed=passed_count
        )
        self.db.add(assessment)
        await self.db.flush()

        # Save results
        for result_data in assessment_results:
            result = AssessmentResult(
                assessment_id=assessment.id,
                requirement_id=result_data["requirement_id"],
                passed=result_data["passed"]
            )
            self.db.add(result)

        # Detect gaps
        await self._detect_gaps(asset, requirements, assessment_results)

        await self.db.commit()
        
        return {
            "id": assessment.id,
            "score": round(score, 2),
            "maturity": maturity,
            "requirements_checked": total_reqs,
            "requirements_passed": passed_count
        }

    async def _evaluate_requirement(self, asset: DataAsset, req: GovernanceRequirement) -> bool:
        """Evaluate if asset meets requirement."""
        if req.code == "GOV-001":  # Owner
            return asset.owner_id is not None
        elif req.code == "GOV-002":  # Steward
            return asset.steward_id is not None
        elif req.code == "GOV-003":  # Description
            return bool(asset.description and len(asset.description) > 10)
        elif req.code == "GOV-004":  # Classification
            return asset.classification is not None
        elif req.code == "GOV-005":  # CDE definition
            # Check if asset has CDEs and they have business terms
            cde_fields = await self.db.execute(
                select(DataField).where(
                    and_(
                        DataField.data_asset_id == asset.id,
                        DataField.is_cde == True
                    )
                )
            )
            fields = cde_fields.scalars().all()
            if not fields:
                return True  # No CDEs, requirement not applicable
            return all(f.business_term_id for f in fields)
        elif req.code == "GOV-006":  # Regulatory mapping
            if not asset.regulatory_relevance:
                return True  # Not applicable
            result = await self.db.execute(
                select(AssetRegulatoryMapping).where(
                    AssetRegulatoryMapping.asset_id == asset.id
                )
            )
            return result.scalar_one_or_none() is not None
        elif req.code == "GOV-007":  # Lineage
            return asset.lineage_completeness >= 50
        elif req.code == "GOV-008":  # Review date
            return asset.next_review_date is not None
        return False

    def _calculate_maturity(self, score: float) -> str:
        """Calculate maturity level based on score."""
        if score >= 95:
            return "Optimized"
        elif score >= 85:
            return "Managed"
        elif score >= 70:
            return "Defined"
        elif score >= 50:
            return "Developing"
        else:
            return "Initial"

    async def _detect_gaps(
        self, asset: DataAsset, requirements: list, results: list
    ) -> None:
        """Detect and record governance gaps."""
        for i, req in enumerate(requirements):
            if not results[i]["passed"]:
                # Determine gap details
                category, severity = self._get_gap_details(req)
                
                gap = GovernanceGap(
                    asset_id=asset.id,
                    requirement_id=req.id,
                    category=category,
                    severity=severity,
                    description=f"Requirement '{req.name}' not met"
                )
                self.db.add(gap)

    def _get_gap_details(self, req: GovernanceRequirement) -> tuple:
        """Determine gap category and severity."""
        categories = {
            "GOV-001": ("Accountability", "High"),
            "GOV-002": ("Accountability", "High"),
            "GOV-003": ("Metadata", "Medium"),
            "GOV-004": ("Classification", "High"),
            "GOV-005": ("Business Context", "Medium"),
            "GOV-006": ("Regulatory", "High"),
            "GOV-007": ("Traceability", "Medium"),
            "GOV-008": ("Review", "Medium"),
        }
        return categories.get(req.code, ("Other", "Low"))

    async def get_assessment_history(self, asset_id: int, limit: int = 10) -> list:
        """Get assessment history for an asset."""
        result = await self.db.execute(
            select(GovernanceAssessment)
            .where(GovernanceAssessment.asset_id == asset_id)
            .order_by(GovernanceAssessment.executed_at.desc())
            .limit(limit)
        )
        assessments = result.scalars().all()
        return [
            {
                "executed_at": a.executed_at,
                "score": a.score,
                "maturity": a.maturity_level
            }
            for a in assessments
        ]
'''

write_file(BASE / "backend/app/assessment/service.py", assessment_service)

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

main_app = '''"""FastAPI application entry point."""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db, Base, engine
from app.api.v1 import router as v1_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(v1_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }
'''

write_file(BASE / "backend/app/main.py", main_app)

# ==============================================================================
# API ROUTES
# ==============================================================================

api_v1_routes = '''"""API v1 routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models import DataAsset, BusinessDomain, BusinessDivision, BusinessTerm
from app.schemas import (
    DataAssetResponse, BusinessDomainResponse, BusinessDivisionResponse,
    DashboardMetricsResponse, SearchResultsResponse
)
from app.assessment.service import GovernanceAssessmentService

router = APIRouter()

# ==============================================================================
# Health & Status
# ==============================================================================

@router.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}

# ==============================================================================
# Data Assets
# ==============================================================================

@router.get("/assets", response_model=list[DataAssetResponse])
async def list_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    domain_id: int = Query(None),
    classification: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List data assets with filtering."""
    query = select(DataAsset)
    
    if domain_id:
        query = query.where(DataAsset.business_domain_id == domain_id)
    if classification:
        query = query.where(DataAsset.classification == classification)
    
    result = await db.execute(
        query.offset(skip).limit(limit)
    )
    assets = result.scalars().all()
    return assets

@router.get("/assets/{asset_id}", response_model=DataAssetResponse)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    """Get asset by ID."""
    result = await db.execute(
        select(DataAsset).where(DataAsset.id == asset_id)
    )
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# ==============================================================================
# Governance Assessment
# ==============================================================================

@router.post("/assessments/run/{asset_id}")
async def run_assessment(
    asset_id: int,
    user_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Run governance assessment for an asset."""
    service = GovernanceAssessmentService(db)
    return await service.assess_asset(asset_id, user_id)

@router.get("/assessments/{asset_id}/history")
async def get_assessment_history(
    asset_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get assessment history for an asset."""
    service = GovernanceAssessmentService(db)
    return await service.get_assessment_history(asset_id)

# ==============================================================================
# Dashboard
# ==============================================================================

@router.get("/dashboard/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db)):
    """Get dashboard metrics."""
    # Calculate metrics from database
    assets_result = await db.execute(select(DataAsset))
    all_assets = assets_result.scalars().all()
    
    total = len(all_assets)
    critical = len([a for a in all_assets if a.criticality == "Critical"])
    certified = len([a for a in all_assets if a.certification_status == "Certified"])
    
    avg_governance = (
        sum(a.metadata_completeness for a in all_assets) / total
        if total > 0 else 0
    )
    
    return DashboardMetricsResponse(
        total_assets=total,
        critical_assets=critical,
        cdes=len([a for a in all_assets for f in a.fields if f.is_cde]),
        certified_assets=certified,
        assets_requiring_review=len([a for a in all_assets if not a.last_reviewed_at]),
        assets_missing_owners=len([a for a in all_assets if not a.owner_id]),
        assets_missing_stewards=len([a for a in all_assets if not a.steward_id]),
        assets_missing_classification=0,
        assets_missing_lineage=len([a for a in all_assets if a.lineage_completeness < 50]),
        assets_with_governance_gaps=len([
            a for a in all_assets 
            for g in a.gaps if g.status == "Open"
        ]),
        average_metadata_completeness=avg_governance,
        average_governance_completeness=avg_governance
    )

# ==============================================================================
# Search
# ==============================================================================

@router.get("/search", response_model=SearchResultsResponse)
async def global_search(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    """Global search across catalog."""
    search_term = f"%{q}%"
    
    # Search assets
    assets_result = await db.execute(
        select(DataAsset).where(
            (DataAsset.name.ilike(search_term)) |
            (DataAsset.display_name.ilike(search_term))
        ).limit(5)
    )
    assets = assets_result.scalars().all()
    
    # Search terms
    terms_result = await db.execute(
        select(BusinessTerm).where(
            BusinessTerm.term.ilike(search_term)
        ).limit(5)
    )
    terms = terms_result.scalars().all()
    
    return SearchResultsResponse(
        assets=assets,
        fields=[],
        terms=terms,
        domains=[]
    )

# ==============================================================================
# Business Domains
# ==============================================================================

@router.get("/domains", response_model=list[BusinessDomainResponse])
async def list_domains(db: AsyncSession = Depends(get_db)):
    """List business domains."""
    result = await db.execute(select(BusinessDomain).where(BusinessDomain.is_active == True))
    return result.scalars().all()

# ==============================================================================
# Business Divisions
# ==============================================================================

@router.get("/divisions", response_model=list[BusinessDivisionResponse])
async def list_divisions(db: AsyncSession = Depends(get_db)):
    """List business divisions."""
    result = await db.execute(select(BusinessDivision).where(BusinessDivision.is_active == True))
    return result.scalars().all()

# ==============================================================================
# Business Glossary
# ==============================================================================

@router.get("/glossary", response_model=list[dict])
async def list_glossary(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List business glossary terms."""
    result = await db.execute(
        select(BusinessTerm)
        .order_by(BusinessTerm.term)
        .offset(skip)
        .limit(limit)
    )
    terms = result.scalars().all()
    return [
        {
            "id": t.id,
            "term": t.term,
            "definition": t.definition,
            "status": t.status,
            "domain_id": t.domain_id
        }
        for t in terms
    ]
'''

write_file(BASE / "backend/app/api/v1/__init__.py", "from fastapi import APIRouter\nrouter = APIRouter()")
write_file(BASE / "backend/app/api/v1/routes.py", api_v1_routes)

# Update __init__.py to export router
write_file(BASE / "backend/app/api/v1/__init__.py", """from fastapi import APIRouter
from app.api.v1.routes import router

__all__ = ["router"]
""")

# ==============================================================================
# ENV FILE
# ==============================================================================

env_example = '''DATABASE_URL=postgresql://postgres:postgres@localhost:5432/catalog_db
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
OPENLINEAGE_URL=http://localhost:5000
MARQUEZ_URL=http://localhost:3000
APP_NAME=Enterprise Data Catalog & Governance Platform
APP_VERSION=1.0.0
DEBUG=False
'''

write_file(BASE / ".env.example", env_example)

# ==============================================================================
# DOCKER COMPOSE
# ==============================================================================

docker_compose = '''version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: catalog_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: catalog_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    container_name: catalog_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/catalog_db
      JWT_SECRET: your-secret-key
      CORS_ORIGINS: '["http://localhost:5173", "http://localhost:3000"]'
      DEBUG: "False"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    container_name: catalog_frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
'''

write_file(BASE / "docker-compose.yml", docker_compose)

# ==============================================================================
# DOCKERFILE FOR BACKEND
# ==============================================================================

backend_dockerfile = '''FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --no-interaction --no-ansi

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

write_file(BASE / "Dockerfile.backend", backend_dockerfile)

# ==============================================================================
# MAKEFILE
# ==============================================================================

makefile = '''
.PHONY: install dev test lint format clean docker-up docker-down

# Development
install:
	cd backend && poetry install
	cd frontend && npm install

dev:
	docker compose up --build

# Testing
test:
	cd backend && pytest tests/ -v --cov=app

# Code quality
lint:
	cd backend && ruff check .
	cd backend && mypy app/

format:
	cd backend && black . && ruff check . --fix
	cd frontend && npx prettier --write src/

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f backend

# Database
db-init:
	cd backend && alembic upgrade head

db-reset:
	cd backend && alembic downgrade base && alembic upgrade head

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

help:
	@echo "Available commands:"
	@grep -E "^\\S+:" Makefile | head -20
'''

write_file(BASE / "Makefile", makefile)

print("\\n✅ Backend implementation files created successfully!")

if __name__ == "__main__":
    print("Enterprise Data Catalog scaffolding complete!")
