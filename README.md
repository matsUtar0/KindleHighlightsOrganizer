<<<<<<< HEAD
# KindleHighlightsOrganizer
=======
# Kindle Highlights Organizer

Kindle Highlights Organizer は、Kindle のハイライト情報を章ごとに整理し、Markdown 形式で出力するデスクトップアプリケーションです。  
本アプリケーションは、OCR、CSV 読み込み、手動入力（プルダウン選択方式）によって書籍の目次情報を取得し、Kindle の JSON 形式のハイライトデータとマッチングして、各章ごとにハイライトを整理します.

---

## 特徴

- **OCR による目次画像解析**  
  - 対応フォーマット: PNG, JPG, JPEG, HEIC  
  - [pillow-heif](https://pypi.org/project/pillow-heif/) を使用して HEIC ファイルを JPEG に変換し、pyocr/Tesseract でテキスト抽出を実施

- **タイトル情報の入力方式 (プルダウン選択)**  
  ユーザーは、以下の入力方式の中からプルダウンメニューで選択できます:
  - **OCR**: 目次画像から自動抽出
  - **CSV読み込み**: CSV ファイルから取り込み
  - **手動入力**: GUI 上で「タイトル,位置番号」形式の複数行入力  
  ※ 入力方式に応じたインターフェースが動的に切り替わります

- **Kindle JSON 取り込み**  
  Kindle メモの JSON ファイルを読み込み、各ハイライトのテキストおよび位置情報を抽出します.

- **マッチング処理**  
  目次情報と Kindle ハイライトの位置情報を、以下のルールに従って照合し、各章に対応するハイライトを整理します:
  - ハイライトの位置が、該当章のページ番号以上かつ次章のページ番号未満の場合、その章に紐づける

- **Markdown 出力**  
  マッチング結果は Markdown 形式に整形して出力されます。仕様は以下の通り:
  - **各ハイライトごとの区切り**は「改行」「---」「改行」として挿入
  - **章区切り**では区切り線は一切挿入しない
  - ハイライト内の **タブおよび全角スペース** は改行に変換  
    ※ 半角スペース（英文の単語間のスペース）はそのまま保持し、改行後の各行の先頭の余分なスペースは除去

- **GUI インターフェース (PyQt5)**  
  - プルダウンメニューにより、タイトル情報の入力方式を **OCR**、**CSV読み込み**、**手動入力** の中から選択
  - 各入力方式に応じ、ファイル選択ダイアログや手動入力ダイアログが起動
  - 進捗やエラーはログエリアに表示されます

---

## ファイル構成

- **main.py**  
  - アプリケーションのエントリーポイント  
  - GUI のレイアウト、プルダウンメニューでの入力方式切替、ファイル選択ダイアログ、各種ボタンのイベントハンドラ（OCR、CSV 読込、手動入力、Kindle JSON 読込、Markdown 出力）を実装

- **ocr_processor.py**  
  - pyocr/Tesseract を利用して画像からテキストを抽出  
  - HEIC ファイルを JPEG に変換して OCR 処理を実施

- **toc_manager.py**  
  - OCR、CSV、GUI 手入力で取得した目次情報（タイトルとページ番号）の管理  
  - CSV へのエクスポート機能も提供

- **kindle_parser.py**  
  - Kindle メモの JSON をパースし、ハイライト情報（テキストと位置番号）を抽出

- **matcher.py**  
  - 目次情報と Kindle ハイライトデータをページ番号に基づいてマッチングし、各章ごとのハイライトリストを生成

- **markdown_exporter.py**  
  - マッチング結果を Markdown 形式に整形して出力  
  - 各ハイライトの区切りは「改行」「---」「改行」とする。章区切りの区切り線は出力しない

---

## 環境要件

- **OS:** macOS（10.14 以降推奨）
- **Python:** 3.7 以降
- **依存ライブラリ:**  
  - PyQt5  
  - pyocr  
  - Pillow  
  - pillow-heif  
  - （必要に応じて jaconv など）

- **OCR エンジン:**  
  - Tesseract (Homebrew 等でインストール)

---

## セットアップ手順

1. **仮想環境の作成と有効化**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```
2. **必要なライブラリのインストール (仮想環境内)**
   ```bash
   pip install pyinstaller pyqt5 pyocr pillow pillow-heif
   ```

## アプリの実行方法
1. **開発環境での実行**
   仮想環境内で以下のコマンドを実行してアプリを起動します.
   ```bash
   python main.py
   ```
   ※ プルダウンで入力方式（OCR、CSV読み込み、手動入力）を選び、対応する目次情報の入力・読み込みを行います.
>>>>>>> c827fa9 (Initial commit: Add program files and README)
