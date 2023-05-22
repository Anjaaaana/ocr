import cv2
import numpy as np
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define the path to the input folder and the output folder
input_folder = r"C:\Users\Lenovo\Desktop\vacancy or tender\output"
output_folder = r"C:\Users\Lenovo\Desktop\vacancy or tender\result"

# Define keywords to search for
keywords = {
    "vacancy": ["vacancy","wanted"],
    "tender": ["tender", "tender notices", "invitation for bids", "notice of invitation for bids", "notice gor quatation","bids", "bid", "bidding", "invitations to bid", "bid notices"]
}

# Loop through all the image files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg"):
        # Read the image
        img = cv2.imread(os.path.join(input_folder, filename))
        img = cv2.resize(img, None, fx=0.5, fy=0.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        adaptive_threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11
        )

        # Convert image to text using Tesseract OCR
        text = pytesseract.image_to_string(adaptive_threshold)

        # Search for each keyword in the text
        found_keywords = []
        for keyword in keywords:
            for subkeyword in keywords[keyword]:
                if subkeyword.lower() in text.lower():
                    found_keywords.append(keyword)
                    break

        # Save the image to the corresponding folder
        if "vacancy" in found_keywords:
            output_folder_vacancy = os.path.join(output_folder, "vacancy")
            if not os.path.exists(output_folder_vacancy):
                os.makedirs(output_folder_vacancy)
            output_filename = f"vacancy_{filename}"
            cv2.imwrite(os.path.join(output_folder_vacancy, output_filename), img)
            print(f"Image saved as {output_filename} in the vacancy folder")
        elif "tender" in found_keywords:
            output_folder_tender = os.path.join(output_folder, "tender")
            if not os.path.exists(output_folder_tender):
                os.makedirs(output_folder_tender)
            output_filename = f"tender_{filename}"
            cv2.imwrite(os.path.join(output_folder_tender, output_filename), img)
            print(f"Image saved as {output_filename} in the tender folder")
        elif "bids" in found_keywords:
            output_folder_bids = os.path.join(output_folder, "bids")
            if not os.path.exists(output_folder_bids):
                os.makedirs(output_folder_bids)
            output_filename = f"bids_{filename}"
            cv2.imwrite(os.path.join(output_folder_bids, output_filename), img)
            print(f"Image saved as {output_filename} in the bids folder")
        else:
            print(f"No relevant keywords found in {filename}")
        
        cv2.waitKey(0)
