# Backend Security Implementation TODO

**Date:** 2025-12-27
**Priority:** CRITICAL for EU B2B Sales
**Context:** Due diligence level 3 audit feedback - property_name exposure risks

---

## 🚨 CRITICAL: PDF Example Contradiction (BLOCKER)

**Status:** ❌ **BLOCKS DEPLOYMENT** - Must fix before going live

### Problem
Old PDF example showed report code: `GG-20251225150233-VUTG`
- Format: GG-YYYYMMDDHHMMSS-XXXX (timestamp + 4 char suffix)
- **Contradicts documentation** which claims "cryptographically secure random format (GG-{16+ chars})"
- **Security vulnerability**: Timestamp makes enumeration trivial (attacker knows date → can guess all codes)
- **Entropy**: Only 62^4 = ~14M combinations in suffix (breakable in minutes)

### Action Taken
- ✅ Deleted old PDF: `GreenGate-Fazenda-Teste-Talhao-12.pdf`
- ✅ Updated all HTML docs to show correct format: `GG-a7f3k9m2p5q8` (16 random chars)

### Required
**BEFORE DEPLOYMENT:**
1. Generate new example PDF with high-entropy code: `GG-a7f3k9m2p5q8r1t4` (16+ random chars)
2. Use property_name: "Farm #12345" (not "Fazenda Teste")
3. Verify QR code points to correct verification URL
4. Upload to repo as: `GreenGate-Example-Report.pdf`

**Test command:**
```bash
# Verify new PDF uses secure format
pdftotext GreenGate-Example-Report.pdf - | grep "GG-"
# Should show: GG-a7f3k9m2p5q8r1t4 (NOT GG-20251225...)
```

---

## 🔴 CRITICAL: Two-Level Verification System

### Current State (INSECURE)
```python
# Single public endpoint exposes all data
@app.get("/reports/verify/{report_code}")
def verify_report(report_code: str):
    return {
        "verified": true,
        "property_name": "Farm ABC",  # ❌ Sensitive data exposed publicly
        "pdf_url": "...",              # ❌ Direct access to PDF
        "metadata": {...}              # ❌ CAR, internal IDs exposed
    }
```

**Problems:**
1. Property_name free text field = "potentially sensitive data" in audits
2. Anyone with report code gets full details
3. Enumeration risk if codes are predictable

---

### Required Implementation

#### 1. Split into Two Endpoints

**PUBLIC Endpoint (No Auth Required):**
```python
@app.get("/reports/verify/public/{report_code}")
@limiter.limit("10/minute")  # Aggressive rate limiting
def verify_report_public(report_code: str):
    """Minimal info for public QR code verification"""
    report = db.get_report(report_code)

    if not report:
        raise HTTPException(404, "Report not found")

    return {
        "verified": True,
        "report_code": report_code,
        "property_name": "[REDACTED]",  # ✅ Always redacted
        "validation_date": report.created_at,
        "score": report.score,
        "risk_level": report.risk_level,
        # ❌ NO pdf_url, NO metadata, NO CAR
    }
```

**AUTHENTICATED Endpoint (Requires API Key):**
```python
@app.get("/reports/verify/full/{report_code}")
@require_api_key  # Must be owner's API key
def verify_report_full(report_code: str, api_key: str = Header(...)):
    """Full details only for authenticated client"""
    report = db.get_report(report_code)

    # Verify requester owns this validation
    if report.api_key_id != get_api_key_id(api_key):
        raise HTTPException(403, "Not authorized to view full details")

    return {
        "verified": True,
        "report_code": report_code,
        "property_name": report.property_name or "N/A",  # ✅ Only for owner
        "validation_date": report.created_at,
        "score": report.score,
        "risk_level": report.risk_level,
        "pdf_url": generate_signed_url(report.pdf_path, expires_in=7*24*3600),
        "metadata": report.metadata,  # ✅ Full details
        "geometry": report.geometry
    }
```

---

## 🔴 CRITICAL: High-Entropy Report Codes

### Current State (VULNERABLE)
```python
# Predictable format allows enumeration
report_code = f"GG-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
# Result: GG-20251227-1234 (easy to enumerate)
```

**Attack:**
```python
# Attacker can enumerate all reports
for i in range(1000, 9999):
    try_code = f"GG-20251227-{i}"
    response = requests.get(f"/reports/verify/{try_code}")
    if response.status_code == 200:
        print(f"Found report: {try_code}")
```

---

### Required Implementation

```python
import secrets

def generate_report_code():
    """Generate cryptographically secure random code"""
    # 16 characters = 128 bits entropy (base62: a-z, A-Z, 0-9)
    random_part = secrets.token_urlsafe(12)[:16]  # URL-safe base64
    return f"GG-{random_part}"

# Example output: GG-a7f3k9m2p5q8r1t4
# Total combinations: 62^16 ≈ 4.7 × 10^28 (impossible to enumerate)
```

**Migration:**
```sql
-- Update existing reports to use new format
UPDATE validations
SET report_code = CONCAT('GG-', SUBSTRING(MD5(RANDOM()::text), 1, 16))
WHERE report_code LIKE 'GG-202%';
```

---

## 🔴 CRITICAL: Rate Limiting on Public Verify

### Current State
No rate limiting on `/reports/verify/{code}` endpoint.

### Required Implementation

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/reports/verify/public/{report_code}")
@limiter.limit("10/minute")  # 10 requests per minute per IP
@limiter.limit("100/hour")   # 100 requests per hour per IP
def verify_report_public(report_code: str, request: Request):
    # ... implementation
```

**Additional Protection:**
```python
# Block after 5 consecutive 404s from same IP
@app.middleware("http")
async def block_enumeration_attempts(request: Request, call_next):
    ip = get_remote_address(request)

    if request.url.path.startswith("/reports/verify/"):
        fail_count = redis.get(f"verify_fails:{ip}") or 0

        if int(fail_count) > 5:
            return Response("Too many failed attempts", status_code=429)

        response = await call_next(request)

        if response.status_code == 404:
            redis.incr(f"verify_fails:{ip}")
            redis.expire(f"verify_fails:{ip}", 3600)  # Reset after 1 hour

        return response
```

---

## 🟡 MEDIUM: Input Validation - Reject CPF/CNPJ Patterns

### Current State
No validation on metadata fields - users could accidentally include CPF/CNPJ.

### Required Implementation

```python
import re

CPF_PATTERN = re.compile(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}')
CNPJ_PATTERN = re.compile(r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}')
NAME_PATTERN = re.compile(r'\b[A-ZÀÁÂÃÉÊÍÓÔÕÚ][a-zàáâãéêíóôõú]+\s+[A-ZÀÁÂÃÉÊÍÓÔÕÚ][a-zàáâãéêíóôõú]+\b')

def validate_no_personal_data(text: str, field_name: str):
    """Reject if text contains CPF, CNPJ, or person names"""
    if CPF_PATTERN.search(text):
        raise HTTPException(
            400,
            f"{field_name} contains CPF pattern. Personal data not allowed. Use anonymous IDs only."
        )

    if CNPJ_PATTERN.search(text):
        raise HTTPException(
            400,
            f"{field_name} contains CNPJ pattern. Personal data not allowed. Use anonymous IDs only."
        )

    # Warn if looks like person name (heuristic)
    if NAME_PATTERN.search(text):
        logger.warning(
            f"Possible person name in {field_name}: {text}. User: {api_key_id}"
        )

@app.post("/validations")
def create_validation(data: ValidationRequest, api_key: str = Header(...)):
    # Validate property_name
    if data.property_name:
        validate_no_personal_data(data.property_name, "property_name")

    # Validate metadata fields
    if data.metadata:
        for key, value in data.metadata.items():
            if isinstance(value, str):
                validate_no_personal_data(value, f"metadata.{key}")

    # ... rest of implementation
```

---

## 🟡 MEDIUM: Automatic Property Name Redaction

### Current State
Relies on frontend to not send real names - backend stores/returns whatever is sent.

### Required Implementation

```python
def sanitize_property_name(name: str) -> str:
    """Redact property_name for public verification"""
    # Allow only pattern: "Farm #123", "Property A", etc.
    safe_pattern = re.compile(r'^(Farm|Property|Fazenda|Propriedade)\s*#?[A-Z0-9\-]+$', re.IGNORECASE)

    if not name or name.strip() == "":
        return None

    if safe_pattern.match(name.strip()):
        return name.strip()  # Keep safe patterns

    # Redact anything else
    logger.warning(f"Redacting unsafe property_name: {name}")
    return "[REDACTED]"

@app.post("/validations")
def create_validation(data: ValidationRequest):
    # Sanitize on input
    if data.property_name:
        data.property_name = sanitize_property_name(data.property_name)

    # ... store in database
```

**Alternative Approach (More Aggressive):**
```python
# Always redact in public endpoint, regardless of content
@app.get("/reports/verify/public/{report_code}")
def verify_report_public(report_code: str):
    report = db.get_report(report_code)
    return {
        "property_name": "[REDACTED]",  # Always redact, no exceptions
        # ... other fields
    }
```

---

## 🟡 MEDIUM: Signed PDF URLs with Expiration

### Current State
```python
pdf_url = f"https://api.greengate.com.br/reports/{report.pdf_id}.pdf"
# ❌ Anyone with URL can access forever
```

### Required Implementation

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("PDF_SIGNING_KEY")  # Rotate monthly

def generate_signed_pdf_url(pdf_path: str, expires_in: int = 7*24*3600):
    """Generate signed URL that expires in 7 days"""
    expiration = datetime.utcnow() + timedelta(seconds=expires_in)

    token = jwt.encode({
        "pdf_path": pdf_path,
        "exp": expiration
    }, SECRET_KEY, algorithm="HS256")

    return f"https://api.greengate.com.br/reports/download?token={token}"

@app.get("/reports/download")
def download_pdf(token: str):
    """Download PDF with signed token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        pdf_path = payload["pdf_path"]

        # Check expiration (jwt.decode already validates exp)
        return FileResponse(pdf_path, media_type="application/pdf")

    except jwt.ExpiredSignatureError:
        raise HTTPException(410, "PDF link expired (7 days max)")
    except jwt.InvalidTokenError:
        raise HTTPException(403, "Invalid PDF token")
```

---

## 🟢 LOW: Audit Logging

### Required Implementation

```python
import logging

logger = logging.getLogger("audit")

@app.get("/reports/verify/public/{report_code}")
def verify_report_public(report_code: str, request: Request):
    logger.info(
        "PUBLIC_VERIFY",
        extra={
            "report_code": report_code,
            "ip": get_remote_address(request),
            "user_agent": request.headers.get("user-agent"),
            "timestamp": datetime.utcnow(),
            "found": report is not None
        }
    )
    # ... implementation

# Monitor for enumeration patterns
# Alert if same IP gets >50% 404 rate on verify endpoint
```

---

## 📋 Implementation Checklist

**Week 1 (MUST DO):**
- [ ] Generate high-entropy report codes (`secrets.token_urlsafe`)
- [ ] Migrate existing report codes to new format
- [ ] Split `/reports/verify` into `/verify/public` and `/verify/full`
- [ ] Always redact property_name in public endpoint
- [ ] Add rate limiting (10/min, 100/hour) to public verify
- [ ] Block IPs after 5 consecutive 404s

**Week 2 (SHOULD DO):**
- [ ] Add CPF/CNPJ pattern validation on POST `/validations`
- [ ] Implement signed PDF URLs with 7-day expiration
- [ ] Add audit logging for all verify attempts
- [ ] Add monitoring for enumeration patterns

**Week 3 (NICE TO HAVE):**
- [ ] Add property_name sanitization (allow only "Farm #123" patterns)
- [ ] Implement IP allowlist for API key owners
- [ ] Add CAPTCHA for public verify endpoint (if abuse detected)
- [ ] Create admin dashboard to review flagged reports

---

## 🧪 Testing

```bash
# Test 1: Public verify should redact property_name
curl https://api.greengate.com.br/reports/verify/public/GG-a7f3k9m2p5q8
# Expected: {"property_name": "[REDACTED]", ...}

# Test 2: Full verify should require API key
curl https://api.greengate.com.br/reports/verify/full/GG-a7f3k9m2p5q8
# Expected: 401 Unauthorized

curl -H "x-api-key: test123" https://api.greengate.com.br/reports/verify/full/GG-a7f3k9m2p5q8
# Expected: {"property_name": "Farm #12345", "pdf_url": "...", ...}

# Test 3: Rate limiting should block after 10 requests/minute
for i in {1..15}; do
  curl https://api.greengate.com.br/reports/verify/public/GG-invalid
done
# Expected: 429 Too Many Requests after 10 requests

# Test 4: Should reject CPF in property_name
curl -X POST https://api.greengate.com.br/api/v1/validations \
  -H "x-api-key: test123" \
  -d '{"property_name": "João Silva 123.456.789-01", ...}'
# Expected: 400 Bad Request "property_name contains CPF pattern"

# Test 5: PDF URL should expire after 7 days
curl https://api.greengate.com.br/reports/download?token=expired_token
# Expected: 410 Gone "PDF link expired"
```

---

## 📊 Success Metrics

**Before Implementation:**
- Security Score: 4/10 (❌ Not EU-ready)
- Enumeration Risk: HIGH (predictable codes)
- Data Exposure: HIGH (property_name public)

**After Implementation:**
- Security Score: 8/10 (✅ Enterprise-grade)
- Enumeration Risk: LOW (128-bit entropy)
- Data Exposure: LOW (redacted by default)

**Due Diligence Audit:**
- ✅ Two-level verification (public minimal, authenticated full)
- ✅ High-entropy tokens (impossible to enumerate)
- ✅ Rate limiting (prevents abuse)
- ✅ No personal data processed (explicit validation)
- ✅ Automatic redaction (property_name treated as sensitive)
- ✅ Signed URLs (PDF access controlled)

---

**Next Steps:**
1. Review this TODO with team
2. Prioritize Week 1 tasks (critical for EU sales)
3. Implement and test each feature
4. Update frontend docs after backend is deployed
