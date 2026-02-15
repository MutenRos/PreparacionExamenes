#!/bin/bash
set -euo pipefail

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

BASE_URL="http://localhost:5000"
curl -s "$BASE_URL/health" >/dev/null || BASE_URL="http://localhost:8001"

echo -e "${YELLOW}[E2E] Using BASE_URL=${BASE_URL}${NC}"

# Login to obtain access token cookie
COOKIE_FILE="/tmp/e2e_cookies.txt"
rm -f "$COOKIE_FILE" 2>/dev/null || true
LOGIN_CODE=$(curl -s -c "$COOKIE_FILE" -b "$COOKIE_FILE" -w "%{http_code}" -o /dev/null \
  -X POST "$BASE_URL/app/login" \
  -d "email=admin@omnisolutions.com&password=admin123" \
  -H "Content-Type: application/x-www-form-urlencoded")
if [ "$LOGIN_CODE" != "303" ] && [ "$LOGIN_CODE" != "200" ]; then
  echo -e "${RED}❌ Login failed (HTTP $LOGIN_CODE)${NC}"; exit 1
fi

# 0) Ensure fiscal data is complete
curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" -H 'Content-Type: application/json' -X PUT \
  -d '{
    "razon_social": "Omni Solutions S.A.",
    "ruc_numero": "B12345678",
    "ruc_digito": "0",
    "direccion": "Calle Empresa 1",
    "ciudad": "Madrid",
    "provincia": "Madrid",
    "codigo_postal": "28001",
    "pais": "España",
    "regimen_tributario": "General",
    "telefono": "+34 600 000 000",
    "website": "https://omni.local"
  }' "$BASE_URL/api/organization/fiscal-data" >/dev/null || true

# 1) Ensure a template exists (create if none)
count=$(curl -s -b "$COOKIE_FILE" "$BASE_URL/api/templates/" | jq 'length' 2>/dev/null || echo 0)
if [ "$count" -eq 0 ]; then
  echo -e "${YELLOW}No templates found. Creating default factura template...${NC}"
  curl -s -b "$COOKIE_FILE" -H 'Content-Type: application/json' -d '{
    "tipo_documento": "factura",
    "logo_url": null,
    "color_primario": "#2563eb",
    "color_secundario": "#64748b",
    "fuente": "Helvetica",
    "mostrar_logo": true,
    "mostrar_qr": true,
    "mostrar_codigo_barras": false,
    "mostrar_firma_vendedor": true,
    "mostrar_firma_cliente": true,
    "mostrar_sello": false,
    "condiciones_pago": "Transferencia 30 días",
    "notas_pie": "Gracias por su confianza",
    "terminos_condiciones": "Condiciones estándar",
    "prefijo": "F-"
  }' "$BASE_URL/api/templates/" -b "$COOKIE_FILE" >/dev/null || true
fi

TEMPLATE_ID=$(curl -s -b "$COOKIE_FILE" "$BASE_URL/api/templates/" | jq '.[0].id' 2>/dev/null)
if [ -z "$TEMPLATE_ID" ] || [ "$TEMPLATE_ID" = "null" ]; then
  echo -e "${RED}❌ Unable to read/create a template${NC}"; exit 1
fi

# 2) Create a manual document
DOC_JSON=$(cat <<JSON
{
  "tipo_documento": "factura",
  "numero_documento": "E2E-$(date +%s)",
  "cliente_nombre": "Cliente E2E",
  "cliente_email": "e2e@example.com",
  "cliente_telefono": "600000000",
  "cliente_direccion": "Calle de Prueba 123, Madrid",
  "items": [
    {"cantidad": 2, "descripcion": "Producto Test", "precio_unitario": 49.9},
    {"cantidad": 1, "descripcion": "Servicio Test", "precio_unitario": 99.0}
  ],
  "subtotal": 198.8,
  "impuesto": 41.75,
  "total": 240.55,
  "template_id": ${TEMPLATE_ID},
  "notas": "Pedido E2E"
}
JSON
)

DOC_RESP=$(curl -s -b "$COOKIE_FILE" -H 'Content-Type: application/json' -d "$DOC_JSON" "$BASE_URL/api/templates/manuales/")
DOC_ID=$(echo "$DOC_RESP" | jq '.id' 2>/dev/null)
DOC_NUM=$(echo "$DOC_RESP" | jq -r '.numero_documento' 2>/dev/null)
if [ -z "$DOC_ID" ] || [ "$DOC_ID" = "null" ]; then
  echo -e "${RED}❌ Failed to create manual document${NC}"; echo "$DOC_RESP"; exit 1
fi
echo -e "${GREEN}✅ Created manual doc id=${DOC_ID}${NC}"

# 3) Generate and save PDF
PDF_CODE=$(curl -s -o /tmp/e2e_doc.pdf -w "%{http_code}" -b "$COOKIE_FILE" -X POST "$BASE_URL/api/templates/manuales/${DOC_ID}/generar-pdf")
if [ "$PDF_CODE" != "200" ]; then
  echo -e "${RED}❌ PDF generation failed (HTTP $PDF_CODE)${NC}"; exit 1
fi
[ -s /tmp/e2e_doc.pdf ] || { echo -e "${RED}❌ PDF file empty${NC}"; exit 1; }
echo -e "${GREEN}✅ PDF generated and streamed${NC}"

# 4) Verify enterprise health and filesystem storage
EH=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" "$BASE_URL/api/enterprise/health")
PDF_FILE="/home/dario/src/data/docs/org_1/documentos_manuales/factura_${DOC_NUM}.pdf"
if [ "$EH" = "200" ] && [ -f "$PDF_FILE" ]; then
  echo -e "${GREEN}✅ Enterprise health OK and PDF file exists at ${PDF_FILE}${NC}"
else
  echo -e "${RED}❌ Enterprise/PDF verification failed (health=$EH, file=$([ -f "$PDF_FILE" ] && echo yes || echo no))${NC}"
  exit 1
fi

echo -e "${GREEN}🎉 E2E document flow completed${NC}"
