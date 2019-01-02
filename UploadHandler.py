from werkzeug.utils import secure_filename
from flask import render_template, request
from TeamMessage import TeamMessage
from VideoMessage import VideoMessage
from os.path import join, basename


"""
    class responsible for accepting the images and video
    as team stats.
"""
class UploadHandler:
    def __init__(self, app, cfg, message_queue):
        self.app = app
        upload_folder = cfg.parser.get('Application', 'file_upload_folder')
        app.config['UPLOAD_FOLDER'] = upload_folder
        self.allowed_extensions = cfg.parser.get('Application', 'file_types').split(",")
        self.file_upload_template = cfg.parser.get('Application', 'file_upload_template')

        self.message_queue = message_queue
        self.expiration = cfg.parser.getint('team_site', 'expiration')
        self.timeout = cfg.parser.getint('team_site', 'timeout')
        self.template = cfg.parser.get('team_site', 'template')

    def allowed_file(self, filename):
        """
            validates whether the file received in valid format.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def render_upload_template(self):
        return render_template(self.file_upload_template)

    def save_file(self):
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'No selected file'

            f = request.files['file']

            if f.filename == '':
                return 'No selected file'

            if file and self.allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(join(self.app.config['UPLOAD_FOLDER'], filename))
                self.insert_message_queue(f.filename)
                return '<h1> file uploaded successfully </h1>'
            else:
                return "<h1> file format is not yet supported </h1> "
        return "<h1> Error in uploading the file </h1>"

    def create_message(self, file_path):
        filetype = basename(file_path).split(".")[1]
        author = basename(file_path).split(".")[0]
        if filetype == "mp4":
            message = VideoMessage(basename(file_path))
        else:
            message = TeamMessage(basename(file_path), author, self.expiration, self.template, self.timeout)
        return message

    def insert_message_queue(self, filename):
        team_msg = self.create_message(filename)
        result = self.message_queue.enqueue(team_msg)
        return result

