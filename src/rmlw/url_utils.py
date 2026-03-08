"""
URL validation and normalization for RMLW.

Ensures target URLs are safe and scoped. All scans are restricted
to the host of the configured base URL.
"""

from urllib.parse import urlparse, urlunparse


class URLValidationError(ValueError):
    """Raised when a URL fails validation."""

    pass


def normalize_url(url: str) -> str:
    """
    Normalize a URL for use as scan target.

    - Strips trailing slashes from path (except for root)
    - Ensures scheme and netloc are present
    - Does not resolve or fetch; purely structural normalization

    Args:
        url: Raw URL string.

    Returns:
        Normalized URL string.

    Raises:
        URLValidationError: If URL is invalid or uses disallowed scheme.
    """
    url = url.strip()
    if not url:
        raise URLValidationError("URL cannot be empty")

    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc

    if scheme not in ("http", "https"):
        raise URLValidationError(f"URL scheme must be http or https, got: {scheme}")

    if not netloc:
        raise URLValidationError("URL must have a host (netloc)")

    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    normalized = urlunparse((scheme, netloc, path, parsed.params, parsed.query, parsed.fragment))
    return normalized


def validate_target_url(url: str) -> str:
    """
    Validate and normalize a target URL for scanning.

    Rejects dangerous schemes (file, javascript, data, etc.) and
    ensures the URL is suitable for HTTP(S) scanning.

    Args:
        url: Target URL from user input.

    Returns:
        Normalized URL safe for use.

    Raises:
        URLValidationError: If URL is invalid.
    """
    url = url.strip()
    if not url:
        raise URLValidationError("Target URL cannot be empty")

    parsed = urlparse(url)
    scheme = parsed.scheme.lower() if parsed.scheme else ""

    disallowed = ("file", "javascript", "data", "vbscript", "blob", "ftp")
    if scheme in disallowed:
        raise URLValidationError(f"URL scheme '{scheme}' is not allowed for scanning")

    if scheme and scheme not in ("http", "https"):
        raise URLValidationError(f"URL scheme must be http or https, got: {scheme}")

    if not scheme:
        url = "http://" + url

    return normalize_url(url)


def url_in_scope(url: str, base_netloc: str) -> bool:
    """
    Check if a URL belongs to the same host as the base.

    Used to enforce scope: we only scan endpoints on the configured host.

    Args:
        url: URL to check.
        base_netloc: Netloc (host:port) of the configured base URL.

    Returns:
        True if url's netloc matches base_netloc (case-insensitive).
    """
    parsed = urlparse(url)
    return parsed.netloc.lower() == base_netloc.lower()
