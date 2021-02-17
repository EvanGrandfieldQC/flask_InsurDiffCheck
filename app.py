import os
import time
from flask import (
    Flask,
    make_response,
    render_template,
    flash,
    redirect,
    request,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/Users/evangrandfield/flask_InsurDiffCheck/uploads/"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def select_upload_file():
    return render_template("upload.html")


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        if f.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if f and allowed_file(f.filename):
            # filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, "file1.pdf"))
            return render_template("second_upload.html")
    #return render_template("second_upload.html")

@app.route("/after_uploader", methods=["GET", "POST"])
def second_upload_file():
    if request.method == "POST":
        f = request.files["file"]
        if f.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if f and allowed_file(f.filename):
            # filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, "file2.pdf"))
            time.sleep(2)
    os.system("mv ~/flask_InsurDiffCheck/uploads/file1.pdf ~/flask_InsurDiffCheck/file1.pdf")
    os.system("mv ~/flask_InsurDiffCheck/uploads/file2.pdf ~/flask_InsurDiffCheck/file2.pdf")
    os.system("rm static/file1_processed.txt")
    os.system("rm statc/file2_processed.txt")
    os.system("rm file1.txt")
    os.system("rm file2.txt") 
    os.system("python text_ripper.py file1.pdf")
    os.system("python text_ripper.py file2.pdf") 
    os.system("rm static/file1_processed01.html")
    os.system("rm static/file2_processed01.html")
    os.system("rm static/file1_processed.html")
    os.system("rm static/file2_processed.html")
    os.system("python unique_identifier.py") 
    return render_template("comparator.html")

if __name__ == "__main__":
    app.run(debug=True)
