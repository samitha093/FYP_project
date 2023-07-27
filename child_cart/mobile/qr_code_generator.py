import qrcode

def generate_qr_code(data, output_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

""" if __name__ == "__main__":
    # Data to encode in the QR code
    server_ip = socket.gethostbyname(socket.gethostname())
    PORT = generate_random_port(9000,15000)
    data = f"ws://{server_ip}:{PORT}"

    # Output file path
    output_file = "qrcodeNew.png"

    generate_qr_code(data, output_file)
    print(f"QR code generated and saved to '{output_file}'.") """
