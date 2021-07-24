class Question():
    def __init__(self, id, body, type):
        self.id = id
        self.body = body
        self.type = type

    TEXT = 'text'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'