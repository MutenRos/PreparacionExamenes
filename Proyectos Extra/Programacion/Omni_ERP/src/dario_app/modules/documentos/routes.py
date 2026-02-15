"""Document templates and attachments API routes."""

import json
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator, Field
from sqlalchemy import select, func, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db, get_current_user_org
from dario_app.core.pdf_service import PDFGenerator
from dario_app.modules.tenants.models import Organization
from dario_app.services.audit_service import AuditService, AuditAction, AuditSeverity
from dario_app.services.document_storage_service import DocumentStorageService

from .models import (
    DocumentTemplate,
    DocumentoManual,
    DocumentFile,
    DocumentAttachment,
    DocumentAttachmentVersion,
    DocumentSearchIndex,
)

router = APIRouter(prefix="/api/templates", tags=["templates"])
attachments_router = APIRouter(prefix="/api/documentos", tags=["documentos"])

storage_service = DocumentStorageService()


class AttachmentVersionResponse(BaseModel):
    """Attachment version response payload."""

    attachment_id: int
    version_id: int
    version_number: int
    doc_type: str
    doc_id: int
    file_name: str
    content_type: str
    storage_path: str
    storage_provider: str
    size_bytes: int
    checksum: Optional[str]
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    scan_status: str
    scan_message: Optional[str] = None
    uploaded_by_id: Optional[int] = None
    uploaded_by_email: Optional[str] = None
    uploaded_at: datetime
    is_latest: bool = True

    class Config:
        from_attributes = True


class AttachmentResponse(BaseModel):
    """Attachment container with latest version embedded."""

    id: int
    name: str
    doc_type: str
    doc_id: int
    description: Optional[str]
    latest_version: AttachmentVersionResponse
    updated_at: datetime

    class Config:
        from_attributes = True


class AttachmentSearchRequest(BaseModel):
    """Search attachments request."""

    query: str
    doc_type: Optional[str] = None
    doc_id: Optional[int] = None
    tags: Optional[List[str]] = None
    limit: int = 20


class AttachmentSearchResult(BaseModel):
    """Search response item."""

    attachment_id: int
    version_id: int
    doc_type: str
    doc_id: int
    title: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


async def _register_attachment_version(
    db: AsyncSession,
    *,
    org_id: int,
    doc_type: str,
    doc_id: int,
    file_name: str,
    content: bytes,
    content_type: str,
    description: Optional[str],
    tags: List[str],
    metadata: dict,
    storage_provider: str,
    user_context: Optional[dict],
) -> tuple[DocumentAttachment, DocumentAttachmentVersion]:
    """Persist attachment version and update search index."""

    stmt = select(DocumentAttachment).where(
        DocumentAttachment.organization_id == org_id,
        DocumentAttachment.doc_type == doc_type,
        DocumentAttachment.doc_id == doc_id,
        DocumentAttachment.name == file_name,
    )
    existing = await db.execute(stmt)
    attachment = existing.scalar_one_or_none()

    if not attachment:
        attachment = DocumentAttachment(
            organization_id=org_id,
            doc_type=doc_type,
            doc_id=doc_id,
            name=file_name,
            description=description,
        )
        db.add(attachment)
        await db.flush()
    else:
        if description:
            attachment.description = description

    # Clear latest flags
    await db.execute(
        update(DocumentAttachmentVersion)
        .where(DocumentAttachmentVersion.attachment_id == attachment.id)
        .values(is_latest=False)
    )

    max_version_stmt = select(func.max(DocumentAttachmentVersion.version_number)).where(
        DocumentAttachmentVersion.attachment_id == attachment.id
    )
    res_version = await db.execute(max_version_stmt)
    next_version = (res_version.scalar_one_or_none() or 0) + 1

    stored = await storage_service.store_bytes(
        content=content,
        filename=file_name,
        content_type=content_type,
        org_id=org_id,
        doc_type=doc_type,
        doc_id=doc_id,
        version_number=next_version,
        storage_provider=storage_provider,
    )

    version = DocumentAttachmentVersion(
        attachment_id=attachment.id,
        organization_id=org_id,
        doc_type=doc_type,
        doc_id=doc_id,
        version_number=next_version,
        file_name=file_name,
        content_type=stored["content_type"],
        storage_provider=stored["storage_provider"],
        storage_path=stored["storage_path"],
        preview_path=None,
        size_bytes=stored["size_bytes"],
        checksum=stored["checksum"],
        tags=tags,
        metadata_json=metadata,
        scan_status=stored["scan_status"],
        scan_message=stored.get("scan_message"),
        uploaded_by_id=user_context.get("user_id") if user_context else None,
        uploaded_by_email=user_context.get("email") if user_context else None,
        is_latest=True,
    )
    db.add(version)
    await db.flush()

    attachment.latest_version_id = version.id
    attachment.updated_at = datetime.utcnow()

    tags_text = " ".join(tags or [])
    metadata_text = " ".join(f"{k}:{v}" for k, v in (metadata or {}).items())
    search_text = " ".join(filter(None, [attachment.name, tags_text, metadata_text, description]))

    index_entry = DocumentSearchIndex(
        organization_id=org_id,
        attachment_id=attachment.id,
        version_id=version.id,
        doc_type=doc_type,
        doc_id=doc_id,
        title=file_name,
        tags_text=tags_text,
        metadata_text=metadata_text,
        search_text=search_text,
        uploaded_at=version.uploaded_at,
    )
    db.add(index_entry)

    return attachment, version


class DocumentTemplateCreate(BaseModel):
    """Create document template request - only visual customization."""

    tipo_documento: str  # "factura" or "albarán"
    logo_url: Optional[str] = None
    color_primario: str = "#2563eb"
    color_secundario: str = "#64748b"
    fuente: str = "Helvetica"
    mostrar_logo: bool = True
    mostrar_qr: bool = True
    mostrar_codigo_barras: bool = False
    mostrar_firma_vendedor: bool = True
    mostrar_firma_cliente: bool = True
    mostrar_sello: bool = False
    condiciones_pago: Optional[str] = None
    notas_pie: Optional[str] = None
    terminos_condiciones: Optional[str] = None
    prefijo: Optional[str] = None

    @field_validator("tipo_documento")
    @classmethod
    def validate_tipo_documento(cls, v):
        if v not in ["factura", "albarán"]:
            raise ValueError('tipo_documento debe ser "factura" o "albarán"')
        return v


class DocumentTemplateResponse(BaseModel):
    """Document template response."""

    id: int
    organization_id: int
    tipo_documento: str
    logo_url: Optional[str]
    color_primario: str
    color_secundario: str
    mostrar_logo: bool
    mostrar_qr: bool
    creado_en: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[DocumentTemplateResponse])
async def list_templates(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all document templates for organization."""
    result = await db.execute(
        select(DocumentTemplate)
        .where(DocumentTemplate.organization_id == org_id)
        .order_by(DocumentTemplate.tipo_documento)
    )
    return result.scalars().all()


@router.get("/{template_id}", response_model=DocumentTemplateResponse)
async def get_template(
    template_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a specific document template."""
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == template_id, DocumentTemplate.organization_id == org_id
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    return template


@router.post("/", response_model=DocumentTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: DocumentTemplateCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new document template."""
    # Check if template for this document type already exists
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.organization_id == org_id,
            DocumentTemplate.tipo_documento == template_data.tipo_documento,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail=f"Ya existe una plantilla para {template_data.tipo_documento}"
        )

    template = DocumentTemplate(organization_id=org_id, **template_data.model_dump())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.put("/{template_id}", response_model=DocumentTemplateResponse)
async def update_template(
    template_id: int,
    template_data: DocumentTemplateCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an existing document template."""
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == template_id, DocumentTemplate.organization_id == org_id
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    # Update fields
    for field, value in template_data.model_dump().items():
        setattr(template, field, value)

    template.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(template)
    return template


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Delete a document template."""
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == template_id, DocumentTemplate.organization_id == org_id
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    await db.delete(template)
    await db.commit()


# ===== PDF Generation Routes =====


class GenerarPDFRequest(BaseModel):
    """Request data for PDF generation."""

    template_id: int
    items: List[dict]  # List of {descripcion, cantidad, precio_unitario, descuento}
    cliente_nombre: str
    cliente_documento: Optional[str] = None
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    subtotal: float
    descuento: float = 0
    impuesto: float
    total: float
    numero_documento: Optional[str] = None


@router.post("/{template_id}/generar-pdf")
async def generar_pdf(
    template_id: int,
    datos: GenerarPDFRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Generate PDF using a specific template."""
    # Get template
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == template_id, DocumentTemplate.organization_id == org_id
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    # Get organization data
    org_result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = org_result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    # Verify fiscal data is complete
    if not organization.datos_fiscales_completos:
        raise HTTPException(
            status_code=400,
            detail="Complete los datos fiscales de su empresa en Configuración → Organización antes de generar documentos",
        )

    # Prepare venta data
    venta_data = {
        "numero": datos.numero_documento or "N/A",
        "items": datos.items,
        "subtotal": datos.subtotal,
        "descuento": datos.descuento,
        "impuesto": datos.impuesto,
        "total": datos.total,
    }

    # Prepare cliente data
    cliente_data = {
        "nombre": datos.cliente_nombre,
        "documento": datos.cliente_documento or "N/A",
        "email": datos.cliente_email or "N/A",
        "telefono": datos.cliente_telefono or "N/A",
    }

    # Generate PDF
    try:
        generator = PDFGenerator(template, organization)
        pdf_buffer = generator.generate_invoice_pdf(venta_data, cliente_data)

        filename = f"{template.tipo_documento}_{datos.numero_documento or 'documento'}.pdf"

        return StreamingResponse(
            iter([pdf_buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")


@router.post("/{template_id}/preview-pdf")
async def preview_pdf(
    template_id: int,
    datos: GenerarPDFRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Preview PDF (returns base64 for inline display)."""
    # Get template
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == template_id, DocumentTemplate.organization_id == org_id
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    # Get organization data
    org_result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = org_result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    # Verify fiscal data is complete
    if not organization.datos_fiscales_completos:
        raise HTTPException(
            status_code=400,
            detail="Complete los datos fiscales de su empresa antes de generar documentos",
        )

    # Prepare venta data
    venta_data = {
        "numero": datos.numero_documento or "N/A",
        "items": datos.items,
        "subtotal": datos.subtotal,
        "descuento": datos.descuento,
        "impuesto": datos.impuesto,
        "total": datos.total,
    }

    # Prepare cliente data
    cliente_data = {
        "nombre": datos.cliente_nombre,
        "documento": datos.cliente_documento or "N/A",
        "email": datos.cliente_email or "N/A",
        "telefono": datos.cliente_telefono or "N/A",
    }

    # Generate PDF
    try:
        import base64

        generator = PDFGenerator(template, organization)
        pdf_buffer = generator.generate_invoice_pdf(venta_data, cliente_data)

        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")

        return {"status": "success", "pdf_base64": pdf_base64, "content_type": "application/pdf"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando preview: {str(e)}")


# ===== Document Attachments (versioned, searchable) =====


@attachments_router.post(
    "/{doc_type}/{doc_id}/attachments",
    response_model=AttachmentVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_attachment(
    doc_type: str,
    doc_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form("[]"),
    metadata: Optional[str] = Form("{}"),
    storage_provider: str = Form("local"),
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    user_ctx: dict | None = Depends(get_current_user_org),
):
    try:
        parsed_tags = json.loads(tags) if tags else []
        if parsed_tags is None:
            parsed_tags = []
        if not isinstance(parsed_tags, list):
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="tags debe ser una lista JSON")

    try:
        parsed_metadata = json.loads(metadata) if metadata else {}
        if parsed_metadata is None:
            parsed_metadata = {}
        if not isinstance(parsed_metadata, dict):
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="metadata debe ser un objeto JSON")

    content = await file.read()

    attachment, version = await _register_attachment_version(
        db,
        org_id=org_id,
        doc_type=doc_type,
        doc_id=doc_id,
        file_name=file.filename,
        content=content,
        content_type=file.content_type or "application/octet-stream",
        description=description,
        tags=parsed_tags,
        metadata=parsed_metadata,
        storage_provider=storage_provider,
        user_context=user_ctx,
    )

    await db.commit()

    return AttachmentVersionResponse(
        attachment_id=attachment.id,
        version_id=version.id,
        version_number=version.version_number,
        doc_type=version.doc_type,
        doc_id=version.doc_id,
        file_name=version.file_name,
        content_type=version.content_type,
        storage_path=version.storage_path,
        storage_provider=version.storage_provider,
        size_bytes=version.size_bytes,
        checksum=version.checksum,
        tags=version.tags,
        metadata=version.metadata_json,
        scan_status=version.scan_status,
        scan_message=version.scan_message,
        uploaded_by_id=version.uploaded_by_id,
        uploaded_by_email=version.uploaded_by_email,
        uploaded_at=version.uploaded_at,
        is_latest=version.is_latest,
    )


@attachments_router.get(
    "/{doc_type}/{doc_id}/attachments",
    response_model=List[AttachmentResponse],
)
async def list_attachments(
    doc_type: str,
    doc_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    stmt = (
        select(DocumentAttachment, DocumentAttachmentVersion)
        .join(
            DocumentAttachmentVersion,
            and_(
                DocumentAttachmentVersion.attachment_id == DocumentAttachment.id,
                DocumentAttachmentVersion.is_latest == True,
            ),
        )
        .where(
            DocumentAttachment.organization_id == org_id,
            DocumentAttachment.doc_type == doc_type,
            DocumentAttachment.doc_id == doc_id,
            DocumentAttachment.is_deleted == False,
        )
        .order_by(DocumentAttachment.updated_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    response: List[AttachmentResponse] = []
    for attachment, version in rows:
        response.append(
            AttachmentResponse(
                id=attachment.id,
                name=attachment.name,
                doc_type=attachment.doc_type,
                doc_id=attachment.doc_id,
                description=attachment.description,
                updated_at=attachment.updated_at,
                latest_version=AttachmentVersionResponse(
                    attachment_id=attachment.id,
                    version_id=version.id,
                    version_number=version.version_number,
                    doc_type=version.doc_type,
                    doc_id=version.doc_id,
                    file_name=version.file_name,
                    content_type=version.content_type,
                    storage_path=version.storage_path,
                    storage_provider=version.storage_provider,
                    size_bytes=version.size_bytes,
                    checksum=version.checksum,
                    tags=version.tags,
                    metadata=version.metadata_json,
                    scan_status=version.scan_status,
                    scan_message=version.scan_message,
                    uploaded_by_id=version.uploaded_by_id,
                    uploaded_by_email=version.uploaded_by_email,
                    uploaded_at=version.uploaded_at,
                    is_latest=version.is_latest,
                ),
            )
        )
    return response


@attachments_router.get(
    "/attachments/{attachment_id}/versions",
    response_model=List[AttachmentVersionResponse],
)
async def list_versions(
    attachment_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    attach_stmt = select(DocumentAttachment).where(
        DocumentAttachment.id == attachment_id,
        DocumentAttachment.organization_id == org_id,
    )
    attach_res = await db.execute(attach_stmt)
    attachment = attach_res.scalar_one_or_none()
    if not attachment:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    stmt = (
        select(DocumentAttachmentVersion)
        .where(DocumentAttachmentVersion.attachment_id == attachment_id)
        .order_by(DocumentAttachmentVersion.version_number.desc())
    )
    res = await db.execute(stmt)
    versions = res.scalars().all()

    return [
        AttachmentVersionResponse(
            attachment_id=attachment.id,
            version_id=v.id,
            version_number=v.version_number,
            doc_type=v.doc_type,
            doc_id=v.doc_id,
            file_name=v.file_name,
            content_type=v.content_type,
            storage_path=v.storage_path,
            storage_provider=v.storage_provider,
            size_bytes=v.size_bytes,
            checksum=v.checksum,
            tags=v.tags,
            metadata=v.metadata_json,
            scan_status=v.scan_status,
            scan_message=v.scan_message,
            uploaded_by_id=v.uploaded_by_id,
            uploaded_by_email=v.uploaded_by_email,
            uploaded_at=v.uploaded_at,
            is_latest=v.is_latest,
        )
        for v in versions
    ]


@attachments_router.get("/attachments/versions/{version_id}/download")
async def download_version(
    version_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    stmt = (
        select(DocumentAttachmentVersion)
        .join(DocumentAttachment, DocumentAttachment.id == DocumentAttachmentVersion.attachment_id)
        .where(
            DocumentAttachmentVersion.id == version_id,
            DocumentAttachment.organization_id == org_id,
        )
    )
    res = await db.execute(stmt)
    version = res.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")

    try:
        content = await storage_service.load_file(version.storage_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no disponible")

    return StreamingResponse(
        iter([content]),
        media_type=version.content_type,
        headers={"Content-Disposition": f"attachment; filename={version.file_name}"},
    )


@attachments_router.post("/attachments/search", response_model=List[AttachmentSearchResult])
async def search_attachments(
    payload: AttachmentSearchRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    stmt = select(DocumentSearchIndex).where(DocumentSearchIndex.organization_id == org_id)

    if payload.doc_type:
        stmt = stmt.where(DocumentSearchIndex.doc_type == payload.doc_type)
    if payload.doc_id:
        stmt = stmt.where(DocumentSearchIndex.doc_id == payload.doc_id)
    if payload.query:
        stmt = stmt.where(DocumentSearchIndex.search_text.ilike(f"%{payload.query}%"))
    if payload.tags:
        for tag in payload.tags:
            stmt = stmt.where(DocumentSearchIndex.tags_text.ilike(f"%{tag}%"))

    stmt = stmt.order_by(DocumentSearchIndex.uploaded_at.desc()).limit(payload.limit)

    res = await db.execute(stmt)
    entries = res.scalars().all()

    return [
        AttachmentSearchResult(
            attachment_id=e.attachment_id,
            version_id=e.version_id,
            doc_type=e.doc_type,
            doc_id=e.doc_id,
            title=e.title,
            uploaded_at=e.uploaded_at,
        )
        for e in entries
    ]


# ===== Documentos Manuales (Invoices/Albarans) =====

from .models import DocumentoManual, DocumentFile


class ItemManual(BaseModel):
    """Item for manual document."""

    cantidad: float
    descripcion: str
    precio_unitario: float


class DocumentoManualCreate(BaseModel):
    """Create manual document request."""

    tipo_documento: str  # "factura" or "albarán"
    numero_documento: str
    cliente_nombre: str
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    cliente_direccion: Optional[str] = None
    items: List[ItemManual]
    subtotal: float
    impuesto: float
    total: float
    template_id: int
    notas: Optional[str] = None

    @field_validator("tipo_documento")
    @classmethod
    def validate_tipo_documento(cls, v):
        if v not in ["factura", "albarán"]:
            raise ValueError('tipo_documento debe ser "factura" o "albarán"')
        return v


class DocumentoManualResponse(BaseModel):
    """Manual document response."""

    id: int
    organization_id: int
    tipo_documento: str
    numero_documento: str
    cliente_nombre: str
    cliente_email: Optional[str]
    cliente_telefono: Optional[str]
    cliente_direccion: Optional[str]
    items: List[dict]
    subtotal: float
    impuesto: float
    total: float
    template_id: int
    notas: Optional[str]
    creado_en: datetime

    class Config:
        from_attributes = True


@router.post(
    "/manuales/", response_model=DocumentoManualResponse, status_code=status.HTTP_201_CREATED
)
async def crear_documento_manual(
    doc_data: DocumentoManualCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new manual document."""
    # Verify template exists
    result = await db.execute(
        select(DocumentTemplate).where(
            DocumentTemplate.id == doc_data.template_id, DocumentTemplate.organization_id == org_id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    # Verify fiscal data is complete
    org_result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = org_result.scalar_one_or_none()
    if not organization or not organization.datos_fiscales_completos:
        raise HTTPException(
            status_code=400,
            detail="Complete los datos fiscales de su empresa para crear documentos",
        )

    # Create document
    items_list = [
        {
            "cantidad": item.cantidad,
            "descripcion": item.descripcion,
            "precio_unitario": item.precio_unitario,
            "subtotal": item.cantidad * item.precio_unitario,
        }
        for item in doc_data.items
    ]

    documento = DocumentoManual(
        organization_id=org_id,
        tipo_documento=doc_data.tipo_documento,
        numero_documento=doc_data.numero_documento,
        cliente_nombre=doc_data.cliente_nombre,
        cliente_email=doc_data.cliente_email,
        cliente_telefono=doc_data.cliente_telefono,
        cliente_direccion=doc_data.cliente_direccion,
        items=items_list,
        subtotal=doc_data.subtotal,
        impuesto=doc_data.impuesto,
        total=doc_data.total,
        template_id=doc_data.template_id,
        notas=doc_data.notas,
    )

    db.add(documento)
    await db.commit()
    await db.refresh(documento)
    
    # Audit logging skipped (audit_logs table not in tenant DB schema)
    
    return documento


@router.get("/manuales/", response_model=List[DocumentoManualResponse])
async def listar_documentos_manuales(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all manual documents for organization."""
    result = await db.execute(
        select(DocumentoManual)
        .where(DocumentoManual.organization_id == org_id)
        .order_by(DocumentoManual.creado_en.desc())
    )
    return result.scalars().all()


@router.get("/manuales/{doc_id}", response_model=DocumentoManualResponse)
async def obtener_documento_manual(
    doc_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a specific manual document."""
    result = await db.execute(
        select(DocumentoManual).where(
            DocumentoManual.id == doc_id, DocumentoManual.organization_id == org_id
        )
    )
    documento = result.scalar_one_or_none()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento


@router.delete("/manuales/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_documento_manual(
    doc_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Delete a manual document."""
    result = await db.execute(
        select(DocumentoManual).where(
            DocumentoManual.id == doc_id, DocumentoManual.organization_id == org_id
        )
    )
    documento = result.scalar_one_or_none()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    await db.delete(documento)
    await db.commit()


@router.post("/manuales/{doc_id}/generar-pdf")
async def generar_pdf_manual(
    doc_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Generate PDF for a manual document."""
    # Get document
    doc_result = await db.execute(
        select(DocumentoManual).where(
            DocumentoManual.id == doc_id, DocumentoManual.organization_id == org_id
        )
    )
    documento = doc_result.scalar_one_or_none()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # Get template
    template_result = await db.execute(
        select(DocumentTemplate).where(DocumentTemplate.id == documento.template_id)
    )
    template = template_result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

    # Get organization
    org_result = await db.execute(select(Organization).where(Organization.id == org_id))
    organization = org_result.scalar_one_or_none()
    if not organization:
        raise HTTPException(status_code=404, detail="Organización no encontrada")

    # Prepare data for PDF generation
    venta_data = {
        "numero": documento.numero_documento,
        "items": documento.items,
        "subtotal": documento.subtotal,
        "descuento": 0,
        "impuesto": documento.impuesto,
        "total": documento.total,
        "notas": documento.notas,
    }

    cliente_data = {
        "nombre": documento.cliente_nombre,
        "documento": "N/A",
        "email": documento.cliente_email or "N/A",
        "telefono": documento.cliente_telefono or "N/A",
        "direccion": documento.cliente_direccion or "N/A",
    }

    # Generate PDF
    try:
        generator = PDFGenerator(template, organization)
        pdf_buffer = generator.generate_invoice_pdf(venta_data, cliente_data)
        filename = f"{documento.tipo_documento}_{documento.numero_documento}.pdf"
        pdf_bytes = pdf_buffer.getvalue()

        await _register_attachment_version(
            db,
            org_id=org_id,
            doc_type="documento_manual",
            doc_id=doc_id,
            file_name=filename,
            content=pdf_bytes,
            content_type="application/pdf",
            description=f"Documento manual {documento.numero_documento}",
            tags=[documento.tipo_documento, "manual"],
            metadata={"cliente": documento.cliente_nombre, "numero": documento.numero_documento},
            storage_provider="local",
            user_context=None,
        )
        await db.commit()

        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")
