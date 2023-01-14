from flask import Flask, render_template, request, redirect
from scipy.integrate import quad
import sympy
import os
import pytesseract
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    func = None
    if request.method == "POST":
        # Get the image file from the form
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Use OCR to extract the problem from the image
            problem = pytesseract.image_to_string(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            func = get_function(problem) # function to solve

            # Define the function to integrate
            f = sympy.sympify(func)

            # Use the quad function to solve the integral
            result, error = quad(f, a, b)

    return render_template("index.html", result=result, error=error, func=func)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_function(problem):
    # function that extract the function from the problem using regex
    # or any other method you prefer
    pass

if __name__ == "__main__":
    app.run(debug=False)
