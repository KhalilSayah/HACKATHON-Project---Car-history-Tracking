from flask import Flask, request

app = Flask(__name__)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    niv = request.form['exampleInputNIV']
    

    # Do something with the form data

    return 'Form submitted successfully!'
