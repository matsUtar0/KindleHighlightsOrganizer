import csv
from typing import List, Tuple

class TOCManager:
    def __init__(self):
        # toc_data: List[Tuple[title, page]]
        self.toc_data: List[Tuple[str, int]] = []

    def add_toc_entry(self, title: str, page: int):
        """目次情報を追加"""
        self.toc_data.append((title, page))

    def load_from_csv(self, csv_path: str):
        """CSVファイルから目次情報を読み込み、toc_dataにセット"""
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                title = row[0].strip()
                page_str = row[1].strip()
                if page_str.isdigit():
                    page_num = int(page_str)
                    self.add_toc_entry(title, page_num)

    def export_to_csv(self, csv_path: str):
        """現在の目次情報をCSVに書き出す"""
        with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for title, page in self.toc_data:
                writer.writerow([title, page])

    def clear(self):
        self.toc_data = []
