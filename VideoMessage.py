from os import remove
from os.path import join
from flask import render_template
from Messages import Messages


class VideoMessage(Messages):
    def __init__(self, content):
        super(VideoMessage, self).__init__(content)
        self.resource_path = "static/"
        self.template = "video.html"
        self.content = content

    def render_page(self, device):
        return render_template(self.template, video_path=self.content, client=device)

    def __del__(self):
        path = join(self.resource_path, self.content)
        remove(path)