# GovernanceTestApp — Decision Record

## DR-001: Pure Python, No External Dependencies
- **Date:** 2026-03-03
- **Context:** Choosing technology stack for the test app
- **Decision:** Use only Python stdlib (no pip packages except pytest for testing)
- **Consequences:** Simpler governance testing (no dep-gate triggers during implementation), faster setup
