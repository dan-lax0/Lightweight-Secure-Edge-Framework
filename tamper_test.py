# simulate tampering
with open("encrypted_data.bin", "rb+") as f:
    data = bytearray(f.read())
    data[0] = (data[0] + 1) % 256
    f.seek(0)
    f.write(data)

print("⚠️ Data Tampered Successfully")