# models/data.py

class Data:
    def __init__(self, data_id, value):
        self.data_id = data_id
        self.value = value

    def __repr__(self):
        return f"<Data {self.data_id}: {self.value}>"
