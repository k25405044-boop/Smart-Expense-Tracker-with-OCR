from flask import Flask, render_template, request
import os

from ocr import (
    extract_text,
    extract_amount,
    extract_date,
    extract_shop,
    detect_category
)

from database import (
    create_table,
    add_expense,
    get_expenses,
    get_total
)

from ai import analyze_expense


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

create_table()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "receipt" not in request.files:
        return "No file selected"

    file = request.files["receipt"]

    if file.filename == "":
        return "Please select a file"

    # Allowed file types
    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf"
    }

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        return "Only JPG, JPEG, PNG and PDF files are allowed."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    try:

        # OCR
        text = extract_text(filepath)

        # Normal OCR extraction
        amount = extract_amount(text)
        date = extract_date(text)
        shop = extract_shop(text)
        category = detect_category(text)

        # Gemini AI analysis
        ai_result = analyze_expense(text)

        # Use AI values if available
        shop = ai_result.get("shop") or shop
        amount = ai_result.get("amount") or amount
        date = ai_result.get("date") or date
        category = ai_result.get("category") or category

        summary = ai_result.get(
            "summary",
            "Expense analyzed successfully."
        )

        # Save to database
        add_expense(
            shop,
            amount,
            date,
            category,
            text
        )

        return render_template(
            "dashboard.html",
            shop=shop,
            amount=amount,
            date=date,
            category=category,
            summary=summary,
            text=text
        )

    except Exception as e:

        print("ERROR:", e)

        return f"""
        <h2>❌ Error while processing receipt</h2>
        <p>{e}</p>
        <a href="/">Go Back</a>
        """


@app.route("/history")
def history():

    expenses = get_expenses()
    total = get_total()

    return render_template(
        "history.html",
        expenses=expenses,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True)