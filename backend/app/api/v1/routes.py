"""API v1 routes."""

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
