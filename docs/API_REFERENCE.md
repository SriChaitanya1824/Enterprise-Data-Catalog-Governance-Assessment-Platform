# API Reference

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://governance-api.example.com`

## Authentication
All endpoints require JWT bearer token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "analyst@governance.com",
  "password": "password123"
}

Response 200:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "analyst@governance.com",
    "role": "GOVERNANCE_ANALYST",
    "name": "Data Governance Analyst"
  }
}
```

---

## Data Assets

### List Assets
```http
GET /api/v1/assets?page=1&page_size=20&domain_id=1&classification=Confidential
Authorization: Bearer <token>

Response 200:
{
  "total": 47,
  "items": [
    {
      "id": 1,
      "name": "Customer Risk Dataset",
      "description": "Risk classification dataset...",
      "asset_type": "DATASET",
      "classification": "Confidential",
      "sensitivity": "HIGH",
      "domain_id": 1,
      "domain_name": "Risk Management",
      "owner_id": 2,
      "owner_name": "Risk Data Office",
      "steward_id": 3,
      "steward_name": "Customer Data Governance",
      "lifecycle_status": "ACTIVE",
      "created_at": "2026-01-15T10:00:00Z",
      "updated_at": "2026-11-01T14:22:00Z",
      "metadata_completeness": 94,
      "last_assessment": {
        "score": 94,
        "maturity": "Managed",
        "executed_at": "2026-11-01T10:00:00Z"
      }
    }
  ],
  "page": 1,
  "page_size": 20
}
```

### Get Asset Detail
```http
GET /api/v1/assets/{id}
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "name": "Customer Risk Dataset",
  "description": "Risk classification assigned to customer accounts...",
  "asset_type": "DATASET",
  "classification": "Confidential",
  "sensitivity": "HIGH",
  "domain_id": 1,
  "domain_name": "Risk Management",
  "division_id": 1,
  "division_name": "Risk Management",
  "owner_id": 2,
  "owner_name": "Risk Data Office",
  "steward_id": 3,
  "steward_name": "Customer Data Governance",
  "technical_owner_id": 4,
  "technical_owner_name": "Data Engineering",
  "business_owner_id": 5,
  "business_owner_name": "Head of Risk",
  "lifecycle_status": "ACTIVE",
  "regulatory_relevance": true,
  "critical": true,
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-11-01T14:22:00Z",
  "metadata_completeness": 94,
  "lineage_completeness": 85,
  "fields": [
    {
      "id": 1,
      "name": "customer_id",
      "description": "Unique customer identifier",
      "data_type": "STRING",
      "is_cde": true,
      "business_term_id": 1,
      "business_term_name": "Customer Identifier"
    }
  ],
  "terms": [
    {
      "id": 1,
      "name": "Customer Risk Rating",
      "status": "APPROVED"
    }
  ],
  "regulatory_references": [
    {
      "id": 1,
      "framework": "GDPR",
      "requirement": "GDPR Article 28"
    }
  ]
}
```

### Create Asset
```http
POST /api/v1/assets
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Dataset",
  "description": "Description of the dataset",
  "asset_type": "DATASET",
  "classification": "Confidential",
  "sensitivity": "HIGH",
  "domain_id": 1,
  "division_id": 1,
  "owner_id": 2,
  "steward_id": 3,
  "regulatory_relevance": true
}

Response 201:
{
  "id": 48,
  "name": "New Dataset",
  ...
}
```

### Update Asset
```http
PUT /api/v1/assets/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "description": "Updated description",
  "steward_id": 4
}

Response 200:
{
  "id": 1,
  ...
}
```

### Search Assets
```http
GET /api/v1/search?q=customer+risk&limit=10
Authorization: Bearer <token>

Response 200:
{
  "query": "customer risk",
  "results": [
    {
      "type": "ASSET",
      "id": 1,
      "name": "Customer Risk Dataset",
      "match_score": 0.95
    },
    {
      "type": "TERM",
      "id": 1,
      "name": "Customer Risk Rating",
      "match_score": 0.92
    },
    {
      "type": "CDE",
      "id": 2,
      "name": "risk_rating",
      "match_score": 0.88
    }
  ]
}
```

---

## Governance Assessment

### Run Assessment
```http
POST /api/v1/assessments/run/{asset_id}?user_id=1
Authorization: Bearer <token>

Response 200:
{
  "id": 42,
  "asset_id": 1,
  "score": 94,
  "maturity": "Managed",
  "requirements_checked": 8,
  "requirements_passed": 7,
  "executed_at": "2026-11-01T10:00:00Z",
  "executed_by": 1,
  "requirements": [
    {
      "code": "GOV-001",
      "description": "Data Owner assigned",
      "passed": true,
      "reason": "Owner: Risk Data Office"
    },
    {
      "code": "GOV-008",
      "description": "Review date current",
      "passed": false,
      "reason": "Next review date not set"
    }
  ]
}
```

### Get Assessment History
```http
GET /api/v1/assessments/{asset_id}/history?limit=10
Authorization: Bearer <token>

Response 200:
{
  "asset_id": 1,
  "asset_name": "Customer Risk Dataset",
  "history": [
    {
      "id": 42,
      "executed_at": "2026-11-01T10:00:00Z",
      "score": 94,
      "maturity": "Managed",
      "requirements_passed": 7,
      "gap_count": 0
    },
    {
      "id": 41,
      "executed_at": "2026-10-15T10:00:00Z",
      "score": 88,
      "maturity": "Managed",
      "requirements_passed": 7,
      "gap_count": 1
    },
    {
      "id": 40,
      "executed_at": "2026-10-01T10:00:00Z",
      "score": 82,
      "maturity": "Managed",
      "requirements_passed": 6,
      "gap_count": 2
    }
  ]
}
```

### Get Assessment Details
```http
GET /api/v1/assessments/{assessment_id}
Authorization: Bearer <token>

Response 200:
{
  "id": 42,
  "asset_id": 1,
  "score": 94,
  "maturity": "Managed",
  "executed_at": "2026-11-01T10:00:00Z",
  "executed_by": 1,
  "requirements": [
    {
      "id": 1,
      "assessment_id": 42,
      "requirement_code": "GOV-001",
      "requirement_description": "Data Owner assigned",
      "passed": true,
      "outcome_notes": "Owner: Risk Data Office"
    }
  ],
  "gaps": [
    {
      "id": 101,
      "assessment_id": 42,
      "category": "Review",
      "severity": "Medium",
      "description": "Next review date not set",
      "status": "Open"
    }
  ]
}
```

---

## Governance Gaps

### List Gaps
```http
GET /api/v1/gaps?asset_id=1&status=Open&severity=High&limit=20
Authorization: Bearer <token>

Response 200:
{
  "total": 3,
  "items": [
    {
      "id": 101,
      "asset_id": 1,
      "asset_name": "Customer Risk Dataset",
      "category": "Review",
      "severity": "Medium",
      "description": "Next review date not set",
      "status": "Open",
      "created_at": "2026-10-01T08:30:00Z",
      "assigned_to": null,
      "resolution_notes": "Set next_review_date to 2027-10-15"
    }
  ]
}
```

### Get Gap Detail
```http
GET /api/v1/gaps/{gap_id}
Authorization: Bearer <token>

Response 200:
{
  "id": 101,
  "asset_id": 1,
  "category": "Review",
  "severity": "Medium",
  "description": "Next review date not set",
  "status": "Open",
  "created_at": "2026-10-01T08:30:00Z",
  "created_by": "system",
  "assigned_to": null,
  "resolution_notes": "Set next_review_date to 2027-10-15",
  "expected_resolution_date": null
}
```

### Update Gap Status
```http
PUT /api/v1/gaps/{gap_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "In Progress",
  "assigned_to": 2,
  "resolution_notes": "Owner updating review date",
  "expected_resolution_date": "2026-11-15T00:00:00Z"
}

Response 200:
{
  "id": 101,
  "status": "In Progress",
  "assigned_to": 2,
  ...
}
```

---

## Business Glossary

### List Terms
```http
GET /api/v1/glossary?status=APPROVED&domain_id=1&limit=20
Authorization: Bearer <token>

Response 200:
{
  "total": 42,
  "items": [
    {
      "id": 1,
      "name": "Customer Risk Rating",
      "definition": "Risk classification assigned to customer accounts...",
      "status": "APPROVED",
      "owner_id": 5,
      "owner_name": "Head of Risk",
      "steward_id": 3,
      "steward_name": "Customer Data Governance",
      "created_at": "2026-01-20T10:00:00Z",
      "approved_at": "2026-01-25T15:30:00Z",
      "approved_by": 1,
      "related_assets": 3,
      "related_fields": 2
    }
  ]
}
```

### Get Term Detail
```http
GET /api/v1/glossary/{term_id}
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "name": "Customer Risk Rating",
  "definition": "Risk classification assigned to customer accounts...",
  "status": "APPROVED",
  "owner_id": 5,
  "steward_id": 3,
  "related_assets": [
    {
      "id": 1,
      "name": "Customer Risk Dataset",
      "type": "ASSET"
    }
  ],
  "related_fields": [
    {
      "id": 2,
      "name": "risk_rating",
      "asset_id": 1,
      "asset_name": "Customer Risk Dataset"
    }
  ],
  "relationships": [
    {
      "id": 1,
      "related_term_id": 2,
      "related_term_name": "Customer Profile",
      "relationship_type": "Parent"
    }
  ]
}
```

### Create Term
```http
POST /api/v1/glossary
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Business Term",
  "definition": "Definition of the term",
  "owner_id": 5,
  "steward_id": 3
}

Response 201:
{
  "id": 43,
  "name": "New Business Term",
  "status": "PENDING_APPROVAL",
  ...
}
```

### Approve Term
```http
PUT /api/v1/glossary/{term_id}/approve
Authorization: Bearer <token>
Content-Type: application/json

{
  "approved": true,
  "notes": "Approved by data governance"
}

Response 200:
{
  "id": 43,
  "status": "APPROVED",
  "approved_by": 1,
  "approved_at": "2026-11-01T14:00:00Z"
}
```

---

## Critical Data Elements

### List CDEs
```http
GET /api/v1/cdes?domain_id=1&classification=Confidential&limit=20
Authorization: Bearer <token>

Response 200:
{
  "total": 12,
  "items": [
    {
      "id": 1,
      "name": "customer_id",
      "asset_id": 1,
      "asset_name": "Customer Risk Dataset",
      "classification": "Public",
      "description": "Unique customer identifier",
      "business_term_id": 1,
      "business_term_name": "Customer Identifier",
      "usage_count": 7,
      "last_assessed": "2026-11-01T10:00:00Z",
      "governance_score": 94,
      "maturity": "Managed"
    }
  ]
}
```

### Get CDE Detail
```http
GET /api/v1/cdes/{cde_id}
Authorization: Bearer <token>

Response 200:
{
  "id": 1,
  "name": "customer_id",
  "asset_id": 1,
  "classification": "Public",
  "usage_across_assets": 7,
  "upstream_lineage": [
    {
      "id": 10,
      "name": "Customer Master",
      "type": "SOURCE"
    }
  ],
  "downstream_usage": [
    {
      "id": 11,
      "name": "Risk Scoring Pipeline",
      "type": "PIPELINE"
    }
  ],
  "quality_metrics": {
    "completeness": 99.8,
    "uniqueness": 100.0,
    "timeliness": "Real-time"
  }
}
```

---

## Certification

### Check Eligibility
```http
POST /api/v1/certifications/check-eligibility/{asset_id}
Authorization: Bearer <token>

Response 200:
{
  "eligible": true,
  "errors": [],
  "completeness": 94,
  "score": 94,
  "maturity": "Managed",
  "requirements_met": 7,
  "requirements_total": 8
}
```

### List Certifications
```http
GET /api/v1/certifications?status=CERTIFIED&limit=20
Authorization: Bearer <token>

Response 200:
{
  "total": 11,
  "items": [
    {
      "id": 1,
      "asset_id": 1,
      "asset_name": "Customer Risk Dataset",
      "status": "CERTIFIED",
      "certified_date": "2026-10-15T14:00:00Z",
      "certified_by": 1,
      "expiry_date": "2027-10-15T00:00:00Z",
      "days_until_expiry": 349,
      "review_count": 1,
      "next_review_date": "2027-10-15T00:00:00Z"
    }
  ]
}
```

### Certify Asset
```http
POST /api/v1/certifications/{asset_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "notes": "Meets all governance requirements",
  "expiry_days": 365
}

Response 201:
{
  "id": 1,
  "asset_id": 1,
  "status": "CERTIFIED",
  "certified_date": "2026-11-01T14:22:00Z",
  "certified_by": 1,
  "expiry_date": "2027-11-01T00:00:00Z",
  "next_review_date": "2027-11-01T00:00:00Z"
}
```

### Revoke Certification
```http
PUT /api/v1/certifications/{certification_id}/revoke
Authorization: Bearer <token>
Content-Type: application/json

{
  "reason": "Governance gap identified",
  "notes": "Revoked due to missing review date"
}

Response 200:
{
  "id": 1,
  "status": "CERTIFICATION_EXPIRED",
  "revoked_at": "2026-11-01T14:30:00Z",
  "revoke_reason": "Governance gap identified"
}
```

---

## Dashboard & Metrics

### Dashboard Metrics
```http
GET /api/v1/dashboard/metrics
Authorization: Bearer <token>

Response 200:
{
  "assets": {
    "total": 47,
    "critical": 12,
    "by_classification": {
      "Public": 15,
      "Internal": 20,
      "Confidential": 12
    },
    "by_lifecycle": {
      "ACTIVE": 45,
      "ARCHIVED": 2
    }
  },
  "governance": {
    "average_score": 87.3,
    "assets_with_owners": 45,
    "assets_certified": 11,
    "open_gaps": 3,
    "high_severity_gaps": 0
  },
  "glossary": {
    "total_terms": 42,
    "approved_terms": 38,
    "pending_approval": 4
  },
  "cdes": {
    "total": 12,
    "with_definitions": 12,
    "governance_score_average": 92.5
  },
  "divisions": [
    {
      "name": "Risk Management",
      "assets": 12,
      "average_score": 89,
      "certified_count": 11
    }
  ],
  "maturity_distribution": {
    "Initial": 2,
    "Developing": 5,
    "Defined": 15,
    "Managed": 20,
    "Optimized": 5
  }
}
```

### Divisional Metrics
```http
GET /api/v1/divisions/{division_id}/metrics
Authorization: Bearer <token>

Response 200:
{
  "division_id": 1,
  "division_name": "Risk Management",
  "assets": 12,
  "owners_assigned": 12,
  "stewards_assigned": 11,
  "classified": 12,
  "certified": 11,
  "average_completeness": 92.5,
  "average_governance_score": 89.0,
  "open_gaps": 1,
  "trend": "improving"
}
```

---

## Audit Trail

### Get Audit Log
```http
GET /api/v1/audit?entity_type=DataAsset&entity_id=1&limit=50
Authorization: Bearer <token>

Response 200:
{
  "total": 12,
  "items": [
    {
      "id": 1001,
      "timestamp": "2026-11-01T14:22:00Z",
      "user_id": 1,
      "user_email": "analyst@governance.com",
      "entity_type": "DataAsset",
      "entity_id": 1,
      "action": "UPDATE",
      "changes": [
        {
          "field": "certification_status",
          "old_value": null,
          "new_value": "CERTIFIED"
        },
        {
          "field": "last_certified_date",
          "old_value": null,
          "new_value": "2026-11-01T14:22:00Z"
        }
      ]
    }
  ]
}
```

---

## Lineage

### Get Asset Lineage
```http
GET /api/v1/lineage/{asset_id}?direction=both&depth=3
Authorization: Bearer <token>

Response 200:
{
  "asset_id": 1,
  "upstream": [
    {
      "id": 10,
      "name": "Customer Master",
      "type": "DATASET",
      "transformation": "Extract customer_id"
    }
  ],
  "downstream": [
    {
      "id": 11,
      "name": "Risk Scoring Pipeline",
      "type": "PIPELINE"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Asset not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- Standard: 100 requests per minute
- Burst: 200 requests per minute
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Pagination

All list endpoints support:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `sort_by`: Sort field (default: created_at)
- `sort_order`: asc or desc (default: desc)

---

**API Reference Version**: 1.0  
**Last Updated**: October 2, 2026  
**OpenAPI Docs**: http://localhost:8000/api/docs
