"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# User Schemas
# ============================================================================


class UserCreate(BaseModel):
    """Create user request."""

    email: EmailStr
    full_name: str
    password: str
    role: str


class UserResponse(BaseModel):
    """User response."""

    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"


# ============================================================================
# Domain and Division Schemas
# ============================================================================


class BusinessDomainCreate(BaseModel):
    """Create business domain request."""

    name: str
    description: Optional[str] = None
    business_owner_id: Optional[int] = None


class BusinessDomainResponse(BaseModel):
    """Business domain response."""

    id: int
    name: str
    description: Optional[str]
    business_owner_id: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BusinessDivisionCreate(BaseModel):
    """Create business division request."""

    name: str
    description: Optional[str] = None
    domain_id: Optional[int] = None


class BusinessDivisionResponse(BaseModel):
    """Business division response."""

    id: int
    name: str
    description: Optional[str]
    domain_id: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Data Asset Schemas
# ============================================================================


class DataFieldCreate(BaseModel):
    """Create data field request."""

    name: str
    display_name: str
    description: Optional[str] = None
    data_type: str
    is_nullable: bool = True
    is_cde: bool = False
    classification: str = "Internal"
    sensitivity: str = "Non-Sensitive"
    business_term_id: Optional[int] = None
    regulatory_tag: Optional[str] = None


class DataFieldUpdate(BaseModel):
    """Update data field request."""

    display_name: Optional[str] = None
    description: Optional[str] = None
    is_cde: Optional[bool] = None
    classification: Optional[str] = None
    sensitivity: Optional[str] = None
    business_term_id: Optional[int] = None
    regulatory_tag: Optional[str] = None


class DataFieldResponse(BaseModel):
    """Data field response."""

    id: int
    name: str
    display_name: str
    description: Optional[str]
    data_type: str
    is_nullable: bool
    is_cde: bool
    classification: str
    sensitivity: str
    business_term_id: Optional[int]
    regulatory_tag: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DataAssetCreate(BaseModel):
    """Create data asset request."""

    name: str
    display_name: str
    description: Optional[str] = None
    asset_type: str
    source_system: Optional[str] = None
    physical_location: Optional[str] = None
    business_domain_id: Optional[int] = None
    business_division_id: Optional[int] = None
    owner_id: Optional[int] = None
    steward_id: Optional[int] = None
    classification: str = "Internal"
    criticality: str = "Medium"
    regulatory_relevance: bool = False
    lifecycle_status: str = "Active"


class DataAssetUpdate(BaseModel):
    """Update data asset request."""

    display_name: Optional[str] = None
    description: Optional[str] = None
    asset_type: Optional[str] = None
    source_system: Optional[str] = None
    physical_location: Optional[str] = None
    business_domain_id: Optional[int] = None
    business_division_id: Optional[int] = None
    owner_id: Optional[int] = None
    steward_id: Optional[int] = None
    classification: Optional[str] = None
    criticality: Optional[str] = None
    regulatory_relevance: Optional[bool] = None
    lifecycle_status: Optional[str] = None
    next_review_date: Optional[datetime] = None


class DataAssetResponse(BaseModel):
    """Data asset response."""

    id: int
    name: str
    display_name: str
    description: Optional[str]
    asset_type: str
    source_system: Optional[str]
    physical_location: Optional[str]
    business_domain_id: Optional[int]
    business_division_id: Optional[int]
    owner_id: Optional[int]
    steward_id: Optional[int]
    classification: str
    criticality: str
    regulatory_relevance: bool
    lifecycle_status: str
    certification_status: str
    metadata_completeness: float
    lineage_completeness: float
    last_reviewed_at: Optional[datetime]
    next_review_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class DataAssetDetailResponse(DataAssetResponse):
    """Data asset with full details."""

    fields: list[DataFieldResponse] = []


# ============================================================================
# Business Glossary Schemas
# ============================================================================


class BusinessTermCreate(BaseModel):
    """Create business term request."""

    term: str
    definition: str
    abbreviation: Optional[str] = None
    domain_id: Optional[int] = None
    owner: Optional[str] = None
    steward: Optional[str] = None


class BusinessTermUpdate(BaseModel):
    """Update business term request."""

    definition: Optional[str] = None
    abbreviation: Optional[str] = None
    domain_id: Optional[int] = None
    owner: Optional[str] = None
    steward: Optional[str] = None
    status: Optional[str] = None
    approval_status: Optional[str] = None


class BusinessTermResponse(BaseModel):
    """Business term response."""

    id: int
    term: str
    definition: str
    abbreviation: Optional[str]
    domain_id: Optional[int]
    owner: Optional[str]
    steward: Optional[str]
    status: str
    approval_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Governance Assessment Schemas
# ============================================================================


class GovernanceAssessmentResponse(BaseModel):
    """Governance assessment response."""

    id: int
    asset_id: int
    executed_at: datetime
    executed_by_id: Optional[int]
    score: float
    maturity_level: str
    requirements_checked: int
    requirements_passed: int
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentResultResponse(BaseModel):
    """Assessment result response."""

    id: int
    requirement_id: int
    passed: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


# ============================================================================
# Governance Gap Schemas
# ============================================================================


class GovernanceGapCreate(BaseModel):
    """Create governance gap request."""

    asset_id: int
    requirement_id: int
    data_field_id: Optional[int] = None
    category: str
    severity: str
    description: str
    status: str = "Open"


class GovernanceGapUpdate(BaseModel):
    """Update governance gap request."""

    status: Optional[str] = None
    resolution_notes: Optional[str] = None


class GovernanceGapResponse(BaseModel):
    """Governance gap response."""

    id: int
    asset_id: int
    requirement_id: int
    data_field_id: Optional[int]
    category: str
    severity: str
    description: str
    status: str
    detected_at: datetime
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]

    class Config:
        from_attributes = True


# ============================================================================
# Certification and Review Schemas
# ============================================================================


class CertificationResponse(BaseModel):
    """Certification response."""

    id: int
    asset_id: int
    status: str
    certified_by_id: Optional[int]
    certified_at: Optional[datetime]
    expires_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    """Create review request."""

    asset_id: int
    outcome: str
    notes: Optional[str] = None
    next_review_date: Optional[datetime] = None


class ReviewResponse(BaseModel):
    """Review response."""

    id: int
    asset_id: int
    reviewer_id: int
    review_date: datetime
    outcome: str
    notes: Optional[str]
    next_review_date: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================================
# Dashboard Schemas
# ============================================================================


class DashboardMetricsResponse(BaseModel):
    """Dashboard metrics response."""

    total_assets: int
    critical_assets: int
    cdes: int
    certified_assets: int
    assets_requiring_review: int
    assets_missing_owners: int
    assets_missing_stewards: int
    assets_missing_classification: int
    assets_missing_lineage: int
    assets_with_governance_gaps: int
    average_metadata_completeness: float
    average_governance_completeness: float


class DivisionAdoptionResponse(BaseModel):
    """Division adoption metrics response."""

    division_id: int
    division_name: str
    assets_registered: int
    assets_with_owners: int
    assets_with_stewards: int
    assets_with_descriptions: int
    assets_with_classifications: int
    assets_with_regulatory_mappings: int
    assets_with_lineage: int
    assets_with_approved_definitions: int
    assets_reviewed_on_time: int
    average_governance_completeness: float


# ============================================================================
# Search Schemas
# ============================================================================


class SearchResultsResponse(BaseModel):
    """Search results response."""

    assets: list[DataAssetResponse] = []
    fields: list[DataFieldResponse] = []
    terms: list[BusinessTermResponse] = []
    domains: list[BusinessDomainResponse] = []
