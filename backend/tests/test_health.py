from http.client import responses
from asyncio import Transport
from httpx import ASGITransport, AsyncClient

from app.main import app

async def test_health_returns_ok():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status" : "ok"}
