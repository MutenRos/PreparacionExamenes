"""Customer/Client models for CRM."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Cliente(Base):
    """Customer/Client model for CRM."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    nombre: Mapped[str] = mapped_column(String(200), nullable=False)  # Nombre comercial
    razon_social: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Si es empresa
    nif_nie: Mapped[str | None] = mapped_column(
        String(20), nullable=True, index=True
    )  # NIF/NIE (España)
    nif_valido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tipo_cliente: Mapped[str] = mapped_column(
        String(20), default="particular", nullable=False
    )  # particular, empresa

    email: Mapped[str] = mapped_column(String(200), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Fiscal address (Spain compliance)
    domicilio: Mapped[str | None] = mapped_column(Text, nullable=True)  # Calle, número
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provincia: Mapped[str | None] = mapped_column(String(100), nullable=True)
    codigo_postal: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Loyalty system
    puntos_lealtad: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nivel_lealtad: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Bronce"
    )  # Bronce, Plata, Oro
    total_compras: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00")
    )

    # Status
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)

    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
