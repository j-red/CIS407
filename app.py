"""
Flask web site with vocabulary matching game
(identify vocabulary words that can be made
from a scrambled string)
"""

import os, flask
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import logging
import config

# Globals
app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

# # Create a directory in a known location to save files to.
# uploads_dir = os.path.join(app.instance_path, 'uploads')
# os.makedirs(uploads_dir, exist_ok=True)

# Pages
# @app.route("/")
# # @app.route('/pdf')
# # def pdf():
# #     return flask.render_template('pdf.html')
# #
# # @app.route('/', methods=['POST'])
# # # @app.route('/pdf', methods=['POST'])
# # def upload_files():
# #     uploaded_file = request.files['file']
# #     filename = secure_filename(uploaded_file.filename)
# #     if filename != '':
# #         file_ext = os.path.splitext(filename)[1]
# #         if file_ext not in app.config['UPLOAD_EXTENSIONS']: # could also validate pdf here?
# #             abort(400)
# #
# #         uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], file.name))
# #         app.logger.info(f"wrote file to {os.path.join(app.config['UPLOAD_PATH'], filename)}")
# #
# #     return redirect(url_for('pdf'))

# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

# request.files['profile']  # single file (even if multiple were sent)
# request.files.getlist('charts')  # list of files (even if one was sent)

@app.route('/pdf', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # save the single "profile" file
        profile = request.files['profile']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        # save each "charts" file
        for file in request.files.getlist('charts'):
            file.save(os.path.join(uploads_dir, secure_filename(file.name)))

        return redirect(url_for('pdf'))

    return render_template('pdf.html')




# Error handlers
@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    return flask.render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403

@app.errorhandler(413)
def error_403(e):
    app.logger.warning("++ 413 error: {}".format(e))
    return flask.render_template('413.html'), 413

@app.errorhandler(405)
def error_405(e):
    app.logger.warning("++ 405 error: {}".format(e))
    return flask.render_template('413.html'), 405

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
        app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
    app.run(host="0.0.0.0", port=CONFIG.PORT)
