from foreman import ForemanMixin
from scanner import ScannerMixin


class Site(ScannerMixin, ForemanMixin):
    def __init__(self, name: str, chat_id: int, client_id: str, ranges: set):
        super().__init__(client_id)  # Инициализируем ForemanMixin
        self.name = name
        self.chat_id = chat_id
        self.ranges = ranges

    def __repr__(self):
        return self.name
