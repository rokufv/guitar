# data_loader.py

from config import GOOGLE_API_KEY
from equipment_data import EQUIPMENT_DATA
from langchain_core.documents import Document
import os
import re
import json # JSONを扱うためにインポート

# 練習フレーズのデータ
PRACTICE_PHRASES = {
    "B'z 松本孝弘": {
        "title": "ultra soul",
        "youtube_url": "https://www.youtube.com/watch?v=P53EuU4-p8Y&list=RDP53EuU4-p8Y&start_radio=1",
    }
}

# --- グローバル変数 ---
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIPMENT_FILES = {
    "B'z 松本孝弘": os.path.join(DATA_DIR, "tak_gear.doc"),
    "布袋寅泰": os.path.join(DATA_DIR, "hotei_gear.doc"),
    "結束バンド 後藤ひとり": os.path.join(DATA_DIR, "gotoh_gear.doc"),
}
PRACTICE_PHRASES_FILE = os.path.join(DATA_DIR, "practice_phrases.json")


def get_equipment_data(guitarist: str) -> list[Document]:
    """
    指定されたギタリストの機材データをファイルから読み込み、
    Documentオブジェクトのリストとして返す。
    全ての機材データは同じテキスト形式として処理する。
    """
    file_path = EQUIPMENT_FILES.get(guitarist)
    if not file_path or not os.path.exists(file_path):
        return []

    documents = []

    # 全てのファイルを同じロジックで処理
    with open(file_path, "r", encoding="utf-8") as f:
        content_full = f.read()

    # 各機材のブロックに分割
    equipment_blocks = re.split(r'\n---\n', content_full.strip())

    for block in equipment_blocks:
        if not block.strip():
            continue

        lines = block.strip().split('\n')
        equipment = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(':', 1)
                key_map = {
                    '機材名': 'name',
                    'タイプ': 'category', # 'type' ではなく 'category' に統一
                    '価格': 'price',
                    '特徴': 'characteristics'
                }
                internal_key = key_map.get(key.strip())
                if internal_key:
                    equipment[internal_key] = value.strip()
        
        # 価格情報を取得
        price_str = equipment.get('price', 'N/A')
        
        # メタデータを生成
        metadata = {
            "name": equipment.get('name', 'N/A'),
            "category": equipment.get('category', 'N/A'), # 'type' ではなく 'category' を参照
            "price": price_str,
            "characteristics": equipment.get('characteristics', 'N/A')
        }
        
        # Document のコンテンツを生成
        content = (
            f"機材名: {metadata.get('name', '')}\n"
            f"カテゴリ: {metadata.get('category', '')}\n"
            f"価格: {metadata.get('price', '')}\n"
            f"概要: {metadata.get('characteristics', '')}"
        )
        documents.append(Document(page_content=content, metadata=metadata))
            
    return documents

def get_practice_phrase(guitarist: str) -> dict:
    """指定されたギタリストの練習フレーズデータを取得する"""
    return PRACTICE_PHRASES.get(guitarist, {})