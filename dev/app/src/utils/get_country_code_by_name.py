import country_converter as coco # type: ignore

def get_country_code_by_name(country_name):
    """Convertit le nom du pays en code ISO3 et retourne une chaîne"""
    iso_code = coco.convert(names=country_name, to="ISO3")
    return iso_code if isinstance(iso_code, str) else iso_code[0] if isinstance(iso_code, list) and iso_code else None