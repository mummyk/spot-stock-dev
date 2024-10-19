import cv2
from pyzbar.pyzbar import decode
import numpy as np
import keyboard
import threading


class Barcode_scanner:

    def __init__(self):
        print("Scanner Active")

    def scan_barcode_with_camera():
        # Attempt to open the default camera (0)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Set camera resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Press 'q' to quit.")

        while True:
            # Read frame from the camera
            ret, frame = cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            # Convert frame to grayscale for better barcode detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:
                # Decode barcodes in the grayscale frame
                barcodes = decode(gray)
            except Exception as e:
                print(f"Error decoding frame: {e}")
                continue

            # Process each detected barcode
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type

                # Draw the polygon around the barcode
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                # Display barcode data and type
                cv2.putText(frame, f'{barcode_data} ({barcode_type})',
                            (barcode.rect.left, barcode.rect.top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

               #  print(f"Scanned Barcode: {
               #        barcode_data} | Type: {barcode_type}")

                return [barcode_data, barcode_type]

            # Show the camera feed with barcode overlays
            cv2.imshow('Barcode Scanner (Camera)', frame)

            # Check for 'q' key press to exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Release the camera and close windows
        cap.release()
        cv2.destroyAllWindows()

    def scan_barcode_with_scanner():
        print("Ready to scan barcodes with a barcode scanner...")
        barcode = ""
        while True:
            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'enter':
                    print(f"Scanned Barcode (Scanner): {barcode}")
                    barcode = ""
                else:
                    barcode += event.name
