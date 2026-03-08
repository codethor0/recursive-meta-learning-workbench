# Security and Scope

## Authorized Testing Only

RMLW is designed for **authorized security testing** in controlled environments:

- Lab networks
- Staging environments
- Applications you own or have explicit permission to test

Out of scope:

- Unauthorized scanning of third-party systems
- Production systems without approval
- Any use that violates computer misuse laws

## Assumptions About Targets

RMLW is intended for lab applications such as:

- DVWA (Damn Vulnerable Web Application)
- OWASP WebGoat
- Other intentionally vulnerable training apps

You must have explicit permission to test any target. The tool does not distinguish between authorized and unauthorized targets; the operator is responsible for compliance.

## Tool Design Principles

- **Transparency**: Every finding records exact payload and response; logs show which tests ran
- **Least privilege**: No eval/exec on untrusted input; target URLs validated and scoped
- **Safe defaults**: TLS verification enabled; explicit timeouts; no hardcoded credentials

## Reporting Vulnerabilities in RMLW

If you find a vulnerability in RMLW itself (not in targets it tests), report responsibly. See SECURITY.md in the project root for contact details and expectations.
