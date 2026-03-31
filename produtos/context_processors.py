import os


def site_contatos(request):
    whatsapp_numero = os.getenv("WHATSAPP_NUMBER", "(31)982027313").strip()
    instagram_handle = os.getenv("INSTAGRAM_HANDLE", "Dona_amora").strip().lstrip("@")
    instagram_url = os.getenv("INSTAGRAM_URL", f"https://www.instagram.com/dona_amora.mg?igsh=MXJ3YnlkZ2YzcDI2dw==").strip()

    return {
        "site_whatsapp_number": whatsapp_numero,
        "site_whatsapp_url": f"https://wa.me/{whatsapp_numero}",
        "site_instagram_handle": instagram_handle,
        "site_instagram_url": instagram_url,
    }
