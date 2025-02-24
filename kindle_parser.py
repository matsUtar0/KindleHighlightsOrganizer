import json
from typing import List, Dict, Any

class KindleParser:
    def __init__(self):
        # highlightsは「{ 'text': str, 'location': int, ... }」のリストを想定
        self.highlights: List[Dict[str, Any]] = []

    def load_json(self, file_path: str):
        """Kindleメモ（JSON形式）を読み込み、ハイライト情報をself.highlightsに格納"""
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
        
        # data の構造はユーザー提供のJSON形式に合わせる
        # 例: { "asin": "...", "title": "...", "highlights": [ {...}, ... ] }
        if "highlights" in data:
            for item in data["highlights"]:
                text = item.get("text", "")
                location_value = item.get("location", {}).get("value", 0)
                self.highlights.append({
                    "text": text,
                    "location": location_value
                })
