def validate_contact(name, phone):
    is_valid_name = isinstance(name, str) and len(name.strip()) > 0
    is_valid_phone = (
        len(phone) == 14 and
        phone.startswith("+234") and
        phone[4:].isdigit()
    )

    return is_valid_phone and is_valid_name


