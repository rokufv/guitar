# data_loader.py

from config import GOOGLE_API_KEY
from equipment_data import EQUIPMENT_DATA
from langchain_core.documents import Document

# 練習フレーズのデータ
PRACTICE_PHRASES = {
    "B'z 松本孝弘": {
        "title": "GO FURTHER",
        "youtube_url": "https://www.youtube.com/watch?v=5VdJ-1d_4DQ",
        "tab_url": "https://www.ultimate-guitar.com/search.php?search_type=title&value=go%20further%20tak%20matsumoto"
    },
    "布袋寅泰": {
        "title": "BATTLE WITHOUT HONOR OR HUMANITY",
        "youtube_url": "https://www.youtube.com/watch?v=oFvgeA1S1tQ",
        "tab_url": "https://www.ultimate-guitar.com/search.php?search_type=title&value=BATTLE%20WITHOUT%20HONOR%20OR%20HUMANITY"
    },
    "結束バンド 後藤ひとり": {
        "title": "ギターと孤独と蒼い惑星",
        "youtube_url": "https://www.youtube.com/watch?v=B53s_pC_L9M",
        "tab_url": "https://www.ultimate-guitar.com/search.php?search_type=title&value=%E3%82%AE%E3%82%BF%E3%83%BC%E3%81%A8%E5%AD%A4%E7%8B%AC%E3%81%A8%E8%92%BC%E3%81%84%E6%83%91%E6%98%9F"
    }
}

def get_equipment_data(guitarist_name: str) -> list[Document]:
    """指定されたギタリストの機材データを取得する"""
    # ギタリスト名のマッピング
    name_map = {
        "B'z 松本孝弘": "TAK",
        "布袋寅泰": "HOTEI",
        "結束バンド 後藤ひとり": "GOTOH"
    }
    data_key = name_map.get(guitarist_name, guitarist_name)
    equipment_list = EQUIPMENT_DATA.get(data_key, [])
    
    # 機材データをDocumentオブジェクトに変換
    documents = []
    for equipment in equipment_list:
        try:
            # 価格を日本円表記に変換
            price = equipment.get('price', 0)
            price_str = f"¥{price:,}" if isinstance(price, (int, float)) and price > 0 else "非売品"
            
            # コンテンツの作成
            content = (
                f"機材名: {equipment.get('name', '')}\n"
                f"タイプ: {equipment.get('type', '')}\n"
                f"価格: {price_str}\n"
                f"レベル: {equipment.get('level', '')}\n"
                f"特徴: {equipment.get('characteristics', '')}"
            )
            
            # メタデータの作成
            metadata = equipment.copy()
            metadata['guitarist'] = guitarist_name
            
            # Documentオブジェクトを作成
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        except Exception as e:
            print(f"機材データの変換中にエラーが発生しました: {e}")
            continue
    
    return documents

def get_practice_phrase(guitarist_name: str) -> dict:
    """指定されたギタリストの練習フレーズデータを取得する"""
    return PRACTICE_PHRASES.get(guitarist_name, {})