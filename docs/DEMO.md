# Demo Walkthrough: Enterprise Data Catalog & Governance Assessment

## Quick Start (5 minutes)

### Prerequisites
- Docker and Docker Compose installed
- Terminal access

### Step 1: Start the Platform
```bash
cd /Users/jyothi/Desktop/CODe/DeutchBank/3
docker compose up --build
```

**Wait for**:
- ✅ `postgres_1` - database ready
- ✅ `backend_1` - "Application startup complete"
- ✅ `frontend_1` - "Local: http://localhost:5173/"

### Step 2: Access the Platform
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

### Step 3: Login
Use any demo credential:
```
Email: analyst@governance.com
Password: password123
Role: GOVERNANCE_ANALYST (can run assessments)
```

---

## Full Demo Scenario: Customer Risk Rating (15 minutes)

### Scene 1: Discover Data Assets (2 minutes)

**Goal**: Find the "Customer Risk Dataset" in the catalog

**Steps**:
1. From Dashboard, click **Search**
2. Enter: `Customer Risk`
3. Observe results:
   - ✅ Data Asset: "Customer Risk Dataset" (marked Critical, Confidential)
   - ✅ Business Terms: "Customer Risk Rating" (defined)
   - ✅ CDE: "risk_rating" (linked)

**What to Highlight**:
- Full-text search across multiple entity types
- Asset metadata visible: Domain (Risk Management), Division (Risk), Owner (Risk Data Office)
- Classification clearly shown: Confidential
- Link between asset and business terms

---

### Scene 2: Understand Governance Status (3 minutes)

**Goal**: See current governance maturity

**Steps**:
1. Click on **"Customer Risk Dataset"** in search results
2. View Asset Detail page showing:
   - **Overview Tab**: Full metadata
   - **Governance Tab**: Last assessment score (94% - Managed)
   - **Fields Tab**: 3 fields including 2 CDEs
   - **Ownership**: 
     - Owner: "Risk Data Office Team"
     - Steward: "Customer Data Governance"
     - Technical Owner: "Data Engineering"

**What to Highlight**:
- Clear ownership structure (Business owner, Data owner, Steward, Technical owner)
- Last assessment: 94% score, Managed maturity level
- Assessment date: Shows when governance was last evaluated
- No gaps currently (all requirements met)

---

### Scene 3: Run Governance Assessment (4 minutes)

**Goal**: Execute assessment and see scoring logic

**Steps**:
1. On Asset Detail, click **"Run Assessment"** button (Governance tab)
2. Observe assessment execution (frontend shows loading)
3. Results displayed:

```
Assessment Score: 94% ✓ MANAGED

Requirements Status:
✓ GOV-001: Data Owner assigned (Risk Data Office Team)
✓ GOV-002: Data Steward assigned (Customer Data Governance)
✓ GOV-003: Description >= 20 chars (87 characters found)
✓ GOV-004: Classification assigned (Confidential)
✓ GOV-005: CDE definitions (2/2 CDEs have approved terms)
✓ GOV-006: Regulatory mapped (GDPR, GLBA references found)
✓ GOV-007: Lineage completeness >= 50% (85% completeness)
✓ GOV-008: Review date current (2026-12-15)

Maturity Level: MANAGED
- 95%+ of governance requirements met
- Suitable for critical business use
- Ready for certification

Recommended Next Steps:
1. Continue regular reviews (quarterly)
2. Monitor lineage changes
3. Update regulatory mappings annually
```

**What to Highlight**:
- **Deterministic**: Same asset always scores 94% (if data unchanged)
- **Explainable**: Each requirement shown with specific data used in evaluation
- **Actionable**: Gaps would show specific fixes needed
- **Non-punitive**: Score reflects metadata completeness, not data quality

---

### Scene 4: View Assessment History (2 minutes)

**Goal**: Show trend analysis and improvement tracking

**Steps**:
1. On Governance tab, click **"Assessment History"**
2. See table:
   ```
   Date           Score  Maturity    Gap Count
   2026-10-01     82%    Managed     1 gap (review date missing)
   2026-10-15     88%    Managed     0 gaps
   2026-11-01     94%    Managed     0 gaps
   ```
3. Optionally view chart showing score trend

**What to Highlight**:
- Platform tracks improvement over time
- 82% → 94% shows governance maturation process
- Gap reduction visible (1 gap → 0 gaps)
- Useful for governance reporting and dashboards

---

### Scene 5: View Related Glossary Terms (2 minutes)

**Goal**: Understand business context through glossary

**Steps**:
1. Click on **"Glossary"** from main menu
2. Search: `Customer Risk Rating`
3. View term:
   ```
   Business Term: Customer Risk Rating
   Status: APPROVED (approved by Data Governance)
   
   Definition: 
   "Risk classification assigned to customer accounts based on 
    regulatory compliance, transaction patterns, and behavioral 
    analysis. Used for customer segmentation, pricing, and controls."
   
   Linked Assets: 3
   - Customer Risk Dataset (asset)
   - Risk Scoring Rules (asset)
   - Customer Master (asset)
   
   Relationships:
   - Parent: "Customer Profile"
   - Related To: "Regulatory Classification"
   - Synonym: "Customer Risk Segment"
   
   Owner: Customer Data Governance
   Steward: Data Analytics Team
   ```

**What to Highlight**:
- Glossary creates business context
- Relationships show term connections
- Linked to data assets in catalog
- Governance ownership visible in glossary too

---

### Scene 6: Explore Critical Data Elements (2 minutes)

**Goal**: Show CDE-specific governance

**Steps**:
1. From Dashboard or Menu, go to **"Critical Data Elements"**
2. Filter by domain: "Risk Management"
3. See 2 CDEs:
   - `customer_id` (Data Type: STRING, Classification: Public)
   - `risk_rating` (Data Type: STRING, Classification: Confidential)
4. Click on `risk_rating` CDE
5. View:
   - Definition (linked business term)
   - Usage: 7 data assets
   - Lineage: Transforms from 3 upstream sources
   - Quality SLA: 99.5% completeness

**What to Highlight**:
- CDEs treated as first-class governance objects
- Each CDE has assessment just like assets
- Lineage tracing through CDE usage
- Quality metrics associated with CDEs

---

### Scene 7: View Dashboard Metrics (2 minutes)

**Goal**: Show governance maturity at portfolio level

**Steps**:
1. Click **"Dashboard"** from main menu
2. View key metrics cards:
   ```
   Total Assets: 47
   Assets with Owners: 45 (95.7%)
   
   Critical Assets: 12
   Certified: 11 (91.7%)
   
   Governance Gaps Open: 3
   High-Severity Gaps: 0
   
   Avg. Governance Score: 87.3% (Managed)
   Metadata Completeness: 94.1%
   ```
3. View Division Adoption Table:
   ```
   Division              Assets  Avg Score  Owners  Certified
   Risk Management         12     89%        12      11
   Retail Banking          18     86%        16      12
   Corporate Banking       10     88%        10       8
   Customer Management      7     83%         6       4
   Finance                  0      -          -       -
   ```

**What to Highlight**:
- Portfolio-level governance visibility
- Divisional comparisons (without ranking)
- Gap metrics showing governance issues
- Certification tracking by division

---

### Scene 8: Inspect Governance Gaps (2 minutes)

**Goal**: See how gaps guide improvement

**Steps**:
1. Click **"Governance Gaps"** from main menu
2. Filter by Status: "Open"
3. See example gaps:
   ```
   Gap #1: Missing Review Date
   Asset: Finance Regulatory Dataset
   Category: Review
   Severity: Medium
   Status: Open (since Oct 15)
   Resolution: Set next_review_date to 2027-10-15
   
   Gap #2: Missing CDE Definition
   Asset: Payment Processing Dataset
   Category: Business Context
   Severity: Medium
   Status: In Progress (assigned to Steward)
   Resolution: Steward must create business term and link
   
   Gap #3: No Regulatory Mapping
   Asset: Customer PII Dataset
   Category: Regulatory
   Severity: High
   Status: Open
   Resolution: Link to GDPR and CCPA regulatory references
   ```
4. Click on "Missing Review Date" gap
5. See:
   - How to resolve (specific action)
   - Who is responsible (data owner)
   - Impact if not resolved (will show in next assessment)

**What to Highlight**:
- Gaps are not failures, but improvement opportunities
- Each gap has specific resolution path
- Severity helps prioritization
- Status tracking shows governance activities

---

### Scene 9: Demonstrate Certification Workflow (2 minutes)

**Goal**: Show asset certification eligibility and process

**Steps**:
1. From Assessments, find asset with 90%+ score
2. Click **"Certify Asset"** button
3. See eligibility check:
   ```
   Certification Eligibility Check:
   ✓ Owner assigned
   ✓ Steward assigned
   ✓ Classification complete
   ✓ Metadata >= 80% complete (94% current)
   
   Status: ELIGIBLE FOR CERTIFICATION
   ```
4. Confirm certification (note: this would trigger workflow)
5. See certification record:
   ```
   Certification Status: CERTIFIED
   Certified Date: 2026-10-15
   Certified By: Data Governance (system)
   Expiry Date: 2027-10-15
   Review Schedule: Annual
   ```

**What to Highlight**:
- Certification is backend-validated (not manual)
- Clear eligibility criteria
- Expiry tracking enforces continuous governance
- Audit trail of certification decisions

---

### Scene 10: Review Audit Trail (1 minute)

**Goal**: Show governance accountability

**Steps**:
1. On Asset Detail page, scroll to **"Audit History"** tab
2. See changes:
   ```
   Date/Time              User                Change
   2026-11-01 14:22:00   analyst@gov.com     Certification created
                                             Certification.status: null -> CERTIFIED
                                             Certification.expiry: null -> 2027-10-15
   
   2026-10-15 09:45:00   owner@risk.com      Updated field metadata
                                             DataField.description: "" -> "..."
                                             DataAsset.metadata_completeness: 82% -> 94%
   
   2026-10-01 08:30:00   steward@gov.com     Created governance assessment
                                             GovernanceAssessment.score: 82%
                                             GovernanceAssessment.maturity: Managed
   ```

**What to Highlight**:
- Complete audit trail of all changes
- Before/after values shown
- User responsibility clear
- Useful for compliance and governance reviews

---

## Talking Points for Governance Interviews

### 1. Governance Assessment Philosophy
- "Score reflects metadata completeness, not data quality"
- "Assessment is deterministic - same input always produces same score"
- "Gap detection is automatic - not manual judgment"

### 2. Maturity Model
- "We use 5-tier maturity levels to show governance evolution, not to rank divisions"
- "Initial → Optimized shows clear progression path"
- "Maturity is about process, not about data"

### 3. Accountability Structure
- "Clear ownership model: Business owner, Data owner, Technical owner, Steward"
- "Each role has specific governance responsibilities"
- "Audit trail shows who made what decisions"

### 4. Gap-Driven Improvement
- "Gaps emerge from failed requirements, not subjective judgment"
- "Severity classification prioritizes effort"
- "Gap status workflow (Open → In Progress → Resolved) tracks governance activities"

### 5. Continuous Monitoring
- "Assessments run regularly to detect governance drift"
- "History shows improvement trajectory"
- "Certification expiry enforces regular governance reviews"

### 6. Business Glossary Integration
- "Business terms provide business context for technical data"
- "Glossary relationships map business concepts"
- "Terms linked to data assets and fields"

### 7. Critical Data Element Focus
- "CDEs are governance priority - treated as first-class objects"
- "CDE lineage shows downstream impact of source changes"
- "Quality metrics tied to CDE governance"

### 8. Regulatory Compliance
- "Regulatory references link business requirements to data"
- "Regulatory data gets stricter governance requirements"
- "Audit trail provides compliance documentation"

---

## Common Questions & Answers

**Q: Why does the score stay at 94%?**  
A: The platform uses deterministic scoring. The Customer Risk Dataset meets 7 out of 8 requirements, so it consistently scores 94%. If the owner were removed, it would immediately drop to 87.5%. Scores only change when underlying data changes.

**Q: How is this different from a data quality tool?**  
A: This is governance, not quality. We're measuring whether governance processes are in place (owner assigned, metadata documented, reviews scheduled), not whether the data is accurate or complete. Quality is a separate concern tracked in quality metrics.

**Q: Who owns governance accountability?**  
A: The Data Owner (assigned at asset creation) owns the governance score. They're responsible for ensuring requirements are met. The Data Steward manages day-to-day governance activities. The Business Owner provides business context.

**Q: How do you prevent "assessment gaming" where teams fake metadata?**  
A: Audit trail captures who entered data and when. Regular reviews and steward verification are checks. For critical assets, certification requires review by independent Reviewer role. Governance is about integrity.

**Q: Can this scale to thousands of assets?**  
A: Yes. Assessment engine runs deterministic checks (no AI/ML needed). Database is indexed for scale. Airflow DAGs can schedule assessments across large portfolios. Typical assessment takes <5 seconds per asset.

**Q: How does this integrate with existing systems?**  
A: This is an integration hub. Metadata flows in from source systems (ETL, databases, data catalogs). Assessment engine consumes this metadata. Results flow to governance dashboards, risk systems, and compliance reporting.

---

## Troubleshooting

**Services won't start**:
```bash
# Clear volumes and restart
docker compose down -v
docker compose up --build
```

**Can't login**:
- Verify database initialized: `docker compose ps`
- Check backend logs: `docker compose logs backend`
- Reseed data: `docker exec 3-backend-1 python seed_data.py`

**API returns errors**:
- Check API docs: http://localhost:8000/api/docs
- Verify token: Login first to get JWT in response
- Check headers: `Authorization: Bearer <token>`

**Frontend blank**:
- Check Vite dev server logs: `docker compose logs frontend`
- Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Verify port 5173 is accessible: `curl http://localhost:5173`

---

## Next Steps After Demo

1. **Run Full Assessment Suite**
   - Execute assessments on all 47 demo assets
   - Show divisional maturity comparison
   - Identify common gap patterns

2. **Create Custom Governance Requirements**
   - Add organization-specific requirements
   - Adjust maturity thresholds
   - Customize gap severity rules

3. **Load Real Data**
   - Connect to actual PostgreSQL database
   - Ingest metadata from data catalog/lineage tool
   - Run assessments on real assets

4. **Set Up Airflow Orchestration**
   - Schedule daily metadata discovery
   - Run assessments on weekly schedule
   - Monitor certification expiry dates

5. **Integrate with Compliance Tools**
   - Export assessment results to risk system
   - Send gap notifications to stakeholders
   - Provide audit reports to compliance team

---

**Demo Script Version**: 1.0  
**Last Updated**: October 2, 2026  
**Estimated Duration**: 15 minutes
