from typing import List, Dict, Any

class MarkdownExporter:
    def export(self, matched_data: List[Dict[str, Any]], output_path: str):
        """
        matched_dataをMarkdown形式に整形し、output_pathに書き出す。
        
        仕様:
        - 各ハイライトごとの区切りは、「改行」「---」「改行」とする。
        - 章区切りには区切り線を一切挿入しない。
        - 各ハイライトの先頭に「- 」は付けない。
        - ハイライト内に含まれるタブおよび全角スペースは、改行に変換して出力する。
          ※ 半角スペースは英文の単語間の区切りとして維持し、改行した各行の先頭の余分なスペースは除去する。
        """
        lines = []
        # 各章について処理
        for toc_item in matched_data:
            # 章タイトルを出力
            lines.append(f"## {toc_item['title']}")
            lines.append("")  # タイトル後の空行
            
            # 各ハイライトごとに処理
            for hl in toc_item["highlights"]:
                # タブと全角スペースを改行に置換（半角スペースは維持）
                hl_clean = hl.replace("\t", "\n").replace("　", "\n")
                # 各行の先頭の余分なスペースを除去
                hl_clean = "\n".join(line.lstrip() for line in hl_clean.splitlines())
                lines.append(hl_clean)
                # 各ハイライトの区切り（「改行」「---」「改行」）
                lines.append("")
                lines.append("---")
                lines.append("")
        
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write("\n".join(lines))
