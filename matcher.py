from typing import List, Tuple, Dict, Any

def match_highlights_to_toc(
    toc_data: List[Tuple[str, int]], 
    highlights: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    目次データとハイライトをマッチングし、
    章ごとのハイライトリストを返す。
    戻り値は以下のような構造:
    [
      {
        'title': '第1章 ～',
        'page': 10,
        'highlights': [
            'ハイライト本文1',
            'ハイライト本文2',
            ...
        ]
      },
      ...
    ]
    """

    # 目次をページ番号でソートしておく
    sorted_toc = sorted(toc_data, key=lambda x: x[1])

    # 返却用のデータ構造を作る
    result = []
    for title, page in sorted_toc:
        result.append({
            "title": title,
            "page": page,
            "highlights": []
        })

    # ハイライトをページ番号順にソート
    sorted_highlights = sorted(highlights, key=lambda x: x["location"])

    # 目次が空の場合はスキップ
    if not result:
        return []

    # マッチングロジック
    last_index = len(result) - 1
    current_toc_idx = 0

    for hl in sorted_highlights:
        hl_page = hl["location"]

        # current_toc_idxを進めながら、ハイライトが入る章を探す
        # ルール:
        #   - ハイライトのpage >= 現在の章のpage かつ
        #   - 次の章があれば、次の章のpage > ハイライトpage
        #   - 次の章が存在しない(最終章)の場合は、すべて最終章に入れる
        while current_toc_idx < last_index:
            current_page = result[current_toc_idx]["page"]
            next_page = result[current_toc_idx + 1]["page"]
            if hl_page >= current_page and hl_page < next_page:
                break
            elif hl_page >= next_page:
                current_toc_idx += 1
            else:
                break

        # 見つかった章にハイライトを追加
        result[current_toc_idx]["highlights"].append(hl["text"])

    return result
