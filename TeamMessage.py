from os import remove
from os.path import join
from flask import render_template
from Messages import Messages

#TODO overloaded __del__ can be moved upwards to optimize the imports.

class TeamMessage(Messages):
    def __init__(self, content, author, expire_time, template, timeout):
        super(TeamMessage, self).__init__(content, expire_time, timeout)
        self.resource_path="static/"
        self.template = template
        self.content = content
        self.author = author

    def render_page(self, device):
        return render_template(self.template, image_path=self.content,
                               team_name=self.author, page_timeout=self.timeout,
                               client=device)

    def __del__(self):
        path = join(self.resource_path, self.content)
        remove(path)