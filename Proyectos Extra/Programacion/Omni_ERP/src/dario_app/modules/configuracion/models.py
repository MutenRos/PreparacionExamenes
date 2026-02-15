"""Modelos de configuración del sistema ERP."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ConfiguracionGeneral(Base):
    """Configuración general del sistema."""

    __tablename__ = "configuracion_general"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Información de la empresa
    nombre_comercial: Mapped[str] = mapped_column(String(255), nullable=True)
    eslogan: Mapped[str] = mapped_column(String(500), nullable=True)
    industria: Mapped[str] = mapped_column(String(100), nullable=True)  # retail, restaurante, farmacia, etc
    
    # Contacto
    telefono_principal: Mapped[str] = mapped_column(String(20), nullable=True)
    telefono_secundario: Mapped[str] = mapped_column(String(20), nullable=True)
    email_contacto: Mapped[str] = mapped_column(String(255), nullable=True)
    email_soporte: Mapped[str] = mapped_column(String(255), nullable=True)
    whatsapp: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Redes sociales
    facebook_url: Mapped[str] = mapped_column(String(500), nullable=True)
    instagram_url: Mapped[str] = mapped_column(String(500), nullable=True)
    twitter_url: Mapped[str] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Horarios
    horario_atencion: Mapped[str] = mapped_column(Text, nullable=True)  # JSON con horarios por día
    zona_horaria: Mapped[str] = mapped_column(String(50), default="Europe/Madrid", nullable=False)
    
    # Localización
    idioma_principal: Mapped[str] = mapped_column(String(10), default="es", nullable=False)
    idioma_secundario: Mapped[str] = mapped_column(String(10), nullable=True)
    moneda_principal: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    moneda_secundaria: Mapped[str] = mapped_column(String(3), nullable=True)
    formato_fecha: Mapped[str] = mapped_column(String(20), default="DD/MM/YYYY", nullable=False)
    formato_hora: Mapped[str] = mapped_column(String(20), default="24h", nullable=False)
    
    # Branding
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    logo_pequeño_url: Mapped[str] = mapped_column(String(500), nullable=True)
    favicon_url: Mapped[str] = mapped_column(String(500), nullable=True)
    color_primario: Mapped[str] = mapped_column(String(7), default="#2563eb", nullable=False)
    color_secundario: Mapped[str] = mapped_column(String(7), default="#64748b", nullable=False)
    color_acento: Mapped[str] = mapped_column(String(7), default="#10b981", nullable=False)
    fuente_principal: Mapped[str] = mapped_column(String(50), default="Inter", nullable=False)
    
    # Personalización Avanzada (PRO)
    color_sidebar: Mapped[str] = mapped_column(String(7), default="#1e293b", nullable=True)
    color_topbar: Mapped[str] = mapped_column(String(7), default="#ffffff", nullable=True)
    color_fondo: Mapped[str] = mapped_column(String(7), default="#f8fafc", nullable=True)
    color_texto_principal: Mapped[str] = mapped_column(String(7), default="#0f172a", nullable=True)
    color_texto_secundario: Mapped[str] = mapped_column(String(7), default="#64748b", nullable=True)
    color_borde: Mapped[str] = mapped_column(String(7), default="#e2e8f0", nullable=True)
    color_hover: Mapped[str] = mapped_column(String(7), default="#f1f5f9", nullable=True)
    color_exito: Mapped[str] = mapped_column(String(7), default="#10b981", nullable=True)
    color_error: Mapped[str] = mapped_column(String(7), default="#ef4444", nullable=True)
    color_advertencia: Mapped[str] = mapped_column(String(7), default="#f59e0b", nullable=True)
    color_info: Mapped[str] = mapped_column(String(7), default="#3b82f6", nullable=True)
    
    fuente_secundaria: Mapped[str] = mapped_column(String(50), default="Roboto", nullable=True)
    fuente_tamano_base: Mapped[int] = mapped_column(Integer, default=14, nullable=True)  # px
    fuente_tamano_titulos: Mapped[int] = mapped_column(Integer, default=24, nullable=True)  # px
    
    tema_oscuro_disponible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    tema_predeterminado: Mapped[str] = mapped_column(String(20), default="claro", nullable=True)  # claro, oscuro, auto
    
    border_radius: Mapped[int] = mapped_column(Integer, default=8, nullable=True)  # px
    espaciado_base: Mapped[int] = mapped_column(Integer, default=16, nullable=True)  # px
    
    animaciones_habilitadas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    sombras_habilitadas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    
    logo_posicion: Mapped[str] = mapped_column(String(20), default="izquierda", nullable=True)  # izquierda, centro, derecha
    menu_estilo: Mapped[str] = mapped_column(String(20), default="vertical", nullable=True)  # vertical, horizontal, compacto
    
    custom_css: Mapped[str] = mapped_column(Text, nullable=True)  # CSS personalizado
    custom_js: Mapped[str] = mapped_column(Text, nullable=True)  # JavaScript personalizado
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionFacturacion(Base):
    """Configuración de facturación y documentos."""

    __tablename__ = "configuracion_facturacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Numeración
    prefijo_factura: Mapped[str] = mapped_column(String(10), default="F-", nullable=False)
    prefijo_boleta: Mapped[str] = mapped_column(String(10), default="FS-", nullable=False)
    prefijo_albaran: Mapped[str] = mapped_column(String(10), default="A-", nullable=False)
    prefijo_cotizacion: Mapped[str] = mapped_column(String(10), default="C-", nullable=False)
    prefijo_nota_credito: Mapped[str] = mapped_column(String(10), default="NC-", nullable=False)
    prefijo_nota_debito: Mapped[str] = mapped_column(String(10), default="ND-", nullable=False)
    
    numeracion_global: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reiniciar_numeracion_anual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    longitud_numeracion: Mapped[int] = mapped_column(Integer, default=6, nullable=False)  # F-000001
    
    # Impuestos
    iva_por_defecto: Mapped[float] = mapped_column(Numeric(5, 2), default=21.00, nullable=False)
    aplicar_iva_automaticamente: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mostrar_impuestos_separados: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Términos y condiciones
    terminos_venta: Mapped[str] = mapped_column(Text, nullable=True)
    politica_devolucion: Mapped[str] = mapped_column(Text, nullable=True)
    notas_pie_factura: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Condiciones de pago
    dias_vencimiento_defecto: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    permitir_credito: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    limite_credito_defecto: Mapped[float] = mapped_column(Numeric(12, 2), default=5000.00, nullable=False)
    
    # Descuentos
    permitir_descuentos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    descuento_maximo_porcentaje: Mapped[float] = mapped_column(Numeric(5, 2), default=20.00, nullable=False)
    requiere_autorizacion_descuento: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Documentos electrónicos
    facturacion_electronica_activa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    proveedor_fe: Mapped[str] = mapped_column(String(100), nullable=True)  # SUNAT, Facturador, etc
    certificado_digital_url: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Impresión
    imprimir_automaticamente: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    formato_impresion: Mapped[str] = mapped_column(String(20), default="A4", nullable=False)  # A4, Ticket
    copias_por_defecto: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionInventario(Base):
    """Configuración de inventario y stock."""

    __tablename__ = "configuracion_inventario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Gestión de stock
    permitir_stock_negativo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    alerta_stock_minimo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    stock_minimo_defecto: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    stock_maximo_defecto: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    
    # Valorización
    metodo_valoracion: Mapped[str] = mapped_column(String(20), default="promedio", nullable=False)  # FIFO, LIFO, promedio
    actualizar_costo_compra: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Códigos de barras
    generar_codigo_barras_automatico: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tipo_codigo_barras: Mapped[str] = mapped_column(String(20), default="EAN13", nullable=False)
    prefijo_codigo_interno: Mapped[str] = mapped_column(String(10), default="PROD", nullable=False)
    
    # Categorización
    categorias_requeridas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    permitir_subcategorias: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Unidades de medida
    unidad_medida_defecto: Mapped[str] = mapped_column(String(10), default="UND", nullable=False)
    permitir_fracciones: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Lotes y vencimientos
    control_lotes: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    control_vencimientos: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    dias_alerta_vencimiento: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Transferencias
    aprobar_transferencias: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Auditoría
    registrar_movimientos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionPOS(Base):
    """Configuración del punto de venta."""

    __tablename__ = "configuracion_pos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Interfaz
    modo_tactil: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mostrar_imagenes_productos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    productos_por_pagina: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    tema_oscuro: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Búsqueda
    busqueda_automatica: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    buscar_por_codigo_barras: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    buscar_por_nombre: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    buscar_por_categoria: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Ventas
    permitir_venta_sin_stock: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pedir_cliente_obligatorio: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    crear_cliente_rapido: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Precios
    mostrar_precios_con_impuestos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    permitir_modificar_precio: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    precio_por_defecto: Mapped[str] = mapped_column(String(20), default="precio_venta", nullable=False)
    
    # Descuentos
    permitir_descuento_pos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    descuento_maximo_pos: Mapped[float] = mapped_column(Numeric(5, 2), default=10.00, nullable=False)
    
    # Pagos
    metodos_pago_activos: Mapped[str] = mapped_column(Text, nullable=True)  # JSON: ["efectivo", "tarjeta", "yape"]
    permitir_pago_mixto: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    redondear_total: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Caja
    abrir_cajon_automaticamente: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    solicitar_monto_apertura: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    solicitar_monto_cierre: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Impresión
    imprimir_ticket_automaticamente: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    copias_ticket: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    mostrar_logo_ticket: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Otras opciones
    sonido_operaciones: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    confirmacion_eliminar_item: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionNotificaciones(Base):
    """Configuración de notificaciones y alertas."""

    __tablename__ = "configuracion_notificaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Email
    email_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    smtp_host: Mapped[str] = mapped_column(String(255), nullable=True)
    smtp_port: Mapped[int] = mapped_column(Integer, default=587, nullable=True)
    smtp_user: Mapped[str] = mapped_column(String(255), nullable=True)
    smtp_password: Mapped[str] = mapped_column(String(255), nullable=True)  # Encriptado
    smtp_from_email: Mapped[str] = mapped_column(String(255), nullable=True)
    smtp_from_name: Mapped[str] = mapped_column(String(255), nullable=True)
    smtp_ssl: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # WhatsApp
    whatsapp_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    whatsapp_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    whatsapp_numero_empresa: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # SMS
    sms_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sms_proveedor: Mapped[str] = mapped_column(String(100), nullable=True)  # Twilio, etc
    sms_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Notificaciones push
    push_activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Eventos a notificar
    notificar_nueva_venta: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notificar_bajo_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notificar_producto_vencido: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notificar_nuevo_cliente: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notificar_pago_recibido: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notificar_error_sistema: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Destinatarios
    emails_notificacion: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array
    telefonos_notificacion: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array
    
    # Horarios
    notificar_fuera_horario: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    horario_inicio: Mapped[str] = mapped_column(String(5), default="08:00", nullable=False)
    horario_fin: Mapped[str] = mapped_column(String(5), default="18:00", nullable=False)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionSeguridad(Base):
    """Configuración de seguridad del sistema."""

    __tablename__ = "configuracion_seguridad"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Contraseñas
    longitud_minima_password: Mapped[int] = mapped_column(Integer, default=8, nullable=False)
    requiere_mayusculas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requiere_minusculas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requiere_numeros: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requiere_caracteres_especiales: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    dias_expiracion_password: Mapped[int] = mapped_column(Integer, default=90, nullable=False)
    historial_passwords: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    
    # Sesiones
    tiempo_expiracion_sesion: Mapped[int] = mapped_column(Integer, default=480, nullable=False)  # minutos
    sesiones_simultaneas_permitidas: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    cerrar_sesion_inactividad: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    minutos_inactividad: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Intentos de login
    max_intentos_login: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    tiempo_bloqueo_minutos: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Autenticación de dos factores
    autenticacion_2fa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metodo_2fa: Mapped[str] = mapped_column(String(20), default="email", nullable=False)  # email, sms, app
    
    # IP y ubicación
    restringir_por_ip: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ips_permitidas: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array
    
    # Auditoría
    registrar_accesos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    registrar_cambios_datos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    dias_retencion_logs: Mapped[int] = mapped_column(Integer, default=90, nullable=False)
    
    # Copias de seguridad
    backup_automatico: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    frecuencia_backup: Mapped[str] = mapped_column(String(20), default="diario", nullable=False)
    hora_backup: Mapped[str] = mapped_column(String(5), default="02:00", nullable=False)
    copias_retenidas: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionIntegraciones(Base):
    """Configuración de integraciones con servicios externos."""

    __tablename__ = "configuracion_integraciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Facturación electrónica
    sunat_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sunat_usuario: Mapped[str] = mapped_column(String(255), nullable=True)
    sunat_password: Mapped[str] = mapped_column(String(255), nullable=True)
    sunat_ambiente: Mapped[str] = mapped_column(String(20), default="produccion", nullable=False)
    
    # Pagos online
    mercadopago_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mercadopago_access_token: Mapped[str] = mapped_column(String(500), nullable=True)
    mercadopago_public_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    paypal_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    paypal_client_id: Mapped[str] = mapped_column(String(500), nullable=True)
    paypal_secret: Mapped[str] = mapped_column(String(500), nullable=True)
    
    stripe_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stripe_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Pasarelas locales
    niubiz_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    niubiz_merchant_id: Mapped[str] = mapped_column(String(255), nullable=True)
    niubiz_access_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Contabilidad
    contabilidad_externa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sistema_contable: Mapped[str] = mapped_column(String(100), nullable=True)
    contable_api_url: Mapped[str] = mapped_column(String(500), nullable=True)
    contable_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Google
    google_analytics_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    google_analytics_id: Mapped[str] = mapped_column(String(100), nullable=True)
    
    google_maps_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    google_maps_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Marketplaces
    shopify_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    shopify_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    shopify_store_url: Mapped[str] = mapped_column(String(500), nullable=True)
    
    woocommerce_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    woocommerce_api_key: Mapped[str] = mapped_column(String(500), nullable=True)
    woocommerce_store_url: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Webhooks
    webhook_ventas_url: Mapped[str] = mapped_column(String(500), nullable=True)
    webhook_inventario_url: Mapped[str] = mapped_column(String(500), nullable=True)
    webhook_secret: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionAutomatizaciones(Base):
    """Automatizaciones globales del ERP (ventas, stock, agenda y sistema)."""

    __tablename__ = "configuracion_automatizaciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Ventas y cobranzas
    auto_enviar_factura_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auto_enviar_factura_whatsapp: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    auto_recordatorio_pago: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    dias_recordatorio_pago: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    auto_resumen_diario_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_resumen_diario: Mapped[str] = mapped_column(String(500), nullable=True)

    # Inventario y compras
    auto_generar_orden_compra_stock_bajo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    umbral_stock_bajo: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    auto_sincronizar_tiendas_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    minutos_sincronizacion_tiendas: Mapped[int] = mapped_column(Integer, default=60, nullable=False)

    # Agenda y servicios
    auto_recordatorio_citas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    horas_antes_recordatorio_cita: Mapped[int] = mapped_column(Integer, default=24, nullable=False)

    # POS y caja
    auto_cierre_caja: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hora_cierre_caja: Mapped[str] = mapped_column(String(5), default="23:00", nullable=False)

    # Sistema
    auto_backup_nocturno: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hora_backup_nocturno: Mapped[str] = mapped_column(String(5), default="02:30", nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class ConfiguracionVeriFactu(Base):
    """Configuración de VeriFactu (AEAT España)."""

    __tablename__ = "configuracion_verifactu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id"), nullable=False, index=True
    )

    # Estado del sistema
    verifactu_activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Datos fiscales
    nif_emisor: Mapped[str] = mapped_column(String(20), nullable=True)
    nombre_razon_social: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Certificado digital
    certificado_activo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    certificado_path: Mapped[str] = mapped_column(String(500), nullable=True)  # Ruta al archivo .pfx/.p12
    certificado_password: Mapped[str] = mapped_column(String(255), nullable=True)  # Encriptado
    certificado_valido_hasta: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Configuración de envío a AEAT
    entorno: Mapped[str] = mapped_column(String(20), default="pruebas", nullable=False)  # pruebas, produccion
    url_webservice_pruebas: Mapped[str] = mapped_column(
        String(500), 
        default="https://prewww1.aeat.es/wlpl/TIKE-CONT/ContribucionTerr", 
        nullable=False
    )
    url_webservice_produccion: Mapped[str] = mapped_column(
        String(500), 
        default="https://www1.agenciatributaria.gob.es/wlpl/TIKE-CONT/ContribucionTerr", 
        nullable=False
    )
    
    # Sistemas informáticos
    id_sistema: Mapped[str] = mapped_column(String(50), nullable=True)  # Identificador único del sistema
    version_sistema: Mapped[str] = mapped_column(String(20), default="1.0.0", nullable=False)
    nombre_sistema: Mapped[str] = mapped_column(String(100), default="OmniERP", nullable=False)
    
    # Configuración de firma
    algoritmo_firma: Mapped[str] = mapped_column(String(50), default="SHA256", nullable=False)
    tipo_huella: Mapped[str] = mapped_column(String(20), default="01", nullable=False)  # 01=Sin encadenamiento, 02=Con encadenamiento
    
    # Encadenamiento de facturas
    usar_encadenamiento: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    ultima_huella: Mapped[str] = mapped_column(String(500), nullable=True)  # Última huella generada
    ultimo_numero_factura: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Registro de alta de sistema
    sistema_registrado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_alta_sistema: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    numero_registro_sistema: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Configuración de QR
    generar_qr_facturas: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    url_verificacion_qr: Mapped[str] = mapped_column(
        String(500), 
        default="https://www2.agenciatributaria.gob.es/wlpl/TIKE-CONT/ValidarQR", 
        nullable=True
    )
    
    # Envío automático
    envio_automatico: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    envio_diferido: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)  # Envío en lote vs tiempo real
    frecuencia_envio: Mapped[str] = mapped_column(String(20), default="diario", nullable=False)  # tiempo_real, horario, diario
    hora_envio: Mapped[str] = mapped_column(String(5), default="23:00", nullable=False)  # Para envío programado
    
    # Reintentos
    max_reintentos: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    tiempo_entre_reintentos: Mapped[int] = mapped_column(Integer, default=60, nullable=False)  # Segundos
    
    # Notificaciones
    notificar_errores: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_notificaciones: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Backup y registro
    guardar_xml_enviados: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    ruta_backup_xml: Mapped[str] = mapped_column(String(500), default="/static/verifactu/xml/", nullable=False)
    dias_retencion_xml: Mapped[int] = mapped_column(Integer, default=1825, nullable=False)  # 5 años por defecto
    
    # Estadísticas
    total_facturas_enviadas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_facturas_rechazadas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ultima_sincronizacion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Metadatos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
