# data_loader.py

from config import GOOGLE_API_KEY
from equipment_data import EQUIPMENT_DATA  # 新しいデータソースをインポート
from langchain_core.documents import Document

DUMMY_EQUIPMENT_DATA = {
    "B'z 松本孝弘": [
        {
            "name": "Gibson Les Paul Tak Matsumoto Signature",
            "type": "ギター",
            "price": 450000,
            "level": "上級",
            "characteristics": "太く粘りのあるサウンドと高いサステイン。松本孝弘のメインギター。"
        },
        {
            "name": "Gibson Tak Matsumoto Double Cutaway",
            "type": "ギター",
            "price": 380000,
            "level": "中級",
            "characteristics": "軽量で扱いやすく、クリアなトーンが特徴。"
        },
        {
            "name": "Fender Stratocaster",
            "type": "ギター",
            "price": 150000,
            "level": "中級",
            "characteristics": "多彩なサウンドバリエーション。クリーンから歪みまで幅広く対応。"
        },
        {
            "name": "Marshall JCM2000",
            "type": "アンプ",
            "price": 180000,
            "level": "上級",
            "characteristics": "ロックに最適なパワフルな歪み。松本サウンドの核。"
        },
        {
            "name": "Marshall 1959SLP",
            "type": "アンプ",
            "price": 250000,
            "level": "上級",
            "characteristics": "伝統的なブリティッシュロックサウンド。"
        },
        {
            "name": "BOSS SD-1",
            "type": "エフェクター",
            "price": 6000,
            "level": "初級",
            "characteristics": "滑らかなオーバードライブ。ソロ時のブーストにも最適。"
        },
        {
            "name": "BOSS DD-3",
            "type": "エフェクター",
            "price": 12000,
            "level": "初級",
            "characteristics": "クリアなデジタルディレイ。"
        },
        {
            "name": "Ibanez TS9",
            "type": "エフェクター",
            "price": 11000,
            "level": "中級",
            "characteristics": "ミッドが強調されたオーバードライブ。"
        },
        {
            "name": "MXR Phase 90",
            "type": "エフェクター",
            "price": 11000,
            "level": "初級",
            "characteristics": "特徴的なフェイザーサウンド。"
        },
        {
            "name": "Jim Dunlop Tortex 0.88mm",
            "type": "ピック",
            "price": 150,
            "level": "初級",
            "characteristics": "適度な硬さでコントロールしやすい。"
        },
        {
            "name": "B'z 松本孝弘",
            "type": "エフェクター",
            "price": 0,
            "level": "上級",
            "characteristics": "感情的なサウンド表現に欠かせない、彼の代名詞とも言えるエフェクト。"
        }
    ],
    "布袋寅泰": [
        {
            "name": "Fender Telecaster HOTEIモデル",
            "type": "ギター",
            "price": 220000,
            "level": "中級",
            "characteristics": "鋭いカッティングと独特のルックス。"
        },
        {
            "name": "Gretsch G6136T HOTEIモデル",
            "type": "ギター",
            "price": 350000,
            "level": "上級",
            "characteristics": "煌びやかなクリーンサウンドと豊かなサスティン。"
        },
        {
            "name": "Gibson Les Paul Custom",
            "type": "ギター",
            "price": 400000,
            "level": "上級",
            "characteristics": "重厚なサウンドと高級感。"
        },
        {
            "name": "Marshall JCM800",
            "type": "アンプ",
            "price": 170000,
            "level": "上級",
            "characteristics": "80年代ロックの定番アンプ。"
        },
        {
            "name": "Roland JC-120",
            "type": "アンプ",
            "price": 120000,
            "level": "中級",
            "characteristics": "クリーンで立体的なコーラスサウンド。"
        },
        {
            "name": "BOSS DS-1",
            "type": "エフェクター",
            "price": 6000,
            "level": "初級",
            "characteristics": "鋭いディストーション。"
        },
        {
            "name": "BOSS CE-2",
            "type": "エフェクター",
            "price": 15000,
            "level": "中級",
            "characteristics": "温かみのあるコーラス。"
        },
        {
            "name": "Line 6 DL4",
            "type": "エフェクター",
            "price": 25000,
            "level": "中級",
            "characteristics": "多彩なディレイサウンド。"
        },
        {
            "name": "Electro-Harmonix Big Muff",
            "type": "エフェクター",
            "price": 13000,
            "level": "中級",
            "characteristics": "分厚いファズサウンド。"
        },
        {
            "name": "Jim Dunlop Nylon 1.0mm",
            "type": "ピック",
            "price": 150,
            "level": "初級",
            "characteristics": "しっかりしたアタック感。"
        }
    ],
    "結束バンド 後藤ひとり": [
        {
            "name": "Fender Made in Japan Stratocaster",
            "type": "ギター",
            "price": 110000,
            "level": "中級",
            "characteristics": "明るく抜けの良いサウンド。"
        },
        {
            "name": "Squier Classic Vibe '60s Stratocaster",
            "type": "ギター",
            "price": 55000,
            "level": "初級",
            "characteristics": "コストパフォーマンスに優れたストラト。"
        },
        {
            "name": "Fender Mustang",
            "type": "ギター",
            "price": 90000,
            "level": "中級",
            "characteristics": "小柄で扱いやすい。"
        },
        {
            "name": "Roland JC-40",
            "type": "アンプ",
            "price": 60000,
            "level": "初級",
            "characteristics": "クリーンで透明感のあるサウンド。"
        },
        {
            "name": "Fender Champion 40",
            "type": "アンプ",
            "price": 35000,
            "level": "初級",
            "characteristics": "多彩なアンプモデリング搭載。"
        },
        {
            "name": "BOSS BD-2",
            "type": "エフェクター",
            "price": 9000,
            "level": "初級",
            "characteristics": "ブルース向きのオーバードライブ。"
        },
        {
            "name": "BOSS DD-7",
            "type": "エフェクター",
            "price": 16000,
            "level": "中級",
            "characteristics": "多機能デジタルディレイ。"
        },
        {
            "name": "Ibanez TS808",
            "type": "エフェクター",
            "price": 18000,
            "level": "中級",
            "characteristics": "伝統的なチューブスクリーマーサウンド。"
        },
        {
            "name": "Electro-Harmonix Soul Food",
            "type": "エフェクター",
            "price": 12000,
            "level": "中級",
            "characteristics": "ナチュラルなブーストと歪み。"
        },
        {
            "name": "Fender 351 Shape Medium",
            "type": "ピック",
            "price": 100,
            "level": "初級",
            "characteristics": "標準的な形状で扱いやすい。"
        }
    ]
}

def get_equipment_data(guitarist_name: str) -> list[Document]:
    """指定されたギタリストの機材データを取得する"""
    equipment_list = EQUIPMENT_DATA.get(guitarist_name, [])
    
    # 機材データをDocumentオブジェクトに変換
    documents = []
    for equipment in equipment_list:
        try:
            # 価格を日本円表記に変換
            price = equipment.get('price', 0)  # 価格が存在しない場合は0を設定
            price_str = f"¥{price:,}" if isinstance(price, (int, float)) and price > 0 else "非売品"
            
            # 機材情報を文字列に変換
            content = (
                f"機材名: {equipment.get('name', '')}\n"
                f"タイプ: {equipment.get('type', '')}\n"
                f"価格: {price_str}\n"
                f"レベル: {equipment.get('level', '')}\n"
                f"特徴: {equipment.get('characteristics', '')}"
            )
            
            # Documentオブジェクトを作成
            doc = Document(
                page_content=content,
                metadata={
                    "name": equipment.get('name', ''),
                    "type": equipment.get('type', ''),
                    "price": price,
                    "level": equipment.get('level', ''),
                    "guitarist": guitarist_name
                }
            )
            documents.append(doc)
        except Exception as e:
            print(f"機材データの変換中にエラーが発生しました: {e}")
            continue
    
    return documents

def get_practice_phrase(guitarist_name):
    """従来の練習フレーズデータ（後方互換性のため残す）"""
    phrases = {
        "B'z 松本孝弘": {
            "title": "Ultra Soul リフ",
            "youtube_url": "https://www.youtube.com/watch?v=P53EuU4-p8Y&list=RDP53EuU4-p8Y&start_radio=1"
        },
        "布袋寅泰": {
            "title": "スリル リフ",
            "tab_譜": "e|----------------|\nB|----------------|\nG|----------------|",
            "audio_path": "audio/thrill.mp3"
        },
        "結束バンド 後藤ひとり": {
            "title": "青春コンプレックス リフ",
            "tab_譜": "e|----------------|\nB|----------------|\nG|----------------|",
            "audio_path": "audio/seishun_complex.mp3"
        }
    }
    return phrases.get(guitarist_name)