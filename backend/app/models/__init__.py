"""SQLAlchemy models for the enterprise data catalog."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ============================================================================
# Enums
# ============================================================================


class AssetTypeEnum(str, Enum):
    """Asset types."""

    DATABASE_TABLE = "Database Table"
    VIEW = "View"
    DATASET = "Dataset"
    FILE = "File"
    API = "API"
    REPORT = "Report"
    DATA_PRODUCT = "Data Product"
    MESSAGE_STREAM = "Message Stream"


class ClassificationEnum(str, Enum):
    """Data classification levels."""

    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class SensitivityEnum(str, Enum):
    """Field sensitivity levels."""

    NON_SENSITIVE = "Non-Sensitive"
    SENSITIVE = "Sensitive"
    HIGHLY_SENSITIVE = "Highly Sensitive"


class LifecycleStatusEnum(str, Enum):
    """Asset lifecycle status."""

    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"
    UNDER_REVIEW = "Under Review"


class CertificationStatusEnum(str, Enum):
    """Asset certification status."""

    NOT_REVIEWED = "Not Reviewed"
    IN_REVIEW = "In Review"
    CERTIFIED = "Certified"
    CERTIFIED_WITH_CONDITIONS = "Certified With Conditions"
    CERTIFICATION_EXPIRED = "Certification Expired"


class UserRoleEnum(str, Enum):
    """User roles."""

    ADMIN = "ADMIN"
    GOVERNANCE_ANALYST = "GOVERNANCE_ANALYST"
    DATA_OWNER = "DATA_OWNER"
    DATA_STEWARD = "DATA_STEWARD"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    VIEWER = "VIEWER"


class ReviewOutcomeEnum(str, Enum):
    """Review outcomes."""

    CERTIFIED = "Certified"
    CERTIFIED_WITH_CONDITIONS = "Certified With Conditions"
    NOT_CERTIFIED = "Not Certified"


class GapStatusEnum(str, Enum):
    """Governance gap status."""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    WAIVED = "Waived"


class GapSeverityEnum(str, Enum):
    """Governance gap severity."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TermStatusEnum(str, Enum):
    """Business term status."""

    DRAFT = "Draft"
    PROPOSED = "Proposed"
    APPROVED = "Approved"
    DEPRECATED = "Deprecated"


class RelationshipTypeEnum(str, Enum):
    """Term relationship types."""

    RELATED_TO = "Related To"
    PARENT_OF = "Parent Of"
    CHILD_OF = "Child Of"
    DERIVED_FROM = "Derived From"
    SYNONYM_OF = "Synonym Of"


# ============================================================================
# User and Authentication
# ============================================================================


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRoleEnum] = mapped_column(SQLEnum(UserRoleEnum))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    owned_assets = relationship(
        "DataAsset", back_populates="owner", foreign_keys="DataAsset.owner_id"
    )
    stewarded_assets = relationship(
        "DataAsset", back_populates="steward", foreign_keys="DataAsset.steward_id"
    )
    audits = relationship("AuditLog", back_populates="actor")
    certifications = relationship("Certification", back_populates="certified_by")
    reviews = relationship("Review", back_populates="reviewer")


# ============================================================================
# Business Structure
# ============================================================================


class BusinessDomain(Base):
    """Business domain model."""

    __tablename__ = "business_domains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    business_owner_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    divisions = relationship("BusinessDivision", back_populates="domain")
    assets = relationship("DataAsset", back_populates="business_domain")
    glossary_terms = relationship("BusinessTerm", back_populates="domain")


class BusinessDivision(Base):
    """Business division model."""

    __tablename__ = "business_divisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    domain_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("business_domains.id")
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    domain = relationship("BusinessDomain", back_populates="divisions")
    assets = relationship("DataAsset", back_populates="business_division")

    __table_args__ = (Index("idx_business_division_domain", "domain_id"),)


# ============================================================================
# Data Catalog
# ============================================================================


class DataAsset(Base):
    """Data asset model - central catalog object."""

    __tablename__ = "data_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    asset_type: Mapped[AssetTypeEnum] = mapped_column(SQLEnum(AssetTypeEnum))
    source_system: Mapped[Optional[str]] = mapped_column(String(255))
    physical_location: Mapped[Optional[str]] = mapped_column(String(255))
    business_domain_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("business_domains.id")
    )
    business_division_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("business_divisions.id")
    )
    owner_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    steward_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    classification: Mapped[ClassificationEnum] = mapped_column(
        SQLEnum(ClassificationEnum), default=ClassificationEnum.INTERNAL
    )
    criticality: Mapped[str] = mapped_column(String(50), default="Medium")
    regulatory_relevance: Mapped[bool] = mapped_column(Boolean, default=False)
    lifecycle_status: Mapped[LifecycleStatusEnum] = mapped_column(
        SQLEnum(LifecycleStatusEnum), default=LifecycleStatusEnum.ACTIVE
    )
    certification_status: Mapped[CertificationStatusEnum] = mapped_column(
        SQLEnum(CertificationStatusEnum), default=CertificationStatusEnum.NOT_REVIEWED
    )
    metadata_completeness: Mapped[float] = mapped_column(Float, default=0.0)
    lineage_completeness: Mapped[float] = mapped_column(Float, default=0.0)
    last_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_review_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    business_domain = relationship("BusinessDomain", back_populates="assets")
    business_division = relationship("BusinessDivision", back_populates="assets")
    owner = relationship(
        "User", back_populates="owned_assets", foreign_keys=[owner_id]
    )
    steward = relationship(
        "User", back_populates="stewarded_assets", foreign_keys=[steward_id]
    )
    fields = relationship("DataField", back_populates="asset", cascade="all, delete-orphan")
    assessments = relationship(
        "GovernanceAssessment", back_populates="asset", cascade="all, delete-orphan"
    )
    gaps = relationship(
        "GovernanceGap", back_populates="asset", cascade="all, delete-orphan"
    )
    certifications = relationship(
        "Certification", back_populates="asset", cascade="all, delete-orphan"
    )
    reviews = relationship("Review", back_populates="asset", cascade="all, delete-orphan")
    lineage_nodes = relationship(
        "LineageNode", back_populates="asset", cascade="all, delete-orphan"
    )
    regulatory_mappings = relationship(
        "AssetRegulatoryMapping", back_populates="asset", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_asset_domain", "business_domain_id"),
        Index("idx_asset_division", "business_division_id"),
        Index("idx_asset_owner", "owner_id"),
        Index("idx_asset_steward", "steward_id"),
        Index("idx_asset_classification", "classification"),
        Index("idx_asset_certification", "certification_status"),
    )


class DataField(Base):
    """Data field model."""

    __tablename__ = "data_fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data_asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    display_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    data_type: Mapped[str] = mapped_column(String(50))
    is_nullable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_cde: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    classification: Mapped[ClassificationEnum] = mapped_column(
        SQLEnum(ClassificationEnum), default=ClassificationEnum.INTERNAL
    )
    sensitivity: Mapped[SensitivityEnum] = mapped_column(
        SQLEnum(SensitivityEnum), default=SensitivityEnum.NON_SENSITIVE
    )
    business_term_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("business_terms.id")
    )
    regulatory_tag: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="fields")
    business_term = relationship("BusinessTerm", back_populates="fields")

    __table_args__ = (
        Index("idx_field_asset", "data_asset_id"),
        Index("idx_field_name", "name"),
        Index("idx_field_cde", "is_cde"),
    )


# ============================================================================
# Business Glossary
# ============================================================================


class BusinessTerm(Base):
    """Business glossary term model."""

    __tablename__ = "business_terms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    term: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    definition: Mapped[str] = mapped_column(Text)
    abbreviation: Mapped[Optional[str]] = mapped_column(String(100))
    domain_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("business_domains.id")
    )
    owner: Mapped[Optional[str]] = mapped_column(String(255))
    steward: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[TermStatusEnum] = mapped_column(
        SQLEnum(TermStatusEnum), default=TermStatusEnum.DRAFT
    )
    approval_status: Mapped[str] = mapped_column(String(50), default="Pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    domain = relationship("BusinessDomain", back_populates="glossary_terms")
    fields = relationship("DataField", back_populates="business_term")
    relationships_from = relationship(
        "TermRelationship",
        back_populates="term_from",
        foreign_keys="TermRelationship.term_from_id",
        cascade="all, delete-orphan",
    )
    relationships_to = relationship(
        "TermRelationship",
        back_populates="term_to",
        foreign_keys="TermRelationship.term_to_id",
        cascade="all, delete-orphan",
    )


class TermRelationship(Base):
    """Term relationship model."""

    __tablename__ = "term_relationships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    term_from_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("business_terms.id"), index=True
    )
    term_to_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("business_terms.id"), index=True
    )
    relationship_type: Mapped[RelationshipTypeEnum] = mapped_column(
        SQLEnum(RelationshipTypeEnum)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    term_from = relationship(
        "BusinessTerm", back_populates="relationships_from", foreign_keys=[term_from_id]
    )
    term_to = relationship(
        "BusinessTerm", back_populates="relationships_to", foreign_keys=[term_to_id]
    )

    __table_args__ = (
        Index("idx_term_relationship_from", "term_from_id"),
        Index("idx_term_relationship_to", "term_to_id"),
    )


# ============================================================================
# Regulatory and Governance
# ============================================================================


class RegulatoryReference(Base):
    """Regulatory reference model."""

    __tablename__ = "regulatory_references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    framework: Mapped[str] = mapped_column(String(255))
    reference: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    asset_mappings = relationship(
        "AssetRegulatoryMapping", back_populates="regulatory_reference"
    )


class AssetRegulatoryMapping(Base):
    """Mapping between assets and regulatory references."""

    __tablename__ = "asset_regulatory_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    regulatory_reference_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("regulatory_references.id"), index=True
    )
    justification: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="regulatory_mappings")
    regulatory_reference = relationship("RegulatoryReference", back_populates="asset_mappings")

    __table_args__ = (
        UniqueConstraint(
            "asset_id",
            "regulatory_reference_id",
            name="uq_asset_regulatory_mapping",
        ),
    )


class GovernanceRequirement(Base):
    """Governance requirement model."""

    __tablename__ = "governance_requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    applicability: Mapped[str] = mapped_column(String(255), default="All Assets")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    assessment_results = relationship(
        "AssessmentResult", back_populates="requirement", cascade="all, delete-orphan"
    )


# ============================================================================
# Governance Assessment
# ============================================================================


class GovernanceAssessment(Base):
    """Governance assessment model."""

    __tablename__ = "governance_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    executed_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    score: Mapped[float] = mapped_column(Float)
    maturity_level: Mapped[str] = mapped_column(String(50))
    requirements_checked: Mapped[int] = mapped_column(Integer)
    requirements_passed: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="assessments")
    results = relationship(
        "AssessmentResult", back_populates="assessment", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_assessment_asset", "asset_id"),)


class AssessmentResult(Base):
    """Individual assessment result for a requirement."""

    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("governance_assessments.id"), index=True
    )
    requirement_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("governance_requirements.id"), index=True
    )
    passed: Mapped[bool] = mapped_column(Boolean)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    assessment = relationship("GovernanceAssessment", back_populates="results")
    requirement = relationship("GovernanceRequirement", back_populates="assessment_results")


# ============================================================================
# Governance Gaps
# ============================================================================


class GovernanceGap(Base):
    """Governance gap model."""

    __tablename__ = "governance_gaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    requirement_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("governance_requirements.id"), index=True
    )
    data_field_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("data_fields.id")
    )
    category: Mapped[str] = mapped_column(String(100))
    severity: Mapped[GapSeverityEnum] = mapped_column(SQLEnum(GapSeverityEnum))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[GapStatusEnum] = mapped_column(
        SQLEnum(GapStatusEnum), default=GapStatusEnum.OPEN, index=True
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="gaps")
    requirement = relationship("GovernanceRequirement")

    __table_args__ = (
        Index("idx_gap_asset", "asset_id"),
        Index("idx_gap_status", "status"),
        Index("idx_gap_severity", "severity"),
    )


# ============================================================================
# Certification and Review
# ============================================================================


class Certification(Base):
    """Certification model."""

    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    status: Mapped[CertificationStatusEnum] = mapped_column(
        SQLEnum(CertificationStatusEnum)
    )
    certified_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    certified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="certifications")
    certified_by = relationship("User", back_populates="certifications")


class Review(Base):
    """Review model."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    outcome: Mapped[ReviewOutcomeEnum] = mapped_column(SQLEnum(ReviewOutcomeEnum))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    next_review_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")

    __table_args__ = (Index("idx_review_asset", "asset_id"),)


# ============================================================================
# Lineage
# ============================================================================


class LineageNode(Base):
    """Lineage node model."""

    __tablename__ = "lineage_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    upstream_asset_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("data_assets.id")
    )
    downstream_asset_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("data_assets.id")
    )
    transformation_description: Mapped[Optional[str]] = mapped_column(Text)
    lineage_level: Mapped[str] = mapped_column(String(50), default="asset-level")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    asset = relationship("DataAsset", back_populates="lineage_nodes", foreign_keys=[asset_id])


# ============================================================================
# Audit and Quality
# ============================================================================


class AuditLog(Base):
    """Audit log model."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(255))
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int] = mapped_column(Integer)
    before_value: Mapped[Optional[str]] = mapped_column(Text)
    after_value: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    # Relationships
    actor = relationship("User", back_populates="audits")

    __table_args__ = (
        Index("idx_audit_entity", "entity_type", "entity_id"),
        Index("idx_audit_timestamp", "timestamp"),
    )


class DataQualityObservation(Base):
    """Data quality observation model."""

    __tablename__ = "data_quality_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_assets.id"), index=True
    )
    quality_score: Mapped[float] = mapped_column(Float)
    quality_status: Mapped[str] = mapped_column(String(50))
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    observations: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (Index("idx_quality_asset", "asset_id"),)
