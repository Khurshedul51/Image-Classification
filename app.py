from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

# Initialize the flask application
app = Flask(__name__)

# path of model
MODEL_PATH = ''

# Load the model
model = load_model(MODEL_PATH)

# ensuring the upload directory exists
UPLOAD_DIR = 'static/uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.config['UPLOAD_DIR'] = UPLOAD_DIR

# function to make predictions
def predict_image_type(img_filename):
    img_width = 180
    img_height = 180
    image = img_filename
    image = tf.keras.utils.load_img(image, target_size=(img_height,img_width))
    img_arr = tf.keras.utils.array_to_img(image)
    img_bat = tf.expand_dims(img_arr,0)
    predict= model.predict(img_bat)
    return predict

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    USERNAME = 'ya hoille goribi'
    PASSWORD = 'admin'
    username = request.form['username']
    password = request.form['password']
    # Add your authentication logic here
    # For demonstration purposes, we assume any username and password are valid
    if username==USERNAME and password==PASSWORD:
        return redirect(url_for('input'))
    # else:
    #     return jsonify({
    #         "error-message": 'oops! password or username is wrong!'
    #     })
    return redirect(url_for('login'))

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        # Save the file to ./uploads
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_DIR'], filename)
        file.save(filepath)

        # call the predict function
        predict = predict_image_type(filename)
        # For demonstration, we just return the filename

        return f"Image uploaded: {file.filename}"
    if not file:
        return "No file selected", 400

if __name__ == '__main__':
    app.run(debug=True)
