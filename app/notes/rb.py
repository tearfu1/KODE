class RBNote:
    def __init__(self, id: int | None = None,
                 title: int | None = None,
                 content: int | None = None,
                 ):
        self.id = id
        self.title = title
        self.content = content

    def to_dict(self) -> dict:
        data = {'id': self.id,
                'title': self.title,
                'content': self.content,
                }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
