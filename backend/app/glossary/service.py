"""Glossary service for business term management."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import BusinessTerm, TermRelationship, TermStatusEnum


class GlossaryService:
    """Service for glossary management."""

    def __init__(self, db: AsyncSession):
        """Initialize service."""
        self.db = db

    async def get_term(self, term_id: int) -> BusinessTerm:
        """Get term by ID."""
        result = await self.db.execute(
            select(BusinessTerm).where(BusinessTerm.id == term_id)
        )
        return result.scalar_one_or_none()

    async def get_term_by_name(self, term: str) -> BusinessTerm:
        """Get term by name."""
        result = await self.db.execute(
            select(BusinessTerm).where(BusinessTerm.term == term)
        )
        return result.scalar_one_or_none()

    async def list_terms(
        self, skip: int = 0, limit: int = 10, status: str = None
    ) -> list:
        """List business terms."""
        query = select(BusinessTerm)
        
        if status:
            query = query.where(BusinessTerm.status == status)

        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_related_terms(self, term_id: int) -> list:
        """Get related terms."""
        result = await self.db.execute(
            select(TermRelationship).where(
                TermRelationship.term_from_id == term_id
            )
        )
        return result.scalars().all()

    async def approve_term(self, term_id: int) -> BusinessTerm:
        """Approve a business term."""
        term = await self.get_term(term_id)
        if term:
            term.status = TermStatusEnum.APPROVED
            term.approval_status = "Approved"
            await self.db.commit()
        return term
