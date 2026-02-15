"""Inventario module."""

from .models import Producto
from .routes import router

__all__ = ["Producto", "router"]
