"""Document templates and attachments models."""

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class DocumentTemplate(Base):
    """Document template configuration for visual customization of invoices and shipping notes."""

    __tablename__ = "document_templates"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Document type: "factura" or "albarán"
    tipo_documento: Mapped[str] = mapped_column(String(20), nullable=False)

    # Visual customization only (legal data comes from Organization)
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    mostrar_logo: Mapped[bool] = mapped_column(Boolean, default=True)
    color_primario: Mapped[str] = mapped_column(String(7), default="#2563eb")  # Hex color
    color_secundario: Mapped[str] = mapped_column(String(7), default="#64748b")  # Hex color
    fuente: Mapped[str] = mapped_column(String(50), default="Helvetica")  # Font family

    # Visual elements
    mostrar_qr: Mapped[bool] = mapped_column(Boolean, default=True)
    mostrar_codigo_barras: Mapped[bool] = mapped_column(Boolean, default=False)
    mostrar_firma_vendedor: Mapped[bool] = mapped_column(Boolean, default=True)
    mostrar_firma_cliente: Mapped[bool] = mapped_column(Boolean, default=True)
    mostrar_sello: Mapped[bool] = mapped_column(Boolean, default=False)

    # Customizable text sections
    condiciones_pago: Mapped[str] = mapped_column(Text, nullable=True)
    notas_pie: Mapped[str] = mapped_column(Text, nullable=True)
    terminos_condiciones: Mapped[str] = mapped_column(Text, nullable=True)

    # Layout configuration (JSON with element positions and sizes)
    layout_config: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
        default={
            "encabezado": {"visible": True, "posicion": "top", "altura": 150},
            "tabla_items": {
                "visible": True,
                "posicion": "middle",
                "columns": ["item", "cantidad", "precio", "subtotal"],
            },
            "totales": {"visible": True, "posicion": "bottom_right"},
            "marco": "simple",  # simple, elegante, corporativo, moderno
            "margenes": {"top": 20, "right": 20, "bottom": 20, "left": 20},
        },
    )

    # Numbering
    prefijo: Mapped[str] = mapped_column(String(10), nullable=True)  # F-, A-, etc.
    proximo_numero: Mapped[int] = mapped_column(Integer, default=1)

    # Timestamps
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    class Config:
        from_attributes = True


class DocumentoManual(Base):
    """Manual documents (invoices/packing slips) created without a sale."""

    __tablename__ = "documentos_manuales"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Document info
    tipo_documento: Mapped[str] = mapped_column(String(20), nullable=False)  # factura or albarán
    numero_documento: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Customer info
    cliente_nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    cliente_email: Mapped[str] = mapped_column(String(100), nullable=True)
    cliente_telefono: Mapped[str] = mapped_column(String(50), nullable=True)
    cliente_direccion: Mapped[str] = mapped_column(Text, nullable=True)

    # Document content
    items: Mapped[list] = mapped_column(
        JSON, nullable=False
    )  # List of {cantidad, descripcion, precio_unitario}

    # Totals
    subtotal: Mapped[float] = mapped_column(nullable=False)
    impuesto: Mapped[float] = mapped_column(nullable=False, default=0)
    total: Mapped[float] = mapped_column(nullable=False)

    # Notes
    notas: Mapped[str] = mapped_column(Text, nullable=True)

    # Template used
    template_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("document_templates.id"), nullable=True
    )

    # Timestamps
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    class Config:
        from_attributes = True


class DocumentFile(Base):
    """Stored file record for generated documents (PDFs)."""

    __tablename__ = "document_files"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), index=True)

    # Document reference
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "manual"
    doc_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # Storage
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), default="application/pdf")

    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True


class DocumentAttachment(Base):
    """Attachment container with latest version pointer."""

    __tablename__ = "document_attachments"
    __table_args__ = (
        Index("idx_doc_attach_org_doc", "organization_id", "doc_type", "doc_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), index=True)

    doc_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    doc_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    latest_version_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True


class DocumentAttachmentVersion(Base):
    """Versioned attachment record with storage info."""

    __tablename__ = "document_attachment_versions"
    __table_args__ = (
        UniqueConstraint("attachment_id", "version_number", name="uq_attachment_version"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attachment_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_attachments.id"), index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), index=True)

    doc_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    doc_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), default="application/octet-stream")
    storage_provider: Mapped[str] = mapped_column(String(50), default="local")
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    preview_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    checksum: Mapped[str] = mapped_column(String(128), nullable=True)

    tags: Mapped[list] = mapped_column(JSON, default=list)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)

    scan_status: Mapped[str] = mapped_column(String(50), default="clean")  # clean, pending, flagged
    scan_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    uploaded_by_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    uploaded_by_email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True


class DocumentSearchIndex(Base):
    """Lightweight search index for attachments (SQLite friendly)."""

    __tablename__ = "document_search_index"
    __table_args__ = (
        Index("idx_doc_search_org", "organization_id", "doc_type", "doc_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), index=True)
    attachment_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_attachments.id"), index=True)
    version_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_attachment_versions.id"), index=True)

    doc_type: Mapped[str] = mapped_column(String(100), nullable=False)
    doc_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    tags_text: Mapped[str] = mapped_column(Text, nullable=True)
    metadata_text: Mapped[str] = mapped_column(Text, nullable=True)
    search_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True
