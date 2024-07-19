from src.foreman import ForemanMixin
from src.scanner import ScannerMixin


class Site(ScannerMixin, ForemanMixin):
    def __init__(self, name: str, chat_id: int, client_id: str, ranges: set):
        ScannerMixin.__init__(self, ranges)  # Инициализируем ScannerMixin
        ForemanMixin.__init__(self, client_id)  # Инициализируем ForemanMixin
        self.name = name
        self.chat_id = chat_id

    def __repr__(self):
        return self.name
