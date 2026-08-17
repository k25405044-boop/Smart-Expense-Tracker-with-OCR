import easyocr
import re
import numpy as np
from PIL import Image

# OCR Reader
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):

    # Open image using Pillow
    image = Image.open(image_path).convert("RGB")

    # Convert PIL image to NumPy array
    image_array = np.array(image)

    # Send image directly to EasyOCR
    result = reader.readtext(image_array, detail=0)

    text = "\n".join(result)

    return text


def extract_amount(text):

    amounts = re.findall(
        r'(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d{1,2})?)',
        text,
        re.IGNORECASE
    )

    if not amounts:
        return 0

    numbers = []

    for value in amounts:
        try:
            numbers.append(float(value))
        except ValueError:
            pass

    return max(numbers) if numbers else 0


def extract_date(text):

    pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_shop(text):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if len(line) > 2:
            return line

    return "Unknown Shop"


def detect_category(text):

    text = text.lower()

    if any(word in text for word in [
        "food",
        "restaurant",
        "pizza",
        "burger",
        "hotel",
        "grocery",
        "milk",
        "bread"
    ]):
        return "Food"

    elif any(word in text for word in [
        "medicine",
        "medical",
        "pharmacy",
        "hospital"
    ]):
        return "Medical"

    elif any(word in text for word in [
        "bus",
        "taxi",
        "uber",
        "fuel",
        "petrol",
        "travel"
    ]):
        return "Travel"

    elif any(word in text for word in [
        "book",
        "college",
        "school",
        "education"
    ]):
        return "Education"

    elif any(word in text for word in [
        "shirt",
        "clothes",
        "mall",
        "shopping"
    ]):
        return "Shopping"

    return "Other"