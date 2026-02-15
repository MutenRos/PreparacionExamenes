"""PDF generation service for invoices and shipping notes."""

from datetime import datetime
from io import BytesIO

import qrcode
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PDFGenerator:
    """Generate professional PDF documents for invoices and shipping notes."""

    def __init__(self, template, organization):
        """Initialize PDF generator with a document template and organization data."""
        self.template = template
        self.organization = organization
        self.styles = getSampleStyleSheet()
        self.setup_styles()

    def setup_styles(self):
        """Setup custom styles based on template configuration."""
        # Title style
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Normal"],
            fontSize=24,
            textColor=self._hex_to_rgb(self.template.color_primario),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )

        # Heading style
        self.heading_style = ParagraphStyle(
            "CustomHeading",
            parent=self.styles["Heading2"],
            fontSize=12,
            textColor=self._hex_to_rgb(self.template.color_primario),
            spaceAfter=12,
            fontName="Helvetica-Bold",
        )

        # Normal style
        self.normal_style = self.styles["Normal"]

    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def generate_invoice_pdf(self, venta_data, cliente_data):
        """Generate an invoice PDF."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)

        story = []

        # Header with logo and company info
        story.extend(self._create_header())
        story.append(Spacer(1, 0.2 * inch))

        # Document title
        if self.template.tipo_documento == "factura":
            title = f"FACTURA {self.template.prefijo or ''}{venta_data.get('numero', 'N/A')}"
        else:
            title = f"ALBARÁN {self.template.prefijo or ''}{venta_data.get('numero', 'N/A')}"

        story.append(Paragraph(title, self.title_style))
        story.append(Spacer(1, 0.3 * inch))

        # Company and client info
        story.extend(self._create_info_section(venta_data, cliente_data))
        story.append(Spacer(1, 0.3 * inch))

        # Items table
        story.extend(self._create_items_table(venta_data))
        story.append(Spacer(1, 0.3 * inch))

        # Totals
        story.extend(self._create_totals_section(venta_data))
        story.append(Spacer(1, 0.3 * inch))

        # Additional info
        story.extend(self._create_footer_section(venta_data))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _create_header(self):
        """Create header with company logo and name."""
        elements = []

        header_data = []

        # Logo (if available)
        if self.template.mostrar_logo and self.template.logo_url:
            try:
                img = RLImage(self.template.logo_url, width=1 * inch, height=1 * inch)
                header_data.append(img)
            except:
                pass

        # Company info
        company_info = f"""
        <b>{self.organization.razon_social or self.organization.nombre}</b><br/>
        NIF/CIF: {self.organization.nif_cif or 'N/A'}<br/>
        {self.organization.domicilio_fiscal or self.organization.direccion or ''}<br/>
        {self.organization.municipio or ''}, {self.organization.provincia or ''} {self.organization.codigo_postal or ''}<br/>
        {self.organization.pais or ''}<br/>
        """

        if self.organization.telefono:
            company_info += f"Tel: {self.organization.telefono}<br/>"
        if self.organization.email:
            company_info += f"Email: {self.organization.email}<br/>"
        if self.organization.website:
            company_info += f"Web: {self.organization.website}<br/>"

        company_para = Paragraph(company_info, self.normal_style)
        header_data.append(company_para)

        # QR code (if enabled)
        if self.template.mostrar_qr:
            qr_code = self._generate_qr_code()
            header_data.append(qr_code)

        table = Table([header_data], colWidths=[2 * inch, 3 * inch, 1.5 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        elements.append(table)

        return elements

    def _generate_qr_code(self):
        """Generate QR code image."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"https://example.com/verify/{self.template.id}")
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            qr_buffer = BytesIO()
            img.save(qr_buffer, format="PNG")
            qr_buffer.seek(0)

            return RLImage(qr_buffer, width=0.8 * inch, height=0.8 * inch)
        except:
            return Paragraph("QR Code", self.normal_style)

    def _create_info_section(self, venta_data, cliente_data):
        """Create company and client information section."""
        elements = []

        info_data = [
            ["INFORMACIÓN DEL DOCUMENTO", "INFORMACIÓN DEL CLIENTE"],
            [
                f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n"
                f"Hora: {datetime.now().strftime('%H:%M:%S')}",
                f"Nombre: {cliente_data.get('nombre', 'N/A')}\n"
                f"Documento: {cliente_data.get('documento', 'N/A')}\n"
                f"Email: {cliente_data.get('email', 'N/A')}\n"
                f"Teléfono: {cliente_data.get('telefono', 'N/A')}",
            ],
        ]

        table = Table(info_data, colWidths=[3.5 * inch, 3.5 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.template.color_primario)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )
        elements.append(table)
        return elements

    def _create_items_table(self, venta_data):
        """Create items table with columns."""
        elements = []

        items = venta_data.get("items", [])

        # Header row
        table_data = [["DESCRIPCIÓN", "CANTIDAD", "PRECIO UNIT.", "DESCUENTO", "SUBTOTAL"]]

        # Item rows
        for item in items:
            table_data.append(
                [
                    item.get("descripcion", "N/A"),
                    str(item.get("cantidad", 0)),
                    f"${item.get('precio_unitario', 0):.2f}",
                    f"${item.get('descuento', 0):.2f}",
                    f"${item.get('subtotal', 0):.2f}",
                ]
            )

        table = Table(
            table_data, colWidths=[2.5 * inch, 1 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch]
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.template.color_primario)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )
        elements.append(table)
        return elements

    def _create_totals_section(self, venta_data):
        """Create totals section."""
        elements = []

        subtotal = venta_data.get("subtotal", 0)
        descuento = venta_data.get("descuento", 0)
        impuesto = venta_data.get("impuesto", 0)
        total = venta_data.get("total", 0)

        totals_data = [
            ["SUBTOTAL:", f"${subtotal:.2f}"],
            ["DESCUENTO:", f"-${descuento:.2f}"],
            ["IVA/IMPUESTO (18%):", f"${impuesto:.2f}"],
            ["TOTAL:", f"${total:.2f}"],
        ]

        table = Table(totals_data, colWidths=[5 * inch, 2 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 2), 10),
                    ("FONTSIZE", (0, 3), (-1, 3), 14),
                    ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor(self.template.color_primario)),
                    ("TEXTCOLOR", (0, 3), (-1, 3), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ]
            )
        )
        elements.append(table)
        return elements

    def _create_footer_section(self, venta_data):
        """Create footer section with terms and signatures."""
        elements = []

        # Payment conditions
        if self.template.condiciones_pago:
            elements.append(Paragraph("<b>CONDICIONES DE PAGO:</b>", self.heading_style))
            elements.append(Paragraph(self.template.condiciones_pago, self.normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Terms and conditions
        if self.template.terminos_condiciones:
            elements.append(Paragraph("<b>TÉRMINOS Y CONDICIONES:</b>", self.heading_style))
            elements.append(Paragraph(self.template.terminos_condiciones, self.normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        # Signatures
        if self.template.mostrar_firma_vendedor or self.template.mostrar_firma_cliente:
            sig_data = []

            if self.template.mostrar_firma_vendedor:
                sig_data.append(["_________________\nFirma Vendedor", ""])

            if self.template.mostrar_firma_cliente:
                sig_data.append(["_________________\nFirma Cliente", ""])

            if sig_data:
                table = Table(sig_data, colWidths=[3.5 * inch, 3.5 * inch])
                elements.append(table)

        # Footer notes
        if self.template.notas_pie:
            elements.append(Spacer(1, 0.3 * inch))
            footer_para = Paragraph(
                f"<i>{self.template.notas_pie}</i>",
                ParagraphStyle("Footer", parent=self.normal_style, alignment=TA_CENTER, fontSize=9),
            )
            elements.append(footer_para)

        return elements
