import pytesseract
from PIL import Image


image = Image.open('uploads/image.jpg')

# Extract text using Tesseract OCR
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)