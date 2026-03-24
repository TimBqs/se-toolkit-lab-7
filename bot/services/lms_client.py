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

    def get_pass_rates(self, lab: str) -> dict:
        """Get pass rates for a specific lab."""
        try:
            response = self._client.get("/analytics/pass-rates", params={"lab": lab})
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return {"error": f"connection refused ({self.base_url})"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code} {e.response.reason_phrase}"}
        except Exception as e:
            return {"error": str(e)}


# Global client instance
lms_client = LMSClient()
