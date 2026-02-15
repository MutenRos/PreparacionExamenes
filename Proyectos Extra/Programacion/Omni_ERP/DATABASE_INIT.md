# Bombas Omni ERP - Database Initialization

This document explains how to initialize the OmniERP database with realistic Bombas Omni demo data.

## Overview

The OmniERP system uses a multi-tenant SQLite database architecture:
- **Master Database** (`data/erp.db`): Organizations, users, roles, and global configuration
- **Tenant Databases** (`data/org_dbs/org_*.db`): Organization-specific data (products, customers, suppliers, etc.)

## Quick Start

### 1. Start the OmniERP Server

```bash
sudo systemctl start omnierp
# or
sudo systemctl restart omnierp
```

### 2. Initialize the Database

Run the initialization script to create tables and seed demo data:

```bash
cd /home/dario
python3 init_db_simple.py
```

This script will:
- ✓ Create all necessary tables in the tenant database
- ✓ Insert 7 realistic suppliers (Bombas Omni partners)
- ✓ Insert 8 customer companies (irrigation, aquaculture, mining, etc.)
- ✓ Insert 17 products (6 pump types, 4 motors, 5 components, 2 services)

### 3. Verify the Data

Access the demo API endpoints to verify the data was loaded:

```bash
# Get all products
curl http://localhost:8001/api/demo/productos | python3 -m json.tool

# Get all suppliers
curl http://localhost:8001/api/demo/proveedores | python3 -m json.tool

# Get all customers
curl http://localhost:8001/api/demo/clientes | python3 -m json.tool

# Get statistics
curl http://localhost:8001/api/demo/stats | python3 -m json.tool
```

## Data Persistence

All data is **automatically persisted** to SQLite database files on disk:

```
/home/dario/src/dario_app/data/
├── erp.db                    # Master database (~315 KB)
└── org_dbs/
    └── org_1.db              # Tenant 1 database (~512 KB)
```

These files are **persistent** across server restarts.

## Bombas Omni Product Catalog

### Pumps (6 types)
- **BC-100**: Centrifugal pump, 1 HP, 50 L/min
- **BS-200**: Submersible pump, 2 HP, 50m depth
- **BA-150**: Axial pump, 1.5 HP, 120 L/min
- **BD-300**: Diaphragm pump, 3 HP, 200 L/min variable
- **BP-180**: Peripheral pump, 2.5 HP, 100 L/min
- **BI-500**: Industrial pump, 5 HP, 300 L/min

### Components
- Electric motors (1 HP to 5 HP, IE3 efficiency)
- Stainless steel chassis
- PVC hoses and fittings
- Impellers
- Mechanical seals
- Bearings

### Services
- Annual maintenance kits
- Professional installation service

## Demo Suppliers

All suppliers are realistic Mexican industrial companies:

1. Motores Industriales SA - Motors supplier
2. Aceros y Metales Import - Steel and metals
3. Plásticos y Polímeros Ltd - Plastic components
4. Electrónica Profesional - Electronic components
5. Componentes Hidráulicos - Hydraulic parts
6. Pintura Industrial México - Industrial paint
7. Empaques y Logística - Packaging and logistics

## Demo Customers

All customers are realistic companies using pump systems:

1. Hidroservicios del Norte - Water services
2. Sistemas de Riego Agrícola - Agricultural irrigation
3. Acuacultura México - Aquaculture operations
4. Constructoras y Proyectos - Construction
5. Minería y Extracción - Mining operations
6. Industria Textil del Bajío - Textile manufacturing
7. Generación de Energía Verde - Green energy generation
8. Distribuidora Integral Técnica - Technical distributor

## API Endpoints

Public endpoints (no authentication required):

```
GET  /api/demo/productos      # List all products
GET  /api/demo/proveedores    # List all suppliers
GET  /api/demo/clientes       # List all customers
GET  /api/demo/stats          # Get inventory statistics
```

## Database Schema

Key tables in the tenant database:

- `productos` - Product inventory
- `proveedores` - Suppliers
- `clientes` - Customers
- `ventas` - Sales orders
- `compras` - Purchase orders
- `usuarios` - Users
- `roles` - User roles
- `permisos` - Permissions
- `automatizaciones` - Automation rules
- And 20+ other tables for complete ERP functionality

## Manual Data Modifications

If you need to modify data manually:

```bash
# Connect to the tenant database
sqlite3 /home/dario/src/dario_app/data/org_dbs/org_1.db

# Example: View all products
SELECT id, codigo, nombre, stock_actual, precio_venta FROM productos;

# Example: Update a product price
UPDATE productos SET precio_venta = 1200 WHERE codigo = 'BC-100-001';
```

## Troubleshooting

### Database file is empty after creation
- Ensure you ran `init_db_simple.py` AFTER starting the server
- Check permissions on `/home/dario/src/dario_app/data/org_dbs/`

### API returns "Database not initialized yet"
- Run `init_db_simple.py` to initialize the tenant database
- Verify the org_1.db file exists and has size > 100 KB

### Changes don't persist after restart
- The database configuration now includes persistence options:
  - `check_same_thread=False`
  - `timeout=30` (30 second connection timeout)
  - `pool_pre_ping=True` (verify connections)
  - `pool_recycle=3600` (recycle connections hourly)

## Architecture Notes

The database system implements:
- **Multi-tenant isolation**: Each organization has its own SQLite database
- **Automatic schema creation**: Tables created automatically on first tenant initialization
- **Data persistence**: SQLAlchemy with connection pooling and recycle settings
- **Async support**: Uses `sqlalchemy.ext.asyncio` for async database operations

Organizations can have separate:
- Products and inventory
- Customers and suppliers
- Users and permissions
- Configuration and settings
- Sales and purchase history
- Automation rules

While sharing:
- Organizations registry (master DB)
- User authentication (master DB)
- Global settings (master DB)
