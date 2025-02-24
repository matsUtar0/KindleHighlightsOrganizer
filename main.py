import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QDialog,
    QLabel, QComboBox
)
from PyQt5.QtCore import Qt

# 各種モジュールをインポート
from ocr_processor import OCRProcessor
from toc_manager import TOCManager
from kindle_parser import KindleParser
from matcher import match_highlights_to_toc
from markdown_exporter import MarkdownExporter

# 手動入力用ダイアログ（複数行入力対応）の追加
class ManualTOCInputDialog(QDialog):
    def __init__(self, toc_manager, parent=None):
        super().__init__(parent)
        self.toc_manager = toc_manager
        self.setWindowTitle("手動で目次を入力")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # 入力方法の説明ラベル
        instruction = QLabel("以下のフォーマットで複数行入力してください：\n"
                             "タイトル,位置番号\n"
                             "タイトル,位置番号")
        layout.addWidget(instruction)
        
        # 複数行入力用テキストエリア
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        self.btn_add = QPushButton("追加")
        self.btn_close = QPushButton("閉じる")
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_close)
        layout.addLayout(button_layout)
        
        self.btn_add.clicked.connect(self.add_entries)
        self.btn_close.clicked.connect(self.accept)
    
    def add_entries(self):
        content = self.text_input.toPlainText()
        lines = content.strip().splitlines()
        if not lines:
            QMessageBox.warning(self, "入力エラー", "何も入力されていません。")
            return
        
        added_count = 0
        for line in lines:
            # 各行は "タイトル,位置番号" の形式で入力
            parts = line.split(',')
            if len(parts) != 2:
                continue
            title = parts[0].strip()
            page_str = parts[1].strip()
            if not title or not page_str.isdigit():
                continue
            page = int(page_str)
            self.toc_manager.add_toc_entry(title, page)
            added_count += 1
        
        if added_count > 0:
            QMessageBox.information(self, "追加完了", f"{added_count} 件の目次エントリを追加しました。")
        else:
            QMessageBox.warning(self, "入力エラー", "正しいフォーマットの入力がありません。")
        
        self.text_input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kindleメモ整理アプリ（サンプル）")
        self.resize(800, 600)

        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # レイアウト設定
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # タイトル情報入力方式のプルダウンと実行ボタン
        input_layout = QHBoxLayout()
        input_label = QLabel("タイトル情報入力方式:")
        input_layout.addWidget(input_label)

        self.input_mode_combo = QComboBox()
        self.input_mode_combo.addItems(["OCR", "CSV読み込み", "手動入力"])
        input_layout.addWidget(self.input_mode_combo)

        self.btn_input = QPushButton("目次入力実行")
        self.btn_input.clicked.connect(self.handle_input_mode)
        input_layout.addWidget(self.btn_input)
        main_layout.addLayout(input_layout)

        # Kindle JSON選択ボタンおよびMarkdown出力ボタンの配置
        button_layout = QHBoxLayout()
        self.btn_select_json = QPushButton("Kindle JSON読込")
        self.btn_select_json.clicked.connect(self.handle_select_json)
        button_layout.addWidget(self.btn_select_json)

        self.btn_export_markdown = QPushButton("Markdown出力")
        self.btn_export_markdown.clicked.connect(self.handle_export_markdown)
        button_layout.addWidget(self.btn_export_markdown)
        main_layout.addLayout(button_layout)

        # ログ表示用テキストエリア
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        # バックエンド処理クラスのインスタンス
        self.ocr_processor = OCRProcessor()
        self.toc_manager = TOCManager()
        self.kindle_parser = KindleParser()

        self.log("アプリが起動しました。")

    def log(self, message: str):
        """ログエリアにメッセージを表示する"""
        self.log_area.append(message)

    def handle_input_mode(self):
        """プルダウンで選択された入力方式に応じた目次入力を実行する"""
        mode = self.input_mode_combo.currentText()
        if mode == "OCR":
            self.handle_select_images()
        elif mode == "CSV読み込み":
            self.handle_select_csv()
        elif mode == "手動入力":
            self.handle_manual_input()
        else:
            QMessageBox.warning(self, "入力エラー", "入力方式が正しく選択されていません。")

    def handle_select_images(self):
        """OCRによる目次キャプチャ画像の選択と処理"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "目次画像を選択", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.heic)"
        )
        if not files:
            return

        self.log("OCR処理を開始します...")
        # OCR処理を実行
        for image_path in files:
            try:
                toc_list = self.ocr_processor.run_ocr(image_path)
                for title, page in toc_list:
                    self.toc_manager.add_toc_entry(title, page)
                self.log(f"OCR完了: {image_path}")
            except Exception as e:
                self.log(f"OCRエラー: {image_path} - {str(e)}")

        self.log("すべてのOCR処理が完了しました。")

    def handle_select_csv(self):
        """目次CSVファイルの選択と読み込み"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "目次CSVを選択", os.getcwd(), "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            self.toc_manager.load_from_csv(file_path)
            self.log(f"CSV読み込み完了: {file_path}")
        except Exception as e:
            self.log(f"CSV読み込みエラー: {str(e)}")

    def handle_select_json(self):
        """KindleメモJSONファイルの選択と読み込み"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Kindle JSONを選択", os.getcwd(), "JSON Files (*.json)"
        )
        if not file_path:
            return

        try:
            self.kindle_parser.load_json(file_path)
            self.log(f"Kindleメモ読み込み完了: {file_path}")
        except Exception as e:
            self.log(f"JSON読み込みエラー: {str(e)}")

    def handle_export_markdown(self):
        """Markdown形式で出力"""
        matched_data = match_highlights_to_toc(self.toc_manager.toc_data, self.kindle_parser.highlights)
        exporter = MarkdownExporter()
        output_file = os.path.join(os.getcwd(), "output.txt")
        exporter.export(matched_data, output_file)
        self.log(f"Markdown出力完了: {output_file}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
