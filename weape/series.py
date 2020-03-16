class Series:
    def __init__(self, values: list):
        self.label: str = values.pop(0)
        self.values: list = values
