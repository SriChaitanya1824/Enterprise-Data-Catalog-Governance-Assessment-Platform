"""Governance assessment service."""

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
