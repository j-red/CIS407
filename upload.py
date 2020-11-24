# --------------------- SETUP ---------------------

import flask, os, urllib.request, pathlib, logging, random, string, time, shutil
from flask import Flask, flash, request, redirect, render_template, session, send_file
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileMerger

ROOT = os.getcwd()
ID_SIZE = 16
UPLOAD_FOLDER = ROOT + '/uploads'
ALLOWED_EXTENSIONS = set(['pdf']) # only allow PDF files

app = Flask(__name__)
app.config.from_pyfile('config.py') # configure from config.py
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def new_session_ID(length=ID_SIZE):
	""" Returns a new session ID. Sets the current flask session ID to this as
	 	a side effect. """
	flask.session["SESSION_ID"] = ''.join(random.choice(string.ascii_letters) for i in range(length))
	return flask.session["SESSION_ID"]

def merge(pdfs, dir):
	MAX_LENGTH = 128 # max file name length
	WRITE_DIR = os.path.join(app.config["UPLOAD_FOLDER"], flask.session["SESSION_ID"])

	prev_wd = os.getcwd()
	os.chdir(dir)

	merger = PdfFileMerger(strict=False) # Enforcing strict=False allows us to avoid the 'xref not zero-indexed' error from scanned documents.

	for pdf in pdfs:
		try:
			merger.append(pdf)
		except:
			app.logger.warning(f"Error merging '{pdf}'. Operation cancelled.")
			os.chdir(prev_wd) # return to previous working directory
			return

	new_name = "_".join(pdfs).replace(".pdf", "")
	new_name = new_name[:MAX_LENGTH] + ".pdf"
	output_path = os.path.join(WRITE_DIR, new_name)

	try:
		merger.write(output_path)
	except:
		app.logger.debug("Error writing output file. Operation cancelled.")
		os.chdir(prev_wd) # return to previous working directory
		return

	app.logger.debug(f"Wrote merged PDF to {output_path}")

	merger.close()
	os.chdir(prev_wd) # return to previous working directory
	return output_path


def clear_old(mins=2, hrs=0, days=0):
	""" Whenever this function is called, delete all tmp upload directories
		older than two minutes. """
	now = time.time()
	for f in os.listdir(app.config['UPLOAD_FOLDER']):
		path = os.path.join(app.config['UPLOAD_FOLDER'], f)
		if os.stat(path).st_mtime < now - (days * 24 + hrs * 3600 + mins * 60):
			app.logger.debug(f"Deleting {path}")
			shutil.rmtree(path)
		else:
			app.logger.debug(f"{f} is too young to delete.")

# --------------------- END SETUP ---------------------

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	clear_old()
	new_session_ID()
	# flash(flask.session["SESSION_ID"])
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	flask.session["FILENAMES"] = [] # reset session var on each upload
	# create individual folder for current user
	my_folder = os.path.join(app.config["UPLOAD_FOLDER"], flask.session["SESSION_ID"])

	while os.path.exists(my_folder):
		# check if folder already exists; if so, assign new session ID and try again
		app.logger.warning("ERROR: Folder already existed")
		new_session_ID()
		my_folder = os.path.join(app.config["UPLOAD_FOLDER"], flask.session["SESSION_ID"])

	try:
		os.mkdir(my_folder)
	except:
		app.logger.warning("Error creating tmp user folder.")

	if not os.path.exists('my_folder'):
		app.logger.warning("Error: could not create temporary storage folder.")
		flash("Error creating tmp storage directory. Please try again.")
		return redirect('/')

	if request.method == 'POST':
		# check if the post request has the file part
		if 'uploads' not in request.files:
			app.logger.debug("No files found.")
			flash('No files part')
			return redirect(request.url)

		files = request.files.getlist('uploads')

		for file in files:
			if file.filename == '':
				flash('No file selected for uploading')
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				flask.session["FILENAMES"].append(filename) # append file name to list of files in current session
				# app.logger.debug(f"Saving file to {os.path.join(my_folder, filename)}")
				try:
					file.save(os.path.join(my_folder, filename))
					app.logger.debug(f"{filename} uploaded successfully.")
				except:
					app.logger.warning(f"Error saving file to {os.path.join(my_folder, filename)}")
			else:
				flash('Error: Only PDF files are permitted.')
				return redirect(request.url)

	# flash("Merging PDFs...")
	new_file = merge(flask.session["FILENAMES"], my_folder) # merge PDFs
	return send_file(new_file, as_attachment=True)
	# return redirect('/')


if app.config["DEBUG"]:
	app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
	app.run(debug=app.config['DEBUG'])
