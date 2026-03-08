"""
Endpoint discovery for the Web Attack Workbench.

Current implementation: stub that seeds the base URL.
Future: crawler, proxy import, OpenAPI, GraphQL introspection.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def crawl(workbench: "WebAttackWorkbench") -> None:
    """
    Populate workbench.endpoints with discovered URLs.

    Stub implementation: adds the base URL only.
    Override or extend for:
        - HTML link and form discovery
        - Import from Burp, ZAP, mitmproxy, HAR
        - JavaScript parsing for dynamic endpoints
        - OpenAPI/Swagger, GraphQL introspection

    Args:
        workbench: The WebAttackWorkbench instance to populate.
    """
    workbench.endpoints.add(workbench.base_url)
