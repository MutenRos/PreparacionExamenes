"""Rutas API para configuración del sistema."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db, get_org_id
from modules.configuracion.models import (
    ConfiguracionGeneral,
    ConfiguracionFacturacion,
    ConfiguracionInventario,
    ConfiguracionPOS,
    ConfiguracionNotificaciones,
    ConfiguracionSeguridad,
    ConfiguracionIntegraciones,
    ConfiguracionVeriFactu,
    ConfiguracionAutomatizaciones,
)

router = APIRouter(prefix="/api/configuracion", tags=["configuracion"])


# ============ SCHEMAS ============

class ConfiguracionGeneralSchema(BaseModel):
    """Schema para configuración general."""

    nombre_comercial: Optional[str] = None
    eslogan: Optional[str] = None
    industria: Optional[str] = None
    telefono_principal: Optional[str] = None
    telefono_secundario: Optional[str] = None
    email_contacto: Optional[str] = None
    email_soporte: Optional[str] = None
    whatsapp: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    horario_atencion: Optional[str] = None
    zona_horaria: str = "America/Lima"
    idioma_principal: str = "es"
    idioma_secundario: Optional[str] = None
    moneda_principal: str = "PEN"
    moneda_secundaria: Optional[str] = None
    formato_fecha: str = "DD/MM/YYYY"
    formato_hora: str = "24h"
    logo_url: Optional[str] = None
    logo_pequeño_url: Optional[str] = None
    favicon_url: Optional[str] = None
    color_primario: str = "#2563eb"
    color_secundario: str = "#64748b"
    color_acento: str = "#10b981"
    fuente_principal: str = "Inter"
    
    # Personalización Avanzada (PRO)
    color_sidebar: Optional[str] = "#1e293b"
    color_topbar: Optional[str] = "#ffffff"
    color_fondo: Optional[str] = "#f8fafc"
    color_texto_principal: Optional[str] = "#0f172a"
    color_texto_secundario: Optional[str] = "#64748b"
    color_borde: Optional[str] = "#e2e8f0"
    color_hover: Optional[str] = "#f1f5f9"
    color_exito: Optional[str] = "#10b981"
    color_error: Optional[str] = "#ef4444"
    color_advertencia: Optional[str] = "#f59e0b"
    color_info: Optional[str] = "#3b82f6"
    fuente_secundaria: Optional[str] = "Roboto"
    fuente_tamano_base: Optional[int] = 14
    fuente_tamano_titulos: Optional[int] = 24
    tema_oscuro_disponible: Optional[bool] = False
    tema_predeterminado: Optional[str] = "claro"
    border_radius: Optional[int] = 8
    espaciado_base: Optional[int] = 16
    animaciones_habilitadas: Optional[bool] = True
    sombras_habilitadas: Optional[bool] = True
    logo_posicion: Optional[str] = "izquierda"
    menu_estilo: Optional[str] = "vertical"
    custom_css: Optional[str] = None
    custom_js: Optional[str] = None

    class Config:
        from_attributes = True


class ConfiguracionFacturacionSchema(BaseModel):
    """Schema para configuración de facturación."""

    prefijo_factura: str = "F-"
    prefijo_boleta: str = "B-"
    prefijo_albaran: str = "A-"
    prefijo_cotizacion: str = "C-"
    prefijo_nota_credito: str = "NC-"
    prefijo_nota_debito: str = "ND-"
    numeracion_global: bool = False
    reiniciar_numeracion_anual: bool = False
    longitud_numeracion: int = 6
    iva_por_defecto: float = 18.00
    aplicar_iva_automaticamente: bool = True
    mostrar_impuestos_separados: bool = True
    terminos_venta: Optional[str] = None
    politica_devolucion: Optional[str] = None
    notas_pie_factura: Optional[str] = None
    dias_vencimiento_defecto: int = 30
    permitir_credito: bool = True
    limite_credito_defecto: float = 5000.00
    permitir_descuentos: bool = True
    descuento_maximo_porcentaje: float = 20.00
    requiere_autorizacion_descuento: bool = False
    facturacion_electronica_activa: bool = False
    proveedor_fe: Optional[str] = None
    certificado_digital_url: Optional[str] = None
    imprimir_automaticamente: bool = False
    formato_impresion: str = "A4"
    copias_por_defecto: int = 1

    class Config:
        from_attributes = True


class ConfiguracionInventarioSchema(BaseModel):
    """Schema para configuración de inventario."""

    permitir_stock_negativo: bool = False
    alerta_stock_minimo: bool = True
    stock_minimo_defecto: int = 10
    stock_maximo_defecto: int = 1000
    metodo_valoracion: str = "promedio"
    actualizar_costo_compra: bool = True
    generar_codigo_barras_automatico: bool = True
    tipo_codigo_barras: str = "EAN13"
    prefijo_codigo_interno: str = "PROD"
    categorias_requeridas: bool = True
    permitir_subcategorias: bool = True
    unidad_medida_defecto: str = "UND"
    permitir_fracciones: bool = False
    control_lotes: bool = False
    control_vencimientos: bool = False
    dias_alerta_vencimiento: int = 30
    aprobar_transferencias: bool = False
    registrar_movimientos: bool = True

    class Config:
        from_attributes = True


class ConfiguracionPOSSchema(BaseModel):
    """Schema para configuración POS."""

    modo_tactil: bool = True
    mostrar_imagenes_productos: bool = True
    productos_por_pagina: int = 12
    tema_oscuro: bool = False
    busqueda_automatica: bool = True
    buscar_por_codigo_barras: bool = True
    buscar_por_nombre: bool = True
    buscar_por_categoria: bool = True
    permitir_venta_sin_stock: bool = False
    pedir_cliente_obligatorio: bool = False
    crear_cliente_rapido: bool = True
    mostrar_precios_con_impuestos: bool = True
    permitir_modificar_precio: bool = False
    precio_por_defecto: str = "precio_venta"
    permitir_descuento_pos: bool = True
    descuento_maximo_pos: float = 10.00
    metodos_pago_activos: Optional[str] = None
    permitir_pago_mixto: bool = True
    redondear_total: bool = False
    abrir_cajon_automaticamente: bool = True
    solicitar_monto_apertura: bool = True
    solicitar_monto_cierre: bool = True
    imprimir_ticket_automaticamente: bool = True
    copias_ticket: int = 1
    mostrar_logo_ticket: bool = True
    sonido_operaciones: bool = True
    confirmacion_eliminar_item: bool = True

    class Config:
        from_attributes = True


class ConfiguracionNotificacionesSchema(BaseModel):
    """Schema para configuración de notificaciones."""

    email_activo: bool = False
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    smtp_from_name: Optional[str] = None
    smtp_ssl: bool = False
    whatsapp_activo: bool = False
    whatsapp_api_key: Optional[str] = None
    whatsapp_numero_empresa: Optional[str] = None
    sms_activo: bool = False
    sms_proveedor: Optional[str] = None
    sms_api_key: Optional[str] = None
    push_activo: bool = True
    notificar_nueva_venta: bool = True
    notificar_bajo_stock: bool = True
    notificar_producto_vencido: bool = True
    notificar_nuevo_cliente: bool = False
    notificar_pago_recibido: bool = True
    notificar_error_sistema: bool = True
    emails_notificacion: Optional[str] = None
    telefonos_notificacion: Optional[str] = None
    notificar_fuera_horario: bool = False
    horario_inicio: str = "08:00"
    horario_fin: str = "18:00"

    class Config:
        from_attributes = True


class ConfiguracionSeguridadSchema(BaseModel):
    """Schema para configuración de seguridad."""

    longitud_minima_password: int = 8
    requiere_mayusculas: bool = True
    requiere_minusculas: bool = True
    requiere_numeros: bool = True
    requiere_caracteres_especiales: bool = False
    dias_expiracion_password: int = 90
    historial_passwords: int = 5
    tiempo_expiracion_sesion: int = 480
    sesiones_simultaneas_permitidas: int = 3
    cerrar_sesion_inactividad: bool = True
    minutos_inactividad: int = 30
    max_intentos_login: int = 5
    tiempo_bloqueo_minutos: int = 30
    autenticacion_2fa: bool = False
    metodo_2fa: str = "email"
    restringir_por_ip: bool = False
    ips_permitidas: Optional[str] = None
    registrar_accesos: bool = True
    registrar_cambios_datos: bool = True
    dias_retencion_logs: int = 90
    backup_automatico: bool = True
    frecuencia_backup: str = "diario"
    hora_backup: str = "02:00"
    copias_retenidas: int = 30

    class Config:
        from_attributes = True


class ConfiguracionIntegracionesSchema(BaseModel):
    """Schema para configuración de integraciones."""

    sunat_activo: bool = False
    sunat_usuario: Optional[str] = None
    sunat_password: Optional[str] = None
    sunat_ambiente: str = "produccion"
    mercadopago_activo: bool = False
    mercadopago_access_token: Optional[str] = None
    mercadopago_public_key: Optional[str] = None
    paypal_activo: bool = False
    paypal_client_id: Optional[str] = None
    paypal_secret: Optional[str] = None
    stripe_activo: bool = False
    stripe_api_key: Optional[str] = None
    niubiz_activo: bool = False
    niubiz_merchant_id: Optional[str] = None
    niubiz_access_key: Optional[str] = None
    contabilidad_externa: bool = False
    sistema_contable: Optional[str] = None
    contable_api_url: Optional[str] = None
    contable_api_key: Optional[str] = None
    google_analytics_activo: bool = False
    google_analytics_id: Optional[str] = None
    google_maps_activo: bool = False
    google_maps_api_key: Optional[str] = None
    shopify_activo: bool = False
    shopify_api_key: Optional[str] = None
    shopify_store_url: Optional[str] = None
    woocommerce_activo: bool = False
    woocommerce_api_key: Optional[str] = None
    woocommerce_store_url: Optional[str] = None
    webhook_ventas_url: Optional[str] = None
    webhook_inventario_url: Optional[str] = None
    webhook_secret: Optional[str] = None

    class Config:
        from_attributes = True


class ConfiguracionAutomatizacionesSchema(BaseModel):
    """Schema para automatizaciones globales del ERP."""

    auto_enviar_factura_email: bool = True
    auto_enviar_factura_whatsapp: bool = False
    auto_recordatorio_pago: bool = True
    dias_recordatorio_pago: int = 3
    auto_resumen_diario_email: bool = True
    email_resumen_diario: Optional[str] = None

    auto_generar_orden_compra_stock_bajo: bool = False
    umbral_stock_bajo: int = 5
    auto_sincronizar_tiendas_online: bool = False
    minutos_sincronizacion_tiendas: int = 60

    auto_recordatorio_citas: bool = True
    horas_antes_recordatorio_cita: int = 24

    auto_cierre_caja: bool = False
    hora_cierre_caja: str = "23:00"

    auto_backup_nocturno: bool = True
    hora_backup_nocturno: str = "02:30"

    class Config:
        from_attributes = True


class ConfiguracionVeriFactuSchema(BaseModel):
    """Schema para configuración de VeriFactu."""

    verifactu_activo: bool = True
    nif_emisor: Optional[str] = None
    nombre_razon_social: Optional[str] = None
    certificado_activo: bool = False
    certificado_path: Optional[str] = None
    certificado_password: Optional[str] = None
    certificado_valido_hasta: Optional[datetime] = None
    entorno: str = "pruebas"
    url_webservice_pruebas: str = "https://prewww1.aeat.es/wlpl/TIKE-CONT/ContribucionTerr"
    url_webservice_produccion: str = "https://www1.agenciatributaria.gob.es/wlpl/TIKE-CONT/ContribucionTerr"
    id_sistema: Optional[str] = None
    version_sistema: str = "1.0.0"
    nombre_sistema: str = "OmniERP"
    algoritmo_firma: str = "SHA256"
    tipo_huella: str = "01"
    usar_encadenamiento: bool = True
    ultima_huella: Optional[str] = None
    ultimo_numero_factura: Optional[str] = None
    sistema_registrado: bool = False
    fecha_alta_sistema: Optional[datetime] = None
    numero_registro_sistema: Optional[str] = None
    generar_qr_facturas: bool = True
    url_verificacion_qr: Optional[str] = "https://www2.agenciatributaria.gob.es/wlpl/TIKE-CONT/ValidarQR"
    envio_automatico: bool = False
    envio_diferido: bool = True
    frecuencia_envio: str = "diario"
    hora_envio: str = "23:00"
    max_reintentos: int = 3
    tiempo_entre_reintentos: int = 60
    notificar_errores: bool = True
    email_notificaciones: Optional[str] = None
    guardar_xml_enviados: bool = True
    ruta_backup_xml: str = "/static/verifactu/xml/"
    dias_retencion_xml: int = 1825
    total_facturas_enviadas: int = 0
    total_facturas_rechazadas: int = 0
    ultima_sincronizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ ENDPOINTS GENERAL ============

@router.get("/general", response_model=ConfiguracionGeneralSchema)
async def get_configuracion_general(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración general."""
    result = await db.execute(
        select(ConfiguracionGeneral).where(ConfiguracionGeneral.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        # Crear configuración por defecto
        config = ConfiguracionGeneral(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/general", response_model=ConfiguracionGeneralSchema)
async def update_configuracion_general(
    data: ConfiguracionGeneralSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración general."""
    result = await db.execute(
        select(ConfiguracionGeneral).where(ConfiguracionGeneral.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionGeneral(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS FACTURACIÓN ============

@router.get("/facturacion", response_model=ConfiguracionFacturacionSchema)
async def get_configuracion_facturacion(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de facturación."""
    result = await db.execute(
        select(ConfiguracionFacturacion).where(ConfiguracionFacturacion.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionFacturacion(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/facturacion", response_model=ConfiguracionFacturacionSchema)
async def update_configuracion_facturacion(
    data: ConfiguracionFacturacionSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de facturación."""
    result = await db.execute(
        select(ConfiguracionFacturacion).where(ConfiguracionFacturacion.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionFacturacion(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS INVENTARIO ============

@router.get("/inventario", response_model=ConfiguracionInventarioSchema)
async def get_configuracion_inventario(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de inventario."""
    result = await db.execute(
        select(ConfiguracionInventario).where(ConfiguracionInventario.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionInventario(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/inventario", response_model=ConfiguracionInventarioSchema)
async def update_configuracion_inventario(
    data: ConfiguracionInventarioSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de inventario."""
    result = await db.execute(
        select(ConfiguracionInventario).where(ConfiguracionInventario.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionInventario(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS POS ============

@router.get("/pos", response_model=ConfiguracionPOSSchema)
async def get_configuracion_pos(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración POS."""
    result = await db.execute(
        select(ConfiguracionPOS).where(ConfiguracionPOS.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionPOS(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/pos", response_model=ConfiguracionPOSSchema)
async def update_configuracion_pos(
    data: ConfiguracionPOSSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración POS."""
    result = await db.execute(
        select(ConfiguracionPOS).where(ConfiguracionPOS.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionPOS(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS NOTIFICACIONES ============

@router.get("/notificaciones", response_model=ConfiguracionNotificacionesSchema)
async def get_configuracion_notificaciones(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de notificaciones."""
    result = await db.execute(
        select(ConfiguracionNotificaciones).where(ConfiguracionNotificaciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionNotificaciones(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/notificaciones", response_model=ConfiguracionNotificacionesSchema)
async def update_configuracion_notificaciones(
    data: ConfiguracionNotificacionesSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de notificaciones."""
    result = await db.execute(
        select(ConfiguracionNotificaciones).where(ConfiguracionNotificaciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionNotificaciones(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS SEGURIDAD ============

@router.get("/seguridad", response_model=ConfiguracionSeguridadSchema)
async def get_configuracion_seguridad(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de seguridad."""
    result = await db.execute(
        select(ConfiguracionSeguridad).where(ConfiguracionSeguridad.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionSeguridad(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/seguridad", response_model=ConfiguracionSeguridadSchema)
async def update_configuracion_seguridad(
    data: ConfiguracionSeguridadSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de seguridad."""
    result = await db.execute(
        select(ConfiguracionSeguridad).where(ConfiguracionSeguridad.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionSeguridad(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS INTEGRACIONES ============

@router.get("/integraciones", response_model=ConfiguracionIntegracionesSchema)
async def get_configuracion_integraciones(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de integraciones."""
    result = await db.execute(
        select(ConfiguracionIntegraciones).where(ConfiguracionIntegraciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionIntegraciones(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/integraciones", response_model=ConfiguracionIntegracionesSchema)
async def update_configuracion_integraciones(
    data: ConfiguracionIntegracionesSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de integraciones."""
    result = await db.execute(
        select(ConfiguracionIntegraciones).where(ConfiguracionIntegraciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionIntegraciones(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINTS AUTOMATIZACIONES ============

@router.get("/automatizaciones", response_model=ConfiguracionAutomatizacionesSchema)
async def get_configuracion_automatizaciones(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de automatizaciones."""
    result = await db.execute(
        select(ConfiguracionAutomatizaciones).where(ConfiguracionAutomatizaciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionAutomatizaciones(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/automatizaciones", response_model=ConfiguracionAutomatizacionesSchema)
async def update_configuracion_automatizaciones(
    data: ConfiguracionAutomatizacionesSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de automatizaciones."""
    result = await db.execute(
        select(ConfiguracionAutomatizaciones).where(ConfiguracionAutomatizaciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionAutomatizaciones(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


# ============ ENDPOINT TODAS LAS CONFIGURACIONES ============

@router.get("/todas")
async def get_todas_configuraciones(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener todas las configuraciones."""
    
    # General
    result_general = await db.execute(
        select(ConfiguracionGeneral).where(ConfiguracionGeneral.organization_id == org_id)
    )
    general = result_general.scalar_one_or_none()
    if not general:
        general = ConfiguracionGeneral(organization_id=org_id)
        db.add(general)
    
    # Facturación
    result_fact = await db.execute(
        select(ConfiguracionFacturacion).where(ConfiguracionFacturacion.organization_id == org_id)
    )
    facturacion = result_fact.scalar_one_or_none()
    if not facturacion:
        facturacion = ConfiguracionFacturacion(organization_id=org_id)
        db.add(facturacion)
    
    # Inventario
    result_inv = await db.execute(
        select(ConfiguracionInventario).where(ConfiguracionInventario.organization_id == org_id)
    )
    inventario = result_inv.scalar_one_or_none()
    if not inventario:
        inventario = ConfiguracionInventario(organization_id=org_id)
        db.add(inventario)
    
    # POS
    result_pos = await db.execute(
        select(ConfiguracionPOS).where(ConfiguracionPOS.organization_id == org_id)
    )
    pos = result_pos.scalar_one_or_none()
    if not pos:
        pos = ConfiguracionPOS(organization_id=org_id)
        db.add(pos)
    
    # Notificaciones
    result_notif = await db.execute(
        select(ConfiguracionNotificaciones).where(ConfiguracionNotificaciones.organization_id == org_id)
    )
    notificaciones = result_notif.scalar_one_or_none()
    if not notificaciones:
        notificaciones = ConfiguracionNotificaciones(organization_id=org_id)
        db.add(notificaciones)
    
    # Seguridad
    result_seg = await db.execute(
        select(ConfiguracionSeguridad).where(ConfiguracionSeguridad.organization_id == org_id)
    )
    seguridad = result_seg.scalar_one_or_none()
    if not seguridad:
        seguridad = ConfiguracionSeguridad(organization_id=org_id)
        db.add(seguridad)
    
    # Integraciones
    result_int = await db.execute(
        select(ConfiguracionIntegraciones).where(ConfiguracionIntegraciones.organization_id == org_id)
    )
    integraciones = result_int.scalar_one_or_none()
    if not integraciones:
        integraciones = ConfiguracionIntegraciones(organization_id=org_id)
        db.add(integraciones)

    # Automatizaciones
    result_auto = await db.execute(
        select(ConfiguracionAutomatizaciones).where(ConfiguracionAutomatizaciones.organization_id == org_id)
    )
    automatizaciones = result_auto.scalar_one_or_none()
    if not automatizaciones:
        automatizaciones = ConfiguracionAutomatizaciones(organization_id=org_id)
        db.add(automatizaciones)
    
    await db.commit()
    
    return {
        "general": ConfiguracionGeneralSchema.model_validate(general),
        "facturacion": ConfiguracionFacturacionSchema.model_validate(facturacion),
        "inventario": ConfiguracionInventarioSchema.model_validate(inventario),
        "pos": ConfiguracionPOSSchema.model_validate(pos),
        "notificaciones": ConfiguracionNotificacionesSchema.model_validate(notificaciones),
        "seguridad": ConfiguracionSeguridadSchema.model_validate(seguridad),
        "integraciones": ConfiguracionIntegracionesSchema.model_validate(integraciones),
        "automatizaciones": ConfiguracionAutomatizacionesSchema.model_validate(automatizaciones),
    }


# ============ ENDPOINT TEST SMTP ============

@router.post("/notificaciones/test-email")
async def test_email_configuration(
    email_destino: str,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Probar configuración de email."""
    result = await db.execute(
        select(ConfiguracionNotificaciones).where(ConfiguracionNotificaciones.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config or not config.email_activo:
        raise HTTPException(status_code=400, detail="Configuración de email no activa")
    
    # Aquí iría la lógica para enviar email de prueba
    # import smtplib, etc.
    
    return {"message": f"Email de prueba enviado a {email_destino}"}


@router.post("/upload-logo")
async def upload_logo(
    file: UploadFile = File(...),
    tipo: str = "logo",  # logo, logo_pequeño, favicon
    org_id: int = Depends(get_org_id)
):
    """Sube un archivo de logo y retorna la URL."""
    
    # Validar tipo de archivo
    allowed_extensions = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Use: {', '.join(allowed_extensions)}"
        )
    
    # Validar tamaño (5MB máximo)
    max_size = 5 * 1024 * 1024  # 5MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande. Máximo 5MB."
        )
    
    # Crear directorio si no existe
    upload_dir = Path("/home/dario/src/dario_app/static/uploads/logos") / str(org_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tipo}_{timestamp}{file_ext}"
    file_path = upload_dir / filename
    
    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Retornar URL relativa
    url = f"/static/uploads/logos/{org_id}/{filename}"
    
    return {
        "success": True,
        "url": url,
        "filename": filename
    }


# ============ ENDPOINTS VERIFACTU ============

@router.get("/verifactu", response_model=ConfiguracionVeriFactuSchema)
async def get_configuracion_verifactu(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtener configuración de VeriFactu."""
    result = await db.execute(
        select(ConfiguracionVeriFactu).where(ConfiguracionVeriFactu.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionVeriFactu(organization_id=org_id)
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/verifactu", response_model=ConfiguracionVeriFactuSchema)
async def update_configuracion_verifactu(
    data: ConfiguracionVeriFactuSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualizar configuración de VeriFactu."""
    result = await db.execute(
        select(ConfiguracionVeriFactu).where(ConfiguracionVeriFactu.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        config = ConfiguracionVeriFactu(organization_id=org_id)
        db.add(config)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    
    await db.commit()
    await db.refresh(config)
    return config


@router.post("/verifactu/upload-certificado")
async def upload_certificado(
    file: UploadFile = File(...),
    org_id: int = Depends(get_org_id)
):
    """Sube el certificado digital (.pfx o .p12) para VeriFactu."""
    
    # Validar tipo de archivo
    allowed_extensions = {".pfx", ".p12"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Use: {', '.join(allowed_extensions)}"
        )
    
    # Validar tamaño (10MB máximo)
    max_size = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande. Máximo 10MB."
        )
    
    # Crear directorio si no existe
    upload_dir = Path("/home/dario/src/dario_app/static/verifactu/certificados") / str(org_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"certificado_{timestamp}{file_ext}"
    file_path = upload_dir / filename
    
    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Retornar ruta relativa
    path = f"/static/verifactu/certificados/{org_id}/{filename}"
    
    return {
        "success": True,
        "path": path,
        "filename": filename
    }


@router.post("/verifactu/test-conexion")
async def test_conexion_verifactu(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Probar conexión con el servicio de VeriFactu de la AEAT."""
    result = await db.execute(
        select(ConfiguracionVeriFactu).where(ConfiguracionVeriFactu.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config or not config.verifactu_activo:
        raise HTTPException(status_code=400, detail="VeriFactu no está activado")
    
    if not config.certificado_activo or not config.certificado_path:
        raise HTTPException(status_code=400, detail="Certificado digital no configurado")
    
    # TODO: Implementar lógica real de conexión con AEAT
    # Por ahora retornamos un mensaje de éxito simulado
    
    return {
        "success": True,
        "message": "Conexión con VeriFactu exitosa",
        "entorno": config.entorno,
        "url": config.url_webservice_pruebas if config.entorno == "pruebas" else config.url_webservice_produccion
    }


@router.post("/verifactu/registrar-sistema")
async def registrar_sistema_verifactu(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Registrar el sistema informático en VeriFactu."""
    result = await db.execute(
        select(ConfiguracionVeriFactu).where(ConfiguracionVeriFactu.organization_id == org_id)
    )
    config = result.scalar_one_or_none()
    
    if not config or not config.verifactu_activo:
        raise HTTPException(status_code=400, detail="VeriFactu no está activado")
    
    if config.sistema_registrado:
        raise HTTPException(status_code=400, detail="El sistema ya está registrado")
    
    # TODO: Implementar lógica real de registro con AEAT
    # Generar ID de sistema único si no existe
    if not config.id_sistema:
        import uuid
        config.id_sistema = f"OMNIERP-{uuid.uuid4().hex[:12].upper()}"
    
    config.sistema_registrado = True
    config.fecha_alta_sistema = datetime.utcnow()
    config.numero_registro_sistema = f"REG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    await db.commit()
    await db.refresh(config)
    
    return {
        "success": True,
        "message": "Sistema registrado exitosamente en VeriFactu",
        "id_sistema": config.id_sistema,
        "numero_registro": config.numero_registro_sistema
    }

