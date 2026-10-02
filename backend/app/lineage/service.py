"""Lineage service for data lineage management."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import LineageNode


class LineageService:
    """Service for lineage management."""

    def __init__(self, db: AsyncSession):
        """Initialize service."""
        self.db = db

    async def get_upstream_lineage(self, asset_id: int, depth: int = 5) -> list:
        """Get upstream lineage for an asset."""
        lineage = []
        current_assets = [asset_id]
        
        for level in range(depth):
            result = await self.db.execute(
                select(LineageNode).where(
                    LineageNode.downstream_asset_id.in_(current_assets)
                )
            )
            nodes = result.scalars().all()
            
            if not nodes:
                break
            
            lineage.extend(nodes)
            current_assets = [n.asset_id for n in nodes]
        
        return lineage

    async def get_downstream_lineage(self, asset_id: int, depth: int = 5) -> list:
        """Get downstream lineage for an asset."""
        lineage = []
        current_assets = [asset_id]
        
        for level in range(depth):
            result = await self.db.execute(
                select(LineageNode).where(
                    LineageNode.upstream_asset_id.in_(current_assets)
                )
            )
            nodes = result.scalars().all()
            
            if not nodes:
                break
            
            lineage.extend(nodes)
            current_assets = [n.asset_id for n in nodes]
        
        return lineage

    async def create_lineage_relationship(
        self, asset_id: int, upstream_id: int = None, 
        downstream_id: int = None, transformation: str = None
    ) -> LineageNode:
        """Create lineage relationship."""
        node = LineageNode(
            asset_id=asset_id,
            upstream_asset_id=upstream_id,
            downstream_asset_id=downstream_id,
            transformation_description=transformation
        )
        self.db.add(node)
        await self.db.flush()
        return node
