from datetime import date


class Today:
    months = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    today = date.today()

    def get_date_str() -> str:
        return f"{Today.today.day} de {Today.get_month_str()} de {Today.today.year}"

    def get_date_iso() -> str:
        return Today.today.strftime("%Y-%m-%d")

    def get_month_str() -> str:
        return Today.months[Today.today.month - 1]
