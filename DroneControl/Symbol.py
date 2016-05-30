class Symbol(object):
    def __init__(self, image, command):
        self._image = image
        self._command = command

    @property
    def image(self):
        return self._image

    @property
    def command(self):
        return self._command