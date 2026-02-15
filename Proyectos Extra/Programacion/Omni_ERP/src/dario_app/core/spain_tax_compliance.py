"""Spanish tax compliance utilities - NIF validation, IVA calculation, legal requirements."""

import re
from typing import Tuple


class SpainTaxCompliance:
    """Utilities for Spanish tax and legal compliance."""

    # NIF validation tables
    NIF_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
    CIF_LETTERS = "JABCDEFGHJUV"

    @staticmethod
    def validate_nif(nif: str) -> Tuple[bool, str]:
        """
        Validate Spanish NIF/NIE/CIF format.

        Returns:
            (is_valid, type) where type is 'NIF', 'NIE', 'CIF', or 'INVALID'
        """
        if not nif:
            return False, "INVALID"

        nif = nif.upper().strip()

        # NIF format: 8 digits + 1 letter
        nif_pattern = r"^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$"
        nif_match = re.match(nif_pattern, nif)
        if nif_match:
            number = int(nif_match.group(1))
            letter = nif_match.group(2)
            expected_letter = SpainTaxCompliance.NIF_LETTERS[number % 23]
            if letter == expected_letter:
                return True, "NIF"

        # NIE format: X/Y/Z + 7 digits + 1 letter (for foreigners)
        nie_pattern = r"^([XYZ])([0-9]{7})([TRWAGMYFPDXBNJZSQVHLCKE])$"
        nie_match = re.match(nie_pattern, nif)
        if nie_match:
            prefix = nie_match.group(1)
            number_str = nie_match.group(2)
            letter = nie_match.group(3)

            # Convert X/Y/Z to 0/1/2 for validation
            prefix_map = {"X": "0", "Y": "1", "Z": "2"}
            number = int(prefix_map[prefix] + number_str)
            expected_letter = SpainTaxCompliance.NIF_LETTERS[number % 23]
            if letter == expected_letter:
                return True, "NIE"

        # CIF format: 1 letter + 7/8 digits + control digit/letter
        cif_pattern = r"^([ABCDEFGHJNPQRSUVW])([0-9]{7,8})([0-9A-J])$"
        cif_match = re.match(cif_pattern, nif)
        if cif_match:
            # Simplified CIF validation (full validation is complex)
            return True, "CIF"

        return False, "INVALID"

    @staticmethod
    def calculate_vat(base: float, vat_rate: int = 21) -> dict:
        """
        Calculate VAT for Spain.

        Args:
            base: Base amount (base imponible)
            vat_rate: VAT rate (21% default, can be 10% or 4% for some goods/services)

        Returns:
            dict with base, vat, and total amounts
        """
        vat_amount = round(base * vat_rate / 100, 2)
        total = round(base + vat_amount, 2)

        return {
            "base_imponible": round(base, 2),
            "iva": vat_amount,
            "porcentaje_iva": vat_rate,
            "total": total,
        }

    @staticmethod
    def calculate_irpf(base: float, irpf_rate: int = 15, applies: bool = False) -> dict:
        """
        Calculate IRPF (income tax withholding) for Spain.

        Args:
            base: Base amount
            irpf_rate: IRPF rate (typically 15% for freelancers)
            applies: Whether IRPF applies for this sale

        Returns:
            dict with base, irpf, and net amounts
        """
        if not applies or irpf_rate <= 0:
            return {"base": round(base, 2), "irpf": 0, "porcentaje_irpf": 0, "neto": round(base, 2)}

        irpf_amount = round(base * irpf_rate / 100, 2)
        neto = round(base - irpf_amount, 2)

        return {
            "base": round(base, 2),
            "irpf": irpf_amount,
            "porcentaje_irpf": irpf_rate,
            "neto": neto,
        }

    @staticmethod
    def get_vat_rates() -> dict:
        """Get valid VAT rates for Spain."""
        return {
            "standard": 21,  # Estándar: 21%
            "reduced": 10,  # Reducido: 10%
            "super_reduced": 4,  # Superreducido: 4%
            "zero": 0,  # Exento de IVA: 0%
        }

    @staticmethod
    def get_spanish_provinces() -> list:
        """Get list of Spanish provinces/autonomous communities (CCAA)."""
        return [
            "Álava",
            "Albacete",
            "Alicante",
            "Almería",
            "Asturias",
            "Ávila",
            "Badajoz",
            "Baleares",
            "Barcelona",
            "Burgos",
            "Cáceres",
            "Cádiz",
            "Cantabria",
            "Castellón",
            "Castilla-La Mancha",
            "Castilla y León",
            "Cataluña",
            "Ceuta",
            "Ciudad Real",
            "Córdoba",
            "Cuenca",
            "Extremadura",
            "Girona",
            "Granada",
            "Guadalajara",
            "Guipúzcoa",
            "Huelva",
            "Huesca",
            "Jaén",
            "La Rioja",
            "Las Palmas",
            "León",
            "Lleida",
            "Lugo",
            "Madrid",
            "Málaga",
            "Melilla",
            "Murcia",
            "Navarra",
            "Ourense",
            "Palencia",
            "Palma de Mallorca",
            "Pamplona",
            "Pontevedra",
            "Salamanca",
            "Segovia",
            "Sevilla",
            "Soria",
            "Tarragona",
            "Tenerife",
            "Teruel",
            "Toledo",
            "Valencia",
            "Valladolid",
            "Vizcaya",
            "Zamora",
            "Zaragoza",
        ]

    @staticmethod
    def get_invoice_requirements() -> dict:
        """Get Spanish invoice legal requirements."""
        return {
            "required_fields": [
                "invoice_number",  # Número de factura (correlativo)
                "issue_date",  # Fecha de emisión
                "supplier_name",  # Nombre/razón social proveedor
                "supplier_nif",  # NIF/CIF proveedor
                "supplier_address",  # Dirección proveedor
                "customer_name",  # Nombre cliente
                "customer_nif",  # NIF/NIE cliente (si disponible)
                "customer_address",  # Dirección cliente
                "item_description",  # Descripción de productos/servicios
                "unit_price",  # Precio unitario
                "quantity",  # Cantidad
                "base_imponible",  # Base imponible
                "vat_rate",  # Porcentaje IVA
                "vat_amount",  # Cantidad IVA
                "total_amount",  # Importe total
                "payment_method",  # Forma de pago
            ],
            "data_retention": 4,  # Años
            "invoicing_requirement": "All transactions over €3,005.06 must be invoiced",
            "vat_number_requirement": "Must display NIF/CIF for companies",
            "digital_signature": "Can use digital signature (opcional but recommended)",
            "archival": "Must be archived for minimum 4 years",
        }
