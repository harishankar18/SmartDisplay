from flask import render_template
from Messages import Messages


class NoItemsInQueue(Messages):
    """
        The current class is responsible for generating
        template when no items are presenting in the Queue
    """
    def __init__(self, content = "No items in the Queue",
                 template = "NoItems.html", timeout = 4000):
        super(NoItemsInQueue, self).__init__(content, 10, timeout)
        self.template = template        #The current template will retry after every 4 secs.

    def render_page(self, device):
        return render_template(self.template, team_name=self.content,
                               page_timeout=self.timeout, client=device)