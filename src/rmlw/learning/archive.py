"""
Persistent archive for RMLW.

Stores successful payloads with context for recombination
and novelty search.
"""

import time
from typing import Any


class PersistentArchive:
    """
    Archive of successful payloads and minimal context.

    Supports add_success, recent retrieval, and can be extended
    for diversity-aware retrieval (e.g. MMR).
    """

    def __init__(self) -> None:
        self.items: list[dict[str, Any]] = []

    def add_success(self, vuln_type: str, payload: str, detail: dict[str, Any]) -> None:
        """
        Add a successful payload to the archive.

        Args:
            vuln_type: Vulnerability type.
            payload: The payload that succeeded.
            detail: Supporting evidence (status, length, etc.).
        """
        self.items.append(
            {
                "vuln_type": vuln_type,
                "payload": payload,
                "detail": detail,
                "timestamp": time.time(),
            }
        )

    def recent(self, n: int = 10) -> list[dict[str, Any]]:
        """
        Return the N most recent archive entries.

        Args:
            n: Number of entries to return.

        Returns:
            List of archive entry dicts.
        """
        return self.items[-n:]
