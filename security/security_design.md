┌─────────────────────────────────────────────────┐
│  SECURITY DESIGN REVIEW QUICK REFERENCE         │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. AUTHENTICATION & AUTHORIZATION               │
│     • Auth on all endpoints? RBAC? IDOR?        │
│                                                  │
│  2. INPUT VALIDATION                             │
│     • SQLi, XSS, SSRF, Path Traversal?          │
│     • Rate limiting? File upload validation?    │
│                                                  │
│  3. ENCRYPTION & DATA PROTECTION                 │
│     • TLS everywhere? Secrets managed?          │
│     • PII encrypted? Strong algorithms?         │
│                                                  │
│  4. INFRASTRUCTURE                               │
│     • Network segmentation? Least privilege?    │
│     • Defense in depth? No exposed admin?       │
│                                                  │
│  5. DEPENDENCIES                                 │
│     • CVE scanning? Pinned versions?            │
│                                                  │
│  6. LOGGING & MONITORING                         │
│     • Centralized logs? Alerting? Audit trail?  │
│                                                  │
│  7. LLM-SPECIFIC (Anthropic!)                    │
│     • Prompt injection? Content filtering?      │
│     • Model access control? PII leakage?        │
│                                                  │
│  APPROACH: Map system → Systematic review →     │
│            Prioritize (C/H/M/L) → Present       │
└─────────────────────────────────────────────────┘

🧠 Mental Models
### The Trust Boundary Model
Draw mental boundaries:
* Internet → API Gateway → Backend → Database
* At each boundary, ask: "Do we validate? Authenticate? Encrypt?"

### The Attacker Mindset (STRIDE)
- For each component, think like an attacker:
- Spoofing: Can I impersonate someone?
- Tampering: Can I modify data?
- Repudiation: Can I deny my actions?
- Information disclosure: Can I see secrets?
- Denial of service: Can I crash it?
- Elevation of privilege: Can I become admin?