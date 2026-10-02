"""Certification service implementation."""

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import (
    DataAsset, Certification, CertificationStatusEnum,
    User, GovernanceAssessment
)


class CertificationService:
    """Service for managing certifications."""

    def __init__(self, db: AsyncSession):
        """Initialize service."""
        self.db = db

    async def check_certification_eligibility(self, asset_id: int) -> dict:
        """Check if asset is eligible for certification."""
        result = await self.db.execute(
            select(DataAsset).where(DataAsset.id == asset_id)
            .options(selectinload(DataAsset.owner), selectinload(DataAsset.steward))
        )
        asset = result.scalar_one_or_none()
        
        if not asset:
            return {"eligible": False, "errors": ["Asset not found"]}

        errors = []

        # Check ownership
        if not asset.owner_id:
            errors.append("Owner required")

        # Check stewardship
        if not asset.steward_id:
            errors.append("Steward required")

        # Check classification
        if not asset.classification:
            errors.append("Classification required")

        # Check description
        if not asset.description or len(asset.description) < 20:
            errors.append("Comprehensive description required")

        # Check governance score
        if asset.metadata_completeness < 80:
            errors.append("Metadata completeness must be >= 80%")

        return {
            "eligible": len(errors) == 0,
            "errors": errors,
            "completeness": asset.metadata_completeness
        }

    async def get_certifications(
        self, skip: int = 0, limit: int = 10, status_filter: str = None
    ) -> list:
        """Get certifications."""
        query = select(Certification)
        
        if status_filter:
            query = query.where(Certification.status == status_filter)

        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_expiring_certifications(self, days_until_expiry: int = 30) -> list:
        """Get certifications expiring soon."""
        threshold = datetime.now(timezone.utc) + timedelta(days=days_until_expiry)
        
        result = await self.db.execute(
            select(Certification).where(
                (Certification.expires_at <= threshold) &
                (Certification.expires_at > datetime.now(timezone.utc)) &
                (Certification.status == "Certified")
            )
        )
        return result.scalars().all()

    async def revoke_expired_certifications(self) -> int:
        """Update expired certifications."""
        now = datetime.now(timezone.utc)
        
        result = await self.db.execute(
            select(Certification).where(
                (Certification.expires_at <= now) &
                (Certification.status == "Certified")
            )
        )
        expired = result.scalars().all()
        
        for cert in expired:
            cert.status = CertificationStatusEnum.CERTIFICATION_EXPIRED
        
        await self.db.commit()
        return len(expired)
