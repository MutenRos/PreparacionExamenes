"""Módulo de configuración del sistema."""

from .models import (
    ConfiguracionGeneral,
    ConfiguracionFacturacion,
    ConfiguracionInventario,
    ConfiguracionPOS,
    ConfiguracionNotificaciones,
    ConfiguracionSeguridad,
    ConfiguracionIntegraciones,
    ConfiguracionAutomatizaciones,
)

__all__ = [
    "ConfiguracionGeneral",
    "ConfiguracionFacturacion",
    "ConfiguracionInventario",
    "ConfiguracionPOS",
    "ConfiguracionNotificaciones",
    "ConfiguracionSeguridad",
    "ConfiguracionIntegraciones",
    "ConfiguracionAutomatizaciones",
]

