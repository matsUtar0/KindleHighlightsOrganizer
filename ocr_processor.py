import os
import re
from PIL import Image
import pillow_heif  # HEIC対応のため追加
import pyocr
import pyocr.builders

class OCRProcessor:
    def __init__(self):
        # Tesseract のパスを環境に応じて指定する場合はここで設定
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise ImportError("Tesseract が見つかりません。インストールされているか確認してください。")
        self.tool = tools[0]

    def convert_heic_to_jpeg(self, heic_path: str) -> str:
        """
        HEIC 画像を JPEG に変換し、一時ファイルとして保存してそのパスを返す。
        """
        heif_file = pillow_heif.open_heif(heic_path)
        image = Image.frombytes(
            heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode
        )
        temp_jpeg_path = heic_path + ".jpg"
        image.save(temp_jpeg_path, format="JPEG")
        return temp_jpeg_path

    def run_ocr(self, image_path: str):
        """
        画像から OCR でテキストを抽出し、行ごとに「タイトル」「ページ番号」を返す。
        対応フォーマット: PNG, JPG, JPEG, HEIC
        戻り値: List[Tuple[str, int]]
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"ファイルが存在しません: {image_path}")

        # HEIC ファイルの場合は JPEG に変換
        temp_file = None
        if image_path.lower().endswith(".heic"):
            temp_file = self.convert_heic_to_jpeg(image_path)
            image_path = temp_file  # 変換後のJPEGをOCR対象とする

        # 画像を開く
        img = Image.open(image_path)

        # OCR 実行
        text = self.tool.image_to_string(
            img,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )

        # 一時的に作成した JPEG ファイルを削除
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

        # OCR 結果の処理
        lines = text.split("\n")
        toc_list = []

        # 行ごとにパース
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 例: "第1章 理論編 12" のような末尾の数字を抽出
            match = re.search(r'(\d+)$', line)
            if match:
                page_str = match.group(1)
                page_num = int(page_str)
                # タイトル部分をページ番号以外として切り出し
                title = line[: line.rfind(page_str)].strip()
                toc_list.append((title, page_num))

        return toc_list
