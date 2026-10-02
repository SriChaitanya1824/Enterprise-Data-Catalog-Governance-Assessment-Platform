# Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)            │
│  Dashboard │ Catalog │ Glossary │ Assessments │ Gaps │ Certs│
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼────────────────────────────────┐
│              BACKEND (FastAPI + Python 3.12)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Layer (/api/v1)                      │  │
│  │  Routes: assets │ glossary │ assessments │ gaps       │  │
│  └───────────────────┬────────────────────────────────┬─┘  │
│                      │                                │     │
│  ┌──────────────────▼─────────────────┬──────────────▼──┐  │
│  │  Services Layer                    │ Middleware     │  │
│  │  - Assessment Engine               │ - Auth/RBAC    │  │
│  │  - Gap Detection                   │ - Validation   │  │
│  │  - Lineage Engine                  │ - Error Handler│  │
│  │  - Metadata Discovery              │ - Audit Logging│  │
│  └──────────────────┬─────────────────┴───────────────┘   │
│                     │                                      │
│  ┌──────────────────▼──────────────────────────────────┐  │
│  │  Repositories & Async Data Access                  │  │
│  │  (SQLAlchemy 2.x async/await)                      │  │
│  └──────────────────┬───────────────────────────────┬─┘  │
└─────────────────────┼───────────────────────────────┼────┘
                      │                               │
        ┌─────────────▼────────────────────────────▐ │
        │                                          │ │
   ┌────▼────────────────────────────────────────┐ │ │
   │  PostgreSQL 15                              │ │ │
   │  - DataAsset                                │ │ │
   │  - DataField                                │ │ │
   │  - BusinessTerm                             │ │ │
   │  - GovernanceAssessment                     │ │ │
   │  - GovernanceGap                            │ │ │
   │  - Certification & Review                   │ │ │
   │  - AuditLog                                 │ │ │
   │  - LineageNode                              │ │ │
   └────────────────────────────────────────────┘ │ │
                                                  │ │
            ┌─────────────────────────────────────┘ │
            │                                       │
   ┌────────▼──────────────────────────────────────▼───┐
   │          Optional Integrations                    │
   │  - OpenLineage / Marquez                          │
   │  - Great Expectations                            │
   │  - External IAM                                  │
   └──────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Architecture
```
App Component
├── Layout (Header, Navigation)
├── Router Configuration
│   ├── /dashboard        → Dashboard
│   ├── /catalog          → Catalog
│   ├── /assets/:id       → Asset Detail
│   ├── /glossary         → Glossary
│   ├── /cdes             → CDEs
│   ├── /assessments      → Assessments
│   ├── /gaps             → Governance Gaps
│   └── /certifications   → Certifications
│
├── Hooks
│   ├── useQuery           (TanStack Query)
│   ├── useMutation        (API calls)
│   └── useRouter          (Navigation)
│
└── Services
    ├── api.ts             (HTTP client)
    ├── auth.ts            (Auth management)
    └── utils.ts           (Helpers)
```

### Backend Architecture
```
FastAPI Application
├── /api/v1/
│   ├── assets/            (Data Asset endpoints)
│   ├── fields/            (Field endpoints)
│   ├── glossary/          (Business Glossary)
│   ├── assessments/       (Governance Assessment)
│   ├── gaps/              (Governance Gaps)
│   ├── certifications/    (Certification)
│   ├── reviews/           (Review workflow)
│   ├── search/            (Global search)
│   └── dashboard/         (Metrics & dashboards)
│
├── Services
│   ├── Assessment Service (Scoring, gap detection)
│   ├── Glossary Service   (Term management)
│   ├── Lineage Service    (Lineage queries)
│   ├── Certification Svc  (Workflow)
│   └── Discovery Service  (Metadata ingestion)
│
├── Repositories
│   ├── DataAssetRepository
│   ├── BusinessTermRepository
│   ├── GovernanceRequirementRepository
│   └── ...
│
└── Models (SQLAlchemy ORM)
    ├── User
    ├── DataAsset
    ├── DataField
    ├── BusinessTerm
    ├── GovernanceAssessment
    └── ...
```

## Data Flow

### Assessment Workflow
```
1. User triggers assessment
2. Backend loads asset
3. Assessment Service evaluates requirements
4. For each requirement:
   - Check ownership
   - Check metadata completeness
   - Check classification
   - Check definitions
   - Check regulatory mapping
   - Check lineage
   - Check review dates
5. Calculate score and maturity
6. Detect gaps for failed requirements
7. Store assessment history
8. Return results to frontend
```

### Gap Detection Flow
```
1. Assessment identifies failed requirement
2. Determine gap category (from requirement mapping)
3. Determine severity (from gap rules)
4. Create GovernanceGap record
5. Record in audit log
6. Frontend queries gaps and displays
```

## Database Design

### Key Relationships
```
User (1) ──────────────────────────── (M) DataAsset (owner/steward)
         (1) ──────────────────────── (M) Review
         (1) ──────────────────────── (M) Certification
         (1) ──────────────────────── (M) AuditLog

BusinessDomain (1) ──────────────── (M) BusinessDivision
                (1) ──────────────── (M) DataAsset
                (1) ──────────────── (M) BusinessTerm

DataAsset (1) ────────────────────── (M) DataField
          (1) ────────────────────── (M) GovernanceAssessment
          (1) ────────────────────── (M) GovernanceGap
          (1) ────────────────────── (M) Certification
          (1) ────────────────────── (M) Review
          (1) ────────────────────── (M) LineageNode

GovernanceAssessment (1) ────────── (M) AssessmentResult
                      (1) ────────── (1) DataAsset

GovernanceRequirement (1) ────────── (M) AssessmentResult
                      (1) ────────── (M) GovernanceGap

BusinessTerm (1) ────────────────── (M) DataField
             (M) ────────────────── (M) TermRelationship
             (1) ────────────────── (1) BusinessDomain

RegulatoryReference (1) ────────── (M) AssetRegulatoryMapping

DataAsset (M) ────────────────────── (M) RegulatoryReference
```

### Indexing Strategy
```
DataAsset.name                    - Fast asset lookup
DataAsset.business_domain_id      - Domain filtering
DataAsset.business_division_id    - Division filtering
DataAsset.owner_id                - Ownership queries
DataAsset.classification          - Classification filtering
DataAsset.certification_status    - Certification queries
DataField.is_cde                  - CDE discovery
DataField.name                    - Field search
BusinessTerm.term                 - Term lookup
GovernanceGap.status              - Gap filtering
GovernanceGap.severity            - Severity filtering
AuditLog.entity_type, entity_id   - Change tracking
AuditLog.timestamp                - Historical queries
```

## Security Architecture

### Authentication Flow
```
1. User submits credentials
2. Backend validates email/password
3. Backend generates JWT token
4. Frontend stores token in localStorage
5. Frontend includes token in Authorization header
6. Backend validates token on each request
7. Backend extracts user and role from token
```

### Authorization Strategy
```
Role-Based Access Control (RBAC)

ADMIN
├── Full platform access
├── User management
└── Configuration

GOVERNANCE_ANALYST
├── Manage catalog
├── Run assessments
├── Initiate reviews
└── Approve glossary terms

DATA_OWNER
├── Update own assets
├── Confirm metadata
└── Participate in certification

DATA_STEWARD
├── Maintain definitions
├── Manage glossary
└── Field classifications

REVIEWER
├── Review assets
└── Approve certification

AUDITOR
├── View all records
├── View history
└── View assessments
    (Read-only)

VIEWER
└── View catalog
    (Read-only)
```

## Performance Considerations

### Query Optimization
- Indexes on frequently filtered columns
- Lazy loading relationships where appropriate
- Pagination for large result sets (default 10, max 100)
- Server-side filtering and aggregation

### Caching Strategy
- Frontend: TanStack Query with 5-minute stale time
- Backend: Database connection pooling
- No application-level cache (PostgreSQL sufficient)

### Scalability
- Async/await for concurrent requests
- Connection pooling
- Database-side aggregation for metrics
- Horizontal scaling ready (stateless API)

## Deployment Architecture

### Docker Compose Services
```
postgres          - PostgreSQL 15 database
backend           - FastAPI application (Python 3.12)
frontend          - React SPA (Vite dev server)
```

### Environment Configuration
```
.env (not committed)
├── DATABASE_URL
├── JWT_SECRET
├── CORS_ORIGINS
└── Feature flags
```

## Error Handling

### API Error Response Format
```json
{
  "detail": {
    "error": "Error message",
    "code": "ERROR_CODE",
    "status": 400
  }
}
```

### Audit Trail on Errors
- All errors logged with context
- User and action recorded
- Traceable to source

---
**Version**: 1.0.0  
**Last Updated**: October 2, 2026
