from random import randint

def hexToRGB(hex: str):
    hex = hex.lstrip('#')
    
    return tuple(int(hex[i:i+2], 16) / 255 for i in (0, 2, 4))

def randomRGB():
    return hexToRGB(f'#{randint(0, 0xFFFFFF):06x}')