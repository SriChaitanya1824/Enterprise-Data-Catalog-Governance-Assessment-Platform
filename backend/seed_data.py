"""Seed data for demonstration."""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models import (
    User, BusinessDomain, BusinessDivision, DataAsset, DataField,
    BusinessTerm, TermRelationship, RegulatoryReference, GovernanceRequirement,
    GovernanceAssessment, AssessmentResult, GovernanceGap, Certification, Review,
    AuditLog, DataQualityObservation, Base
)
from app.core.security import hash_password
from app.core.config import get_settings


async def seed_database():
    """Seed database with sample data."""
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, future=True
    )
    
    async with AsyncSessionLocal() as db:
        # Users
        users = [
            User(
                email="analyst@governance.com",
                full_name="Governance Analyst",
                hashed_password=hash_password("password123"),
                role="GOVERNANCE_ANALYST"
            ),
            User(
                email="owner@risk.com",
                full_name="Risk Data Owner",
                hashed_password=hash_password("password123"),
                role="DATA_OWNER"
            ),
            User(
                email="steward@governance.com",
                full_name="Data Steward",
                hashed_password=hash_password("password123"),
                role="DATA_STEWARD"
            ),
        ]
        db.add_all(users)
        await db.flush()
        
        # Business Domains
        domains = [
            BusinessDomain(name="Retail Banking", description="Retail banking products and services"),
            BusinessDomain(name="Corporate Banking", description="Corporate banking services"),
            BusinessDomain(name="Risk Management", description="Risk management and compliance"),
            BusinessDomain(name="Finance", description="Financial operations"),
            BusinessDomain(name="Operations", description="Operational functions"),
            BusinessDomain(name="Treasury", description="Treasury operations"),
            BusinessDomain(name="Payments", description="Payment processing"),
            BusinessDomain(name="Customer Management", description="Customer data management"),
        ]
        db.add_all(domains)
        await db.flush()
        
        # Business Divisions
        divisions = [
            BusinessDivision(name="Retail Banking", domain_id=domains[0].id),
            BusinessDivision(name="Corporate Banking", domain_id=domains[1].id),
            BusinessDivision(name="Risk Management", domain_id=domains[2].id),
            BusinessDivision(name="Finance", domain_id=domains[3].id),
            BusinessDivision(name="Operations", domain_id=domains[4].id),
            BusinessDivision(name="Technology", domain_id=None),
        ]
        db.add_all(divisions)
        await db.flush()
        
        # Data Assets - Customer Risk Dataset (demo asset)
        customer_risk_asset = DataAsset(
            name="customer_risk_dataset",
            display_name="Customer Risk Dataset",
            description="Central repository for customer risk assessments and ratings",
            asset_type="Dataset",
            source_system="Risk Analytics Platform",
            physical_location="Hadoop Cluster / S3",
            business_domain_id=domains[2].id,  # Risk Management
            business_division_id=divisions[2].id,  # Risk Management
            owner_id=users[1].id,  # Risk Data Owner
            steward_id=users[2].id,  # Data Steward
            classification="Confidential",
            criticality="Critical",
            regulatory_relevance=True,
            lifecycle_status="Active",
            certification_status="Certified",
            metadata_completeness=94.0,
            lineage_completeness=85.0,
            next_review_date=datetime.utcnow() + timedelta(days=365)
        )
        db.add(customer_risk_asset)
        await db.flush()
        
        # Fields for Customer Risk Dataset
        fields = [
            DataField(
                data_asset_id=customer_risk_asset.id,
                name="customer_id",
                display_name="Customer ID",
                description="Unique customer identifier",
                data_type="VARCHAR",
                is_nullable=False,
                is_cde=True,
                classification="Confidential",
                sensitivity="Sensitive"
            ),
            DataField(
                data_asset_id=customer_risk_asset.id,
                name="risk_rating",
                display_name="Customer Risk Rating",
                description="Assessment of customer credit and compliance risk",
                data_type="VARCHAR",
                is_nullable=False,
                is_cde=True,
                classification="Confidential",
                sensitivity="Highly Sensitive"
            ),
            DataField(
                data_asset_id=customer_risk_asset.id,
                name="assessment_date",
                display_name="Assessment Date",
                description="Date of risk assessment",
                data_type="DATE",
                is_nullable=False,
                is_cde=False,
                classification="Internal"
            ),
        ]
        db.add_all(fields)
        await db.flush()
        
        # Governance Requirements
        requirements = [
            GovernanceRequirement(code="GOV-001", name="Data Owner assigned", category="Accountability", is_mandatory=True),
            GovernanceRequirement(code="GOV-002", name="Data Steward assigned", category="Accountability", is_mandatory=True),
            GovernanceRequirement(code="GOV-003", name="Description provided", category="Metadata", is_mandatory=True),
            GovernanceRequirement(code="GOV-004", name="Classification assigned", category="Classification", is_mandatory=True),
            GovernanceRequirement(code="GOV-005", name="CDE definitions approved", category="Business Context", is_mandatory=True),
            GovernanceRequirement(code="GOV-006", name="Regulatory mapping documented", category="Regulatory", is_mandatory=True),
            GovernanceRequirement(code="GOV-007", name="Lineage documented", category="Traceability", is_mandatory=True),
            GovernanceRequirement(code="GOV-008", name="Review date current", category="Review", is_mandatory=True),
        ]
        db.add_all(requirements)
        await db.flush()
        
        # Business Terms
        terms = [
            BusinessTerm(
                term="Customer Risk Rating",
                definition="Quantitative or qualitative assessment of a customer's financial risk",
                domain_id=domains[2].id,
                owner="Risk Data Office",
                steward="Customer Data Governance",
                status="Approved"
            ),
            BusinessTerm(
                term="Customer",
                definition="Individual or entity with whom the bank maintains a relationship",
                domain_id=domains[7].id,
                owner="Customer Management",
                status="Approved"
            ),
        ]
        db.add_all(terms)
        await db.flush()
        
        # Link fields to terms
        fields[1].business_term_id = terms[0].id
        fields[0].business_term_id = terms[1].id
        
        # Regulatory References
        regulatory_refs = [
            RegulatoryReference(
                framework="Risk Management",
                reference="Risk-001",
                title="Risk Data Lineage Requirement",
                description="All risk data must have documented lineage"
            ),
            RegulatoryReference(
                framework="Compliance",
                reference="Compliance-001",
                title="Customer Data Classification",
                description="Customer data must be classified as sensitive"
            ),
        ]
        db.add_all(regulatory_refs)
        await db.flush()
        
        # Governance Assessment
        assessment = GovernanceAssessment(
            asset_id=customer_risk_asset.id,
            executed_by_id=users[0].id,
            score=94.0,
            maturity_level="Managed",
            requirements_checked=8,
            requirements_passed=8
        )
        db.add(assessment)
        await db.flush()
        
        # Assessment Results
        for req in requirements:
            result = AssessmentResult(
                assessment_id=assessment.id,
                requirement_id=req.id,
                passed=req.code != "GOV-008"  # Simulate missing review date
            )
            db.add(result)
        
        # Governance Gap
        gap = GovernanceGap(
            asset_id=customer_risk_asset.id,
            requirement_id=requirements[7].id,
            category="Review",
            severity="Medium",
            description="Next review date not set"
        )
        db.add(gap)
        
        # Certification
        cert = Certification(
            asset_id=customer_risk_asset.id,
            status="Certified",
            certified_by_id=users[0].id,
            certified_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=365)
        )
        db.add(cert)
        
        # Quality Observation
        quality = DataQualityObservation(
            asset_id=customer_risk_asset.id,
            quality_score=97.0,
            quality_status="Healthy",
            observed_at=datetime.utcnow(),
            observations="Data quality excellent, no missing values detected"
        )
        db.add(quality)
        
        await db.commit()
        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
