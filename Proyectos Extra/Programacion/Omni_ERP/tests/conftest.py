"""Pytest configuration and fixtures."""

import asyncio
from datetime import datetime, timedelta

import bcrypt
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from dario_app.api import create_app
from dario_app.core import settings
from dario_app.core.auth import get_tenant_db
from dario_app.database import Base, get_db
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Role, UserRole, Usuario
from dario_app.modules.inventario.models import Producto, Proveedor
from dario_app.modules.produccion_ordenes.models import OrdenProduccion
from dario_app.modules.usuarios.routes import get_tenant_db_local

# In-memory database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
_test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    echo=True, 
    future=True, 
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)
_test_session_maker = async_sessionmaker(_test_engine, class_=AsyncSession, expire_on_commit=False)


async def setup_test_database():
    """Create tables and insert test data."""
    # Create all tables
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Insert test data
    async with _test_session_maker() as session:
        org = Organization(
            nombre="Test Org",
            slug="test-org",
            razon_social="Test SL",
            nif_cif="A12345678",
            domicilio_fiscal="Calle Test, 1",
            municipio="Madrid",
            provincia="Madrid",
            codigo_postal="28001",
            pais="España",
            regimen_iva="normal",
            porcentaje_iva=21,
            nif_valido=True,
            email="test@example.com",
            plan="trial",
        )
        session.add(org)
        await session.flush()
        org_id = org.id

        password = "test123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Usuario(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed,
            nombre_completo="Test User",
            es_admin=True,
            activo=True,
            organization_id=org_id,
        )
        session.add(user)
        await session.flush()
        user_id = user.id

        role = Role(
            nombre="Admin", descripcion="Admin role", es_sistema=True, organization_id=org_id
        )
        session.add(role)
        await session.flush()

        ur = UserRole(usuario_id=user_id, role_id=role.id)
        session.add(ur)

        await session.commit()

    return {"org_id": org_id, "user_id": user_id, "email": "test@example.com"}


def create_test_token(org_id: int, user_id: int, email: str) -> str:
    """Create a test JWT token."""
    payload = {
        "sub": str(user_id),
        "org_id": org_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return token


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async fixtures."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db_setup(event_loop):
    """Setup test database once per session."""
    return event_loop.run_until_complete(setup_test_database())


@pytest.fixture(scope="session")
def test_token_value(test_db_setup):
    """Create test token from test database data."""
    return create_test_token(
        test_db_setup["org_id"], test_db_setup["user_id"], test_db_setup["email"]
    )


@pytest.fixture
def client(test_token_value, test_db_setup):
    """Create test client with authentication and database overrides."""
    app = create_app()

    # Override database dependencies to use the in-memory test database
    async def override_get_db():
        async with _test_session_maker() as session:
            yield session

    # Override both get_db (general) and get_tenant_db (tenant-specific)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_tenant_db] = override_get_db
    app.dependency_overrides[get_tenant_db_local] = override_get_db

    tc = TestClient(app)
    # Add token to headers
    tc.headers = {"Authorization": f"Bearer {test_token_value}"}
    return tc

