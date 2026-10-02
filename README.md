# Enterprise Data Catalog & Governance Assessment Platform

> A comprehensive, production-grade platform for enterprise data governance, metadata management, and governance assessment. Part of a 3-project Data Governance portfolio.

## 🎯 Overview

This platform addresses a critical challenge in enterprise data management: **How can a Data Governance team discover, understand, classify, own, and continuously improve their data assets?**

The Enterprise Data Catalog & Governance Assessment Platform provides a **single source of truth** for:

- **Discovery**: What data assets exist and where
- **Understanding**: Business context, definitions, ownership
- **Governance**: Completeness, compliance, regulatory mapping
- **Assessment**: Scoring and maturity tracking
- **Improvement**: Gap identification and remediation tracking

## 🏗️ Architecture

```
ENTERPRISE DATA SOURCES
         │
    ┌────┼────┐
    ▼    ▼    ▼
 PostgreSQL CSV APIs
    │    │    │
    └────┼────┘
         │
  METADATA DISCOVERY
         │
METADATA NORMALIZATION
         │
 ENTERPRISE CATALOG
    ┌────┼────┐
    ▼    ▼    ▼
Glossary CDEs Ownership
    │    │    │
    └────┼────┘
         │
GOVERNANCE ASSESSMENT
    ┌────┼────┐
    ▼    ▼    ▼
Completeness Lineage Regulatory
    │    │    │
    └────┼────┘
         │
  GOVERNANCE GAPS
         │
ADOPTION DASHBOARDS
         │
   USER INTERFACE
```

## ✨ Key Features

### Data Catalog & Discovery
- **Full-text search** across assets, fields, business terms, domains
- **Multi-dimensional filtering**: domain, classification, criticality, lifecycle, certification status
- **Asset detail pages** with ownership, classification, regulatory mapping, lineage
- **Field-level governance** with CDE identification and lineage
- **Relationship discovery** between assets, glossary terms, and regulatory requirements

### Business Glossary
- **Rich term definitions** with approval workflow
- **Term relationships**: Parent/Child, Synonym, Derived From, Related To
- **Business ownership** and stewardship tracking
- **Link to data assets and fields**
- **Approval status tracking**

### Critical Data Elements (CDEs)
- **First-class citizen** in the catalog
- **Inventory view** with ownership, classification, regulatory mapping
- **Governance assessment** specific to CDEs
- **Lineage tracing** from source to consumption
- **Impact analysis**: downstream asset and report identification

### Governance Assessment Engine
The core differentiator: **deterministic, explainable governance scoring**.

Assessment evaluates 8+ mandatory requirements:
- ✓ Data Owner assigned
- ✓ Data Steward assigned
- ✓ Comprehensive description
- ✓ Classification assigned
- ✓ CDE definitions approved
- ✓ Regulatory mapping documented
- ✓ Lineage captured
- ✓ Review date current

**Scoring methodology**: 
- Each requirement weighted equally
- Score = (Passed Requirements / Total Requirements) × 100
- Maturity level calculated from score:
  - 95–100% = **Optimized**
  - 85–94% = **Managed**
  - 70–84% = **Defined**
  - 50–69% = **Developing**
  - 0–49% = **Initial**

### Governance Gaps
Automatically identifies missing requirements:
- **Gap detection**: Runs during assessments
- **Gap categorization**: Accountability, Metadata, Classification, Business Context, Regulatory, Traceability, Review
- **Severity classification**: Critical, High, Medium, Low
- **Status tracking**: Open, In Progress, Resolved, Waived
- **Gap dashboard**: Browse, filter, prioritize gaps by category and severity

### Governance Dashboards
- **Executive dashboard**: Total assets, critical assets, CDEs, certifications, gaps
- **Adoption metrics**: By division—coverage, ownership, completeness
- **Maturity distribution**: Assets across maturity levels
- **Metadata completeness**: Field-level and asset-level completeness tracking
- **Trend analysis**: Governance improvement over time

### Certification & Review
- **Eligibility requirements**: Mandatory metadata complete, owner/steward assigned, classification assigned
- **Certification workflow**: Not Reviewed → In Review → Certified
- **Certification expiry**: Auto-expiring certifications with renewal reminders
- **Review records**: Tracking reviewer, outcome, next review date
- **Audit trail**: Historical certification and review records

### Metadata Discovery & Ingestion
- **PostgreSQL discovery**: Inspect source schemas and metadata
- **File-based ingestion**: CSV and Parquet metadata import
- **Automated normalization**: Technical metadata → Catalog metadata
- **Metadata profiling**: Row count, null percentage, distinct values, data type analysis
- **Change detection**: Identify schema changes and updates

### Lineage Visibility
- **Asset lineage**: Upstream/downstream relationships
- **Transformation metadata**: Capture transformation logic
- **Field-level lineage** (demonstrated): Trace critical fields through pipeline
- **Regulatory data traceability**: Identify which outputs depend on which inputs
- **OpenLineage integration**: Ready for Marquez or other lineage platforms

### Audit & Compliance
- **Complete audit trail**: Changes to metadata, ownership, classification, certification
- **Actor tracking**: Who changed what, when
- **Before/after values**: Audit compliance and historical analysis
- **Retention**: Full historical audit log for 5+ year retention

### Ownership & Stewardship
- **Data Owner**: Accountable for accuracy, completeness, regulatory compliance
- **Data Steward**: Maintains definition, quality, classification
- **Business Owner**: Owns business process
- **Technical Owner**: Owns infrastructure, pipelines
- **Responsibility gaps**: Dashboard identifies assets missing mandatory roles

### Data Classification
- **Asset-level classification**: Public, Internal, Confidential, Restricted
- **Field-level sensitivity**: Non-Sensitive, Sensitive, Highly Sensitive
- **Classification policies**: Document rationale and justification
- **Regulatory mapping**: Link classifications to regulatory requirements

### Regulatory Mapping
- **Framework-based references**: GDPR, CCPA, internal policies, data retention rules
- **Asset-to-regulation mapping**: Which assets satisfy which requirements
- **Field-level regulatory tags**: Risk data, customer data, transaction data
- **Compliance validation**: Assess asset regulatory completeness

## 📊 Core Data Model

### DataAsset
Central catalog object representing any managed data.
- Metadata: name, type, location, owner, steward
- Classification: sensitivity level, regulatory relevance
- Governance: completeness, maturity, certification status
- Tracking: review dates, assessment history

### DataField
Represents individual fields/columns in assets.
- Technical: name, type, nullability
- Governance: classification, sensitivity, CDE designation
- Traceability: business term linking, regulatory tagging

### BusinessTerm
Rich glossary entry with definitions and relationships.
- Definition, owner, steward, approval status
- Relationships: Parent/Child, Synonym, Related To, Derived From
- Links to fields and assets

### GovernanceRequirement
Reusable requirement template.
- Code, name, category, mandatory flag
- Used to drive assessments and gap detection

### GovernanceAssessment
Captures point-in-time evaluation of an asset.
- Score, maturity level, timestamp
- Individual requirement results
- Historical tracking

### GovernanceGap
Missing requirement identified during assessment.
- Category, severity, status, detection date
- Resolution tracking

### Certification
Records governance certification state.
- Status, certification date, expiry date
- Reviewer and notes
- Eligibility validation

## 🔐 Authentication & Authorization

### Roles
- **ADMIN**: Platform administration, user management
- **GOVERNANCE_ANALYST**: Manage catalog, run assessments, approve glossary
- **DATA_OWNER**: Update owned assets, confirm metadata
- **DATA_STEWARD**: Maintain definitions, field mappings, glossary
- **REVIEWER**: Review and certify assets
- **AUDITOR**: View catalog and history, no changes
- **VIEWER**: Read-only access to catalog

### Security
- JWT authentication with configurable expiration
- Role-based access control (RBAC)
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- Audit logging of all changes

## 🚀 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18, TypeScript, Vite, TanStack Query, TanStack Table |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.x, Async/await |
| **Database** | PostgreSQL 15 with indexed model |
| **Auth** | JWT (python-jose), bcrypt password hashing |
| **ORM** | SQLAlchemy with async session management |
| **Testing** | pytest, pytest-asyncio, httpx for client testing |
| **Code Quality** | Ruff, Black, mypy (where practical) |
| **Containers** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Orchestration** | Apache Airflow (demo DAGs) |
| **Lineage** | OpenLineage-compatible metadata format |
| **Data Quality** | Great Expectations (integration point) |

## 📦 Repository Structure

```
Enterprise-Data-Catalog-Governance-Assessment-Platform/
├── backend/
│   ├── app/
│   │   ├── api/v1/              # REST API endpoints
│   │   ├── core/                # Config, database, security
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic validation
│   │   ├── repositories/        # Data access layer
│   │   ├── services/            # Business logic
│   │   ├── assessment/          # Governance assessment engine
│   │   ├── certification/       # Certification workflow
│   │   ├── catalog/             # Catalog services
│   │   ├── glossary/            # Glossary services
│   │   ├── lineage/             # Lineage services
│   │   └── main.py              # FastAPI application
│   ├── tests/                   # Unit and integration tests
│   ├── alembic/                 # Database migrations
│   ├── pyproject.toml           # Poetry dependencies
│   └── requirements.txt         # Alternative requirements format
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable React components
│   │   ├── pages/               # Page-level components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API client, utilities
│   │   ├── types/               # TypeScript types
│   │   ├── router/              # React Router config
│   │   ├── App.tsx              # Root component
│   │   └── main.tsx             # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── airflow/
│   └── dags/
│       ├── metadata_discovery.py
│       ├── governance_assessment.py
│       └── certification_expiry_check.py
│
├── data/
│   ├── sample/                  # Sample data for demo
│   ├── raw/                     # Raw ingestion files
│   └── generated/               # Generated test data
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── catalog.md
│   ├── glossary.md
│   ├── cde-management.md
│   ├── assessment-methodology.md
│   ├── governance-gaps.md
│   ├── certification.md
│   ├── lineage.md
│   ├── regulatory-mapping.md
│   ├── api.md
│   ├── testing.md
│   └── demo.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── Makefile
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15 (if running without Docker)

### Setup with Docker Compose

```bash
# Clone repository
git clone https://github.com/SriChaitanya1824/Enterprise-Data-Catalog-Governance-Assessment-Platform.git
cd Enterprise-Data-Catalog-Governance-Assessment-Platform

# Copy environment file
cp .env.example .env

# Start services
docker compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/api/docs
# PostgreSQL: localhost:5432
```

### Setup for Local Development

**Backend:**
```bash
cd backend
poetry install
# Configure .env
poetry run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Database:**
```bash
# Create PostgreSQL database
createdb catalog_db

# Run migrations
cd backend
alembic upgrade head

# Seed data
python scripts/seed_data.py
```

## 📋 Governance Assessment Methodology

### Scoring Model

Assessment score = (Requirements Passed / Total Requirements Evaluated) × 100

**Weight Distribution:**
- Accountability: 25% (owner, steward)
- Metadata: 20% (description, asset type, domain)
- Classification: 15% (data classification)
- Business Context: 15% (glossary mapping)
- Regulatory: 15% (regulatory mapping)
- Traceability: 10% (lineage)
- Review: 5% (review dates)

**Maturity Levels:**
- **Initial (0–49%)**: Minimal governance controls; asset lacks multiple required attributes
- **Developing (50–69%)**: Basic governance established; most metadata present; gaps in strategic areas
- **Defined (70–84%)**: Good governance foundation; most requirements met; minor gaps remain
- **Managed (85–94%)**: Strong governance; nearly all requirements met; high compliance
- **Optimized (95–100%)**: Exemplary governance; complete metadata; continuous improvement

### Governance Requirements

Core requirements evaluated:

| Code | Requirement | Category | Mandatory |
|------|-------------|----------|-----------|
| GOV-001 | Data Owner assigned | Accountability | Yes |
| GOV-002 | Data Steward assigned | Accountability | Yes |
| GOV-003 | Comprehensive description | Metadata | Yes |
| GOV-004 | Classification assigned | Classification | Yes |
| GOV-005 | CDE definitions approved | Business Context | Yes |
| GOV-006 | Regulatory mapping (if applicable) | Regulatory | Yes |
| GOV-007 | Lineage documented | Traceability | Yes |
| GOV-008 | Review date current | Review | Yes |

### Gap Categories

- **Accountability**: Missing owner, steward, or business owner
- **Metadata**: Incomplete description, source, domain
- **Classification**: Missing or incorrect classification
- **Business Context**: No glossary term, no approved definition
- **Regulatory**: Regulatory data without mapping, compliance metadata missing
- **Traceability**: Incomplete lineage, missing upstream/downstream relationships
- **Review**: Missing review dates, expired certifications

## 🎯 Demo Walkthrough: "Customer Risk Rating"

This demonstrates the complete platform workflow:

### 1. Discovery
- Search "Customer Risk Rating"
- Business Glossary result appears
- Open glossary term to see definition and linked CDE

### 2. Understanding
- Click linked CDE: "Customer Risk Rating"
- Open linked Data Asset: "Customer Risk Dataset"
- View ownership: Risk Data Office (owner), Customer Data Governance (steward)
- View classification: Confidential
- View fields: risk_rating, customer_id, assessment_date

### 3. Governance Assessment
- Run governance assessment on Customer Risk Dataset
- Score: 82% (Managed)
- Passed: Owner ✓, Steward ✓, Description ✓, Classification ✓, Regulatory mapping ✓, Lineage ✓
- Failed: Review date ✗

### 4. Gap Identification
- Platform detects: "Review date missing" (Severity: Medium, Category: Review)
- Gap created and displayed in Governance Gaps dashboard

### 5. Remediation
- Data Owner updates asset metadata
- Sets next review date to 2027-01-01
- Saves changes

### 6. Re-assessment
- Run assessment again
- Score: 100% (Optimized)
- All gaps resolved

### 7. Certification
- Asset now eligible for certification
- Data Owner submits for certification
- Reviewer approves
- Asset status: Certified (expires 2027-10-01)

### 8. Tracking Improvement
- Assessment history shows progression:
  - Oct 1: 82% (Managed)
  - Oct 15: 100% (Optimized)
- Dashboard shows improving divisional adoption metrics

## 🔗 Lineage Integration

### OpenLineage Support
The platform is designed to integrate with OpenLineage-compatible systems (Marquez, custom pipelines).

**What's implemented:**
- Lineage metadata model (upstream/downstream relationships)
- Lineage completeness scoring
- Field-level lineage structure
- Lineage visibility in asset detail pages
- Lineage tracing UI

**What's demonstrated:**
- Sample lineage data showing transformation pipeline
- Lineage completeness calculation
- Upstream/downstream navigation

**Integration ready for:**
- Marquez API integration
- Custom OpenLineage event emission
- Apache Spark lineage capture
- dbt metadata integration

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app

# Specific test suites
pytest tests/test_assessment.py -v
pytest tests/test_certification.py -v
pytest tests/test_search.py -v
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Integration Tests
```bash
# Run complete Customer Risk Rating workflow
cd backend
pytest tests/integration/test_cde_workflow.py -v
```

### Test Coverage
Target: >80% coverage on core services

- Authentication & authorization
- Asset CRUD operations
- Governance assessment and scoring
- Gap detection
- Certification eligibility and workflow
- Search and filtering
- Dashboard metric calculation

## 📚 API Documentation

### Base URL
`http://localhost:8000/api/v1`

### Key Endpoints

**Assets**
- `GET /assets` - List assets with filtering and pagination
- `GET /assets/{id}` - Get asset detail
- `POST /assets` - Create asset
- `PATCH /assets/{id}` - Update asset
- `GET /assets/{id}/fields` - Get asset fields

**Governance**
- `POST /assessments/run/{asset_id}` - Run assessment
- `GET /assessments/{asset_id}/history` - Get assessment history
- `GET /gaps` - List governance gaps
- `PATCH /gaps/{id}` - Update gap status

**Certification**
- `GET /certifications` - List certifications
- `POST /certifications` - Submit for certification
- `GET /certifications/{id}` - Get certification details

**Glossary**
- `GET /glossary` - List business terms
- `POST /glossary` - Create term
- `GET /glossary/{id}/relationships` - Get term relationships

**Search**
- `GET /search?q=...` - Global search

**Dashboard**
- `GET /dashboard/metrics` - Overall metrics
- `GET /dashboard/adoption` - Division adoption
- `GET /dashboard/gaps` - Gap categories
- `GET /dashboard/maturity` - Maturity distribution

**Full OpenAPI docs**: `http://localhost:8000/api/docs`

## ⚙️ Configuration

### Environment Variables
See `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/catalog_db

# Authentication
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Integrations
OPENLINEAGE_URL=http://localhost:5000
MARQUEZ_URL=http://localhost:3000

# Application
APP_NAME=Enterprise Data Catalog & Governance Platform
APP_VERSION=1.0.0
DEBUG=False
```

## 🔄 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`):

1. **Code Quality**
   - Ruff linting
   - Black formatting check
   - Type checking (mypy)

2. **Backend Tests**
   - Unit tests
   - Integration tests
   - Coverage reporting

3. **Frontend Tests**
   - Component tests
   - Type checking

4. **Build Verification**
   - Backend build
   - Frontend build (Vite)
   - Docker image build

## 📊 Seed Data

Platform comes pre-seeded with realistic enterprise data:

- **6 Business Divisions**: Retail Banking, Corporate Banking, Risk, Finance, Operations, Technology
- **8 Business Domains**: Retail Banking, Corporate Banking, Risk Management, Finance, Operations, Treasury, Payments, Customer Management
- **10+ Users** across roles
- **25+ Data Assets** across domains
- **100+ Data Fields** with CDE designations
- **20+ Business Terms** with relationships and approvals
- **8+ Regulatory References**
- **10+ Governance Requirements**
- **30+ Assessment Records** showing maturity progression
- **20+ Governance Gaps** across categories

Complete demo scenario for "Customer Risk Rating" is fully functional.

## 📖 Documentation

Detailed documentation in `/docs`:

- `architecture.md` - System design and component details
- `data-model.md` - Entity relationships and schema explanation
- `catalog.md` - Catalog discovery and browsing features
- `glossary.md` - Business glossary and term management
- `cde-management.md` - Critical Data Elements lifecycle
- `assessment-methodology.md` - Governance scoring methodology
- `governance-gaps.md` - Gap detection and remediation
- `certification.md` - Certification workflow and eligibility
- `lineage.md` - Lineage integration and visualization
- `regulatory-mapping.md` - Regulatory requirements mapping
- `api.md` - Complete API reference
- `testing.md` - Testing strategy and coverage
- `demo.md` - Walkthrough of Customer Risk Rating scenario

## ⚠️ Limitations

### Implemented
- Full data catalog with search and filtering
- Governance assessment with deterministic scoring
- Gap detection and categorization
- Certification workflow with expiry
- Business glossary with relationships
- CDE management and lineage
- Audit trail for all changes
- Role-based access control
- Docker/Docker Compose deployment

### Simulated (Synthetic/Demo)
- Sample lineage data (not from live pipelines)
- Sample quality observations (not from Great Expectations)
- Demo governance documents (placeholder integration)
- Synthetic enterprise data only (no real customer data)

### Not Implemented (Future)
- Real-time lineage capture from Spark/Airflow
- Automated data quality rules from Great Expectations
- SSO/LDAP integration
- Cloud storage integration (S3, GCS, Azure)
- Policy-as-Code engine
- Advanced semantic search (AI/ML)
- Data contracts validation
- Collibra/Alation integrations

These are documented as future enhancements, not claimed as working features.

## 🤝 Architecture Distinction from Related Projects

This project is **Project 3** in a Data Governance portfolio:

| Project | Focus | Problem Solved |
|---------|-------|---|
| **Project 1: Lineage & Quality** | Governance + Lineage + Quality | How do we trace data and measure quality? |
| **Project 2: Controls & Exceptions** | Controls + Findings + Exceptions | How do we manage regulatory exceptions and remediation? |
| **Project 3: Catalog & Assessment** ← | **Catalog + Metadata + Assessment** | **How do we discover, understand, and assess governance maturity?** |

Each project is architecturally distinct and solves different problems. Project 3 focuses on **discovery, cataloging, and governance assessment**.

## 🔐 Data Privacy

- **No real data**: All demonstration data is synthetic enterprise data
- **No real customer PII**: Field names like `customer_id` are generic
- **No real regulatory compliance**: References are generic examples, not legal requirements
- **Suitable for portfolio demonstration only**

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contact

For questions about this implementation:
- This is a portfolio project demonstrating enterprise data governance patterns
- Not an official Deutsche Bank product
- Not affiliated with any real regulatory body

---

**Last Updated**: October 2, 2026  
**Version**: 1.0.0  
**Status**: Production Ready for Portfolio Demonstration
