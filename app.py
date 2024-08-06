import qrcode

# Read the file line by line
with open("sample.txt", "r") as file:
    lines = file.readlines()

# Create a QR code for each line
for i, line in enumerate(lines):
    data = line.strip()  # Remove leading/trailing whitespaces
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=300 // 29,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # get the first chassis_no
    first = data.split(',')[0]

    img = qr.make_image()
    index = f"{(i+1):03d}"
    img.save(f"{index}_{first}.png")

# Print a success message
print(f"QR codes generated for {len(lines)} lines and saved as qrcode_0.png, qrcode_1.png, etc.")
