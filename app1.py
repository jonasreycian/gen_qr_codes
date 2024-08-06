import qrcode
from reportlab.lib.pagesizes import A1
from reportlab.pdfgen import canvas
from PIL import Image

# Read the file line by line
with open("sample.txt", "r") as file:
    lines = file.readlines()

# Limit to 20 lines
# lines = lines[:20]

# Create a QR code for each line and save as image
qr_images = []
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
    img_path = f"{index}_{first}.png"
    img.save(img_path)
    qr_images.append(img_path)

# Create a PDF with size A1
pdf_path = "qrcodes.pdf"
c = canvas.Canvas(pdf_path, pagesize=A1)
width, height = A1

# Define the grid layout
cols = 4
rows = 5
qr_size = min(width // cols, height // rows)

# Draw the QR codes on the PDF
for i, img_path in enumerate(qr_images):
    col = i % cols
    row = i // cols
    x = col * qr_size
    y = height - (row + 1) * qr_size  # Invert y-axis for PDF coordinates

    # Draw the image
    c.drawImage(img_path, x, y, qr_size, qr_size)

# Save the PDF
c.save()

# Print a success message
print(f"QR codes generated for {len(lines)} lines and saved in {pdf_path}.")