# Governance Assessment Methodology

## Scoring Model

The Enterprise Data Catalog uses a **deterministic, explainable governance scoring model** to evaluate data asset governance maturity.

## Core Principle

> **A data asset's governance score reflects the completeness of its governance metadata and controls.**

The score is NOT a ranking or rating of quality, but a **measurement of governance implementation completeness**.

## Assessment Process

### 1. Requirement Evaluation
For each data asset, the platform evaluates **8 mandatory governance requirements**:

| # | Code | Requirement | Category | Mandatory |
|---|------|-------------|----------|-----------|
| 1 | GOV-001 | Data Owner assigned | Accountability | Yes |
| 2 | GOV-002 | Data Steward assigned | Accountability | Yes |
| 3 | GOV-003 | Comprehensive description | Metadata | Yes |
| 4 | GOV-004 | Classification assigned | Classification | Yes |
| 5 | GOV-005 | CDE definitions approved | Business Context | Yes |
| 6 | GOV-006 | Regulatory mapping (if applicable) | Regulatory | Yes |
| 7 | GOV-007 | Lineage documented | Traceability | Yes |
| 8 | GOV-008 | Review date current | Review | Yes |

### 2. Requirement Evaluation Rules

**GOV-001: Data Owner**
- Passes: asset.owner_id is not null
- Purpose: Ensures clear accountability for asset accuracy

**GOV-002: Data Steward**
- Passes: asset.steward_id is not null
- Purpose: Ensures operational governance management

**GOV-003: Description**
- Passes: asset.description exists and length >= 20 characters
- Purpose: Ensures business context is documented

**GOV-004: Classification**
- Passes: asset.classification is not null
- Purpose: Ensures sensitivity is assessed

**GOV-005: CDE Definitions**
- Passes: All CDE fields in asset have business_term_id assigned
- Not Applicable: Asset has no CDEs
- Purpose: Ensures critical elements have approved definitions

**GOV-006: Regulatory Mapping**
- Passes: Asset has at least one RegulatoryReference if regulatory_relevance=True
- Not Applicable: asset.regulatory_relevance=False
- Purpose: Ensures regulatory data is explicitly mapped

**GOV-007: Lineage**
- Passes: asset.lineage_completeness >= 50
- Purpose: Ensures traceability is documented

**GOV-008: Review Date**
- Passes: asset.next_review_date is not null
- Purpose: Ensures regular governance reviews

### 3. Score Calculation

```
Score = (Requirements Passed / Total Requirements) × 100
```

### Example:
```
Requirements Checked: 8
Requirements Passed: 7
Score: (7 / 8) × 100 = 87.5%
```

## Maturity Levels

Score is mapped to **governance maturity level**:

### Initial (0–49%)
**Characteristics:**
- Minimal governance controls
- Asset lacks multiple required attributes
- Ownership not established
- No business context
- Not suitable for regulatory reporting

**Actions Required:**
- Assign ownership and stewardship
- Document business definition
- Perform risk classification
- Establish review schedule

### Developing (50–69%)
**Characteristics:**
- Basic governance established
- Most metadata present
- Owner and steward assigned
- Gaps in strategic areas
- Suitable for internal use with caveats

**Actions Required:**
- Complete business glossary mapping
- Document lineage
- Complete regulatory mapping (if applicable)
- Establish certification schedule

### Defined (70–84%)
**Characteristics:**
- Good governance foundation
- Most requirements met
- Minor gaps remaining
- Business context clear
- Suitable for managed internal use

**Actions Required:**
- Complete remaining metadata
- Ensure current review dates
- Enhance lineage documentation
- Prepare for certification

### Managed (85–94%)
**Characteristics:**
- Strong governance
- Nearly all requirements met
- High compliance
- Suitable for critical business use
- Ready for certification

**Actions Required:**
- Final metadata polish
- Plan certification review
- Establish renewal schedule

### Optimized (95–100%)
**Characteristics:**
- Exemplary governance
- Complete metadata
- Continuous improvement in place
- Enterprise-grade governance
- Model for other assets

**Actions:**
- Maintain through reviews
- Share as governance exemplar

## Gap Severity Determination

Governance gaps are automatically categorized by **severity** based on **requirement type and asset criticality**:

### Severity Rules

| Condition | Severity |
|-----------|----------|
| Missing owner on critical regulatory asset | Critical |
| Missing steward on critical asset | High |
| Missing classification on any asset | High |
| Missing glossary mapping on CDE | Medium |
| Missing lineage on regulatory asset | Medium |
| Missing review date | Medium |
| Missing description | Low |

## Assessment History

The platform maintains **full assessment history** for each asset:

```
Assessment History for Customer Risk Dataset:

Date           Score  Maturity    Owner Change
2026-10-01     82%    Managed     Review date added
2026-10-15     88%    Managed     Lineage improved
2026-11-01     94%    Managed     Certified
```

This allows visualization of **governance improvement trajectory**.

## Divisional Adoption Metrics

For each business division, the platform calculates:

| Metric | Calculation |
|--------|-------------|
| Assets Registered | Count of active DataAssets |
| Assets with Owners | Count where owner_id is not null |
| Assets with Stewards | Count where steward_id is not null |
| Assets Classified | Count where classification is not null |
| Average Completeness | Mean of asset.metadata_completeness |
| Average Governance Score | Mean of latest assessment.score |

**Purpose**: Track divisional governance maturity without ranking or competition.

## Key Principles

### 1. Deterministic
- Same asset always produces same score
- No randomness or subjective judgment
- Reproducible across assessments

### 2. Explainable
- Users can see exactly why score is X%
- Each failed requirement documented in gaps
- Clear path to improvement

### 3. Actionable
- Gaps identified automatically
- Specific actions listed for each gap
- Maturity levels indicate next steps

### 4. Non-Punitive
- Score reflects metadata completeness, not data quality
- Not used for personnel evaluation
- Focused on governance improvement

### 5. Continuous
- Assessments run regularly (weekly)
- Historical trends tracked
- Improvement recognized and visible

## Example Assessment

### Asset: Customer Risk Dataset

**Requirements Evaluation:**
| Requirement | Status | Details |
|-------------|--------|---------|
| GOV-001: Owner | ✓ PASS | Risk Data Owner assigned |
| GOV-002: Steward | ✓ PASS | Customer Data Governance assigned |
| GOV-003: Description | ✓ PASS | 150-character description present |
| GOV-004: Classification | ✓ PASS | Confidential classification |
| GOV-005: CDE Defs | ✓ PASS | All 2 CDEs have approved terms |
| GOV-006: Regulatory | ✓ PASS | 2 regulatory references mapped |
| GOV-007: Lineage | ✓ PASS | Lineage completeness: 85% |
| GOV-008: Review Date | ✗ FAIL | Next review: not set |

**Calculation:**
- Total Requirements: 8
- Requirements Passed: 7
- Score: 87.5%
- Maturity: **Managed**

**Identified Gaps:**
1. **Next Review Date Missing** (Category: Review, Severity: Medium)
   - Resolution: Set next_review_date to one year from today

**Next Assessment:**
After setting review date → Score: 100% → Maturity: **Optimized**

## Configuration

Governance requirements can be customized:

```python
# In configuration
GOVERNANCE_REQUIREMENTS = [
    {"code": "GOV-001", "mandatory": True, "weight": 0.25},
    {"code": "GOV-002", "mandatory": True, "weight": 0.25},
    ...
]

MATURITY_THRESHOLDS = {
    "Initial": (0, 49),
    "Developing": (50, 69),
    "Defined": (70, 84),
    "Managed": (85, 94),
    "Optimized": (95, 100),
}

GAP_SEVERITY_RULES = {
    "missing_owner_on_critical": "Critical",
    "missing_steward": "High",
    ...
}
```

## API Usage

### Run Assessment
```bash
POST /api/v1/assessments/run/{asset_id}?user_id=1

Response:
{
  "id": 42,
  "score": 87.5,
  "maturity": "Managed",
  "requirements_checked": 8,
  "requirements_passed": 7
}
```

### Get Assessment History
```bash
GET /api/v1/assessments/{asset_id}/history

Response:
[
  {"executed_at": "2026-10-01T10:00:00Z", "score": 82, "maturity": "Managed"},
  {"executed_at": "2026-10-15T10:00:00Z", "score": 88, "maturity": "Managed"},
  {"executed_at": "2026-11-01T10:00:00Z", "score": 94, "maturity": "Managed"}
]
```

### Get Governance Gaps
```bash
GET /api/v1/gaps?asset_id=1&status=Open

Response:
[
  {
    "id": 101,
    "category": "Review",
    "severity": "Medium",
    "description": "Next review date not set",
    "status": "Open"
  }
]
```

---

**Methodology Version**: 1.0  
**Last Updated**: October 2, 2026  
**Reviewed By**: Data Governance Office
