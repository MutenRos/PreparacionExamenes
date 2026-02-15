"""Test API endpoints."""

import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"


def test_root_endpoint(client):
    """Test root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_list_usuarios(client):
    """Test list usuarios endpoint."""
    response = client.get("/api/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_productos(client):
    """Test list productos endpoint."""
    response = client.get("/api/inventario/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_ventas(client):
    """Test list ventas endpoint."""
    response = client.get("/api/ventas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_compras(client):
    """Test list compras endpoint."""
    response = client.get("/api/compras/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
