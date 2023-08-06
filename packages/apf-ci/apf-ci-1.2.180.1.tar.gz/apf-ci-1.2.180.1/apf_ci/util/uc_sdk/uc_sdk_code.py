# coding=ascii


def get_ascii_code():
    hex_str = "a3aca1a3"
    bt = []

    for i in range(0, len(hex_str), 2):
        b = hex_str[i:i + 2]
        bt.append(chr(int(b, 16)))
    btmd5 = ''.join(bt)
    return btmd5