def is_valid_email(value: str) -> bool:
    return "@" in value and "." in value.split("@")[-1]

def is_adult(age: int) -> bool:
    return age >= 18

def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in value if ch.isdigit())
    if digits.startswith("8"):
        digits = "7" + digits[1:]
    return "+" + digits