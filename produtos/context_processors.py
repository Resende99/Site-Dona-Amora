import os
import re


def _normalizar_whatsapp_numero(numero_bruto):
    numero_limpo = re.sub(r"\D", "", (numero_bruto or "").strip())

    if not numero_limpo:
        return "5531982027313"

    if not numero_limpo.startswith("55"):
        numero_limpo = f"55{numero_limpo}"

    return numero_limpo


def site_contatos(request):
    whatsapp_numero = os.getenv("WHATSAPP_NUMBER", "(31)982027313").strip()
    whatsapp_numero_link = _normalizar_whatsapp_numero(whatsapp_numero)
    instagram_handle = os.getenv("INSTAGRAM_HANDLE", "Dona_amora").strip().lstrip("@")
    instagram_url = os.getenv("INSTAGRAM_URL", f"https://www.instagram.com/dona_amora.mg?igsh=MXJ3YnlkZ2YzcDI2dw==").strip()

    return {
        "site_whatsapp_number": whatsapp_numero,
        "site_whatsapp_number_link": whatsapp_numero_link,
        "site_whatsapp_url": f"https://wa.me/{whatsapp_numero_link}",
        "site_instagram_handle": instagram_handle,
        "site_instagram_url": instagram_url,
    }
