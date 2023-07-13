from flask import Flask, render_template, request,flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
from flask import *

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'webp',  'jpg', 'jpeg'}
SAVE_FOLDER="saved"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SAVED_FOLDER"] = SAVE_FOLDER
app.secret_key ='super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    
    img = cv2.imread(f"upload/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename =f"saved/{filename}"
            cv2.imwrite(newFilename,imgProcessed)
            return newFilename
        case "cpng":
            newFilename = f"saved/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename,img)
            return newFilename
        case "cwebp":
            newFilename = f"saved/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename,img)
            return newFilename
        case "cjpg":
            newFilename = f"saved/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename,img)
            return newFilename




@app.route("/")
def home():
    image_paths =['/static/src/img2.jpg','/static/src/img3.jpg','/static/src/img5.jpg']
    return render_template("Home.html",images=image_paths)

@app.route("/about.html")
def about():
    image_path =['/static/src/img1.jpg']
    return render_template("about.html",image=image_path)

@app.route("/operation.html")
def operation():
    return render_template("operation.html")

@app.route("/projects.html")
def projects():
    return render_template("projects.html")

@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "File is not selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new =processImage(filename=filename,operation=operation)
            new1 =new.split("/")[1]
            return send_from_directory("saved",new1)
            
        
    return render_template('operation.html')

app.run(debug=True, port =5001)