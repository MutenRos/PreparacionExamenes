# OmniERP - Información de Base de Datos

## Ubicación de Datos Persistentes

Las bases de datos se almacenan en **rutas absolutas** para evitar pérdida de datos:

### Base de Datos Master
- **Ruta**: `/home/dario/src/data/erp.db`
- **Propósito**: Gestión de organizaciones y usuarios del sistema
- **Persistencia**: ✅ NO se borra al reiniciar el servidor

### Bases de Datos por Tenant (Organización)
- **Ruta**: `/home/dario/src/data/org_dbs/org_{ID}.db`
- **Propósito**: Datos de cada organización (productos, ventas, compras, etc.)
- **Persistencia**: ✅ NO se borran al reiniciar el servidor

## Configuración

La configuración se encuentra en: `src/dario_app/database/__init__.py`

```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MASTER_DB_PATH = DATA_DIR / "erp.db"
ORG_DB_DIR = DATA_DIR / "org_dbs"
```

## Respaldo de Datos

Para respaldar todas las bases de datos:

```bash
# Respaldar todo
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/dario/src/data/

# Restaurar
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz -C /
```

## Notas Importantes

- ✅ Las DBs persisten entre reinicios del servidor
- ✅ Las rutas son absolutas, no relativas
- ✅ El directorio `data/` está en `.gitignore`
- ⚠️ Hacer backups regulares antes de actualizaciones importantes
