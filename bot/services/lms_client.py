"""LMS API client with Bearer token authentication."""

import httpx
from config import settings


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(self):
        self.base_url = settings.lms_api_base_url
        self.api_key = settings.lms_api_key
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10.0,
        )

    def health_check(self) -> dict:
        """Check if backend is healthy and return item count."""
        try:
            response = self._client.get("/items/")
            response.raise_for_status()
            items = response.json()
            return {"healthy": True, "item_count": len(items)}
        except httpx.ConnectError as e:
            return {"healthy": False, "error": f"connection refused ({self.base_url})"}
        except httpx.HTTPStatusError as e:
            return {"healthy": False, "error": f"HTTP {e.response.status_code} {e.response.reason_phrase}"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def get_labs(self) -> list[dict]:
        """Get all available labs."""
        try:
            response = self._client.get("/items/")
            response.raise_for_status()
            items = response.json()
            # Filter for labs (type may vary based on backend structure)
            return items
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_pass_rates(self, lab: str) -> list[dict]:
        """Get pass rates for a specific lab."""
        try:
            response = self._client.get("/analytics/pass-rates", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError as e:
            return [{"error": f"HTTP {e.response.status_code} {e.response.reason_phrase}"}]
        except Exception as e:
            return [{"error": str(e)}]

    def get_learners(self) -> list[dict]:
        """Get all enrolled learners."""
        try:
            response = self._client.get("/learners/")
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_scores(self, lab: str) -> list[dict]:
        """Get score distribution for a lab (4 buckets)."""
        try:
            response = self._client.get("/analytics/scores", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_timeline(self, lab: str) -> list[dict]:
        """Get submissions per day for a lab."""
        try:
            response = self._client.get("/analytics/timeline", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_groups(self, lab: str) -> list[dict]:
        """Get per-group performance for a lab."""
        try:
            response = self._client.get("/analytics/groups", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_top_learners(self, lab: str, limit: int = 5) -> list[dict]:
        """Get top N learners for a lab."""
        try:
            response = self._client.get("/analytics/top-learners", params={"lab": lab, "limit": limit})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def get_completion_rate(self, lab: str) -> dict:
        """Get completion rate for a lab."""
        try:
            response = self._client.get("/analytics/completion-rate", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return {"error": "connection refused"}
        except httpx.HTTPStatusError:
            return {"error": "HTTP error"}
        except Exception as e:
            return {"error": str(e)}

    def trigger_sync(self) -> dict:
        """Trigger ETL pipeline sync."""
        try:
            response = self._client.post("/pipeline/sync", json={})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return {"error": "connection refused"}
        except httpx.HTTPStatusError:
            return {"error": "HTTP error"}
        except Exception as e:
            return {"error": str(e)}


# Global client instance
lms_client = LMSClient()
