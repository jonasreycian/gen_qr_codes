import qrcode
from reportlab.lib.pagesizes import A1
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw

def generate_qr_codes(input_file):
    # Read the file line by line
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Create a QR code for each line and save as image
    qr_images = []
    for i, line in enumerate(lines):
        data = line.strip()  # Remove leading/trailing whitespaces
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=216 // 29,  # 216 pixels for 60% of 1.2 inch at 300 DPI
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # get the first chassis_no
        first = data.split(',')[0]

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        index = f"{(i+1):03d}"
        img_path = f"{index}_{first}.png"


        # Create a black background image with the same size as the mask
        background = Image.new("RGB", (360, 360), "black")

        # Paste the QR code image onto the black background using the mask
        background.paste(img, (72, 72), mask=mask)  # Center the QR code in the circle
        background.save(img_path)
        qr_images.append(img_path)

    return qr_images

def create_pdf_with_qrcodes(pdf_filename, qr_images):
    """
    Create a PDF with size A1 and place QR codes in a grid layout.

    :param pdf_filename: The filename of the PDF to be created.
    :param qr_images: A list of file paths to the QR code images.
    """
    # Create a PDF with size A1
    c = canvas.Canvas(pdf_filename, pagesize=A1)
    width, height = A1

    # Define the grid layout
    cols = 5
    rows = 6
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

def main():
    input_file = "Results.csv"
    qr_images = generate_qr_codes(input_file)

    # Group the qr_images by 30 and create a PDF for each group
    # group_size = 30
    # for i in range(0, len(qr_images), group_size):
    #     group = qr_images[i:i + group_size]
    #     pdf_filename = f"qrcodes_{i // group_size + 1}.pdf"
    #     create_pdf_with_qrcodes(pdf_filename, group)

    # Print a success message
    print(f"QR codes generated for {len(qr_images)} lines and saved in multiple PDFs.")

if __name__ == "__main__":
    main()