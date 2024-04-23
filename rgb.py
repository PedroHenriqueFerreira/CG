def hex_to_RGB(hex: str):
    return tuple(int(hex.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
