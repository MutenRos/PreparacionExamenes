"""Módulo de automatizaciones internas del ERP."""

from .models import (
    Automatizacion,
    Accion,
    RegistroAutomatizacion,
    CondicionAutomatizacion,
)

__all__ = [
    "Automatizacion",
    "Accion",
    "RegistroAutomatizacion",
    "CondicionAutomatizacion",
]
