def determine_status(status: bool):
    return "Enabled" if status is True else "Disabled"


def format_desc(value: str, status: bool):
    new_status = determine_status(status)
    value_map = {"mod": "Moderation", "eco": "Economy", "redirects": "Redirects"}
    desc = (
        "Select on the buttons to enable/disable the current module\n\n"
        f"**Current Selected Module**: `{value_map[value]}`\n"
        f"**Current Status**: `{new_status}`"
    )
    return desc


def format_conf_desc(value: str, status: bool):
    new_status = determine_status(status)
    desc = (
        "Select on the buttons to enable/disable the current module\n\n"
        f"**Current Selected Module**: `{value}`\n"
        f"**Current Status**: `{new_status}`"
    )
    return desc
