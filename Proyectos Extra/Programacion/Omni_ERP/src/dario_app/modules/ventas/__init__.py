"""Ventas module."""

from .models import Venta, VentaDetalle
from .routes import router

__all__ = ["Venta", "VentaDetalle", "router"]
