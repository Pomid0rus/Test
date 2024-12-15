from datetime import datetime, date


class RBAuthor:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 date_of_birth: date):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

    def to_dict(self) -> dict:
        data = {'first_name': self.first_name,
                'last_name': self.last_name,
                'date_of_birth': self.date_of_birth}
        return data


class RBBook:
    def __init__(self,
                 author_id: int,
                 title: str,
                 description: str | None = None,
                 copies: int | None = 0):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.copies = copies

    def to_dict(self) -> dict:
        data = {'title': self.title,
                'description': self.description,
                'author_id': self.author_id,
                'copies': self.copies}
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return filtered_data


class RBBorrow:
    def __init__(self,
                 book_id: int,
                 name: str,
                 date_of_issue: date | None = datetime.now().date()
                 ):
        self.book_id = book_id
        self.name = name
        self.date_of_issue = date_of_issue
        self.date_of_return = None

    def to_dict(self) -> dict:
        data = {'book_id': self.book_id,
                'name': self.name,
                'date_of_issue': self.date_of_issue,
                'date_of_return': self.date_of_return}
        filtered_data = {key: value for key,
                         value in data.items() if value is not None}
        return filtered_data
