import cv2
import ast

def QRReader():
    cam = cv2.VideoCapture(0)
    cam.set(5, 640)
    cam.set(6, 480)
    camera = True
    while camera:
        success, frame = cam.read()

        # Decode the QR code
        qr = cv2.QRCodeDetector()
        decoded_data, _, _ = qr.detectAndDecode(frame)

        if decoded_data:
            try:
                # Extract the desired value
                value_list = ast.literal_eval(decoded_data)
                print(value_list)
                return value_list
            except ValueError:
                print("Error: Unable to decode QR code data")
                continue
        else:
            print("Error: QR code not detected")
            continue
