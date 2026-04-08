class Memory:
    def __init__(self):
        self.data = []

    def add(self, text):
        self.data.append(text)

    def get_recent(self):
        return "\n".join(self.data[-5:])