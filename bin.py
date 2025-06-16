edid_hex0 = ("0fFFFFFFFFFFFF0010AC79424C475A420F220104B53C22783ADF15AD5044AD250F5054A54B00D100D1C0B300A94081808100714FE1C04DD000A0F0703E803020350055502100001A000000FF0032335A534A30340A2020202020000000FC0044454C4C20553237323351450A000000FD0017560F8C36010A202020202020012A")

edid_hex3 = ("00FFFFFFFFFFFF0010AC79424C475A420F220104B53C22783ADF15AD5044AD250F5054A54B00D100D1C0B300A94081808100714FE1C04DD000A0F0703E803020350055502100001A000000FF0032335A534A30340A2020202020000000FC0044454C4C20553237323351450A000000FD0017560F8C36010A202020202020012A")

edid_hex5 = (
    "00ffffffffffff00ffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "023a801871382d40582c4500fd1e1100"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ffffffffffffffffffffffffffffffff"
    "ff"
)

edid_invalid_manu = (
    "00ffffffffffff000000000000000000"
    "0c16010380200978eaee95a3544c9926"
    "0f5054a54b00714f8180818f9500a9c0"
    "b30001010101023a801871382d40582c"
    "4500fd1e1100001e000000ff004e3132"
    "333435363738390a20000000fc004445"
    "4c4c2055323431344d0a20000000fd00"
    "384c1e5311000a202020202020202077"
)

edid_hex6 = (
    "00ffffffffffff0010ac8340533333310c16010380200978"
    "eaee95a3544c99260f5054a54b00714f8180818f9500a9c0"
    "000000ff004e3132333435363738390a20000000fc004445"
    "4c4c2055323431344d0a20000000fd00384c1e5311000a20"
    "20202020202000000000000000000000000000000000f1"
)

with open("bad_header.bin", "wb") as f:
    f.write(bytes.fromhex(edid_hex0))

with open("sample_edid.bin", "wb") as f:
    f.write(bytes.fromhex(edid_hex3))
    
with open("bad_long.bin", "wb") as f:
    f.write(bytes.fromhex(edid_hex5))
    
with open("bad_short.bin", "wb") as f:
    f.write(bytes.fromhex(edid_hex6))
    
with open("bad_manu.bin", "wb") as f:
    f.write(bytes.fromhex(edid_invalid_manu))