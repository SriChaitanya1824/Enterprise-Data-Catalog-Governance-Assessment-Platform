"""Repositories for data access."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models import DataAsset, GovernanceRequirement, BusinessDomain, BusinessDivision


class DataAssetRepository:
    """Repository for data assets."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, asset_id: int):
        """Get asset by ID."""
        result = await self.db.execute(
            select(DataAsset).where(DataAsset.id == asset_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 10, filters: dict = None):
        """List all assets with optional filters."""
        query = select(DataAsset)
        
        if filters:
            if filters.get("domain_id"):
                query = query.where(DataAsset.business_domain_id == filters["domain_id"])
            if filters.get("classification"):
                query = query.where(DataAsset.classification == filters["classification"])
            if filters.get("is_critical"):
                query = query.where(DataAsset.criticality == "Critical")

        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, asset_data: dict):
        """Create new asset."""
        asset = DataAsset(**asset_data)
        self.db.add(asset)
        await self.db.flush()
        return asset

    async def update(self, asset_id: int, update_data: dict):
        """Update asset."""
        asset = await self.get_by_id(asset_id)
        if not asset:
            return None
        
        for key, value in update_data.items():
            if value is not None:
                setattr(asset, key, value)
        
        await self.db.flush()
        return asset


class GovernanceRequirementRepository:
    """Repository for governance requirements."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_mandatory_requirements(self):
        """Get all mandatory requirements."""
        result = await self.db.execute(
            select(GovernanceRequirement).where(
                GovernanceRequirement.is_mandatory == True
            )
        )
        return result.scalars().all()

    async def get_by_code(self, code: str):
        """Get requirement by code."""
        result = await self.db.execute(
            select(GovernanceRequirement).where(
                GovernanceRequirement.code == code
            )
        )
        return result.scalar_one_or_none()


class BusinessDomainRepository:
    """Repository for business domains."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self):
        """List all active domains."""
        result = await self.db.execute(
            select(BusinessDomain).where(BusinessDomain.is_active == True)
        )
        return result.scalars().all()

    async def get_by_id(self, domain_id: int):
        """Get domain by ID."""
        result = await self.db.execute(
            select(BusinessDomain).where(BusinessDomain.id == domain_id)
        )
        return result.scalar_one_or_none()
