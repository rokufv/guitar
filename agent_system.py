# agent_system.py
"""
RAG x Agentsシステム: 高精度な機材推薦のためのエージェントベースシステム
"""

from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json
import re
from dataclasses import dataclass

from config import GOOGLE_API_KEY
from data_loader import get_equipment_data

@dataclass
class EquipmentRecommendation:
    """機材推薦結果の構造化データ"""
    name: str
    category: str
    price: str
    characteristics: str
    match_score: float
    reason: str

class GuitarEquipmentAgent:
    """ギター機材推薦エージェント"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            max_tokens=1000
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.guitarist_options = ["B'z 松本孝弘", "布袋寅泰", "結束バンド 後藤ひとり"]
        
        # 各ギタリストの機材データベースを初期化
        self.equipment_databases = self._initialize_equipment_databases()
        
        # エージェントツールを作成
        self.tools = self._create_tools()
        
        # エージェントを初期化
        self.agent = self._create_agent()
        
    def _initialize_equipment_databases(self) -> Dict[str, Dict]:
        """ギタリスト別の機材データベースを初期化"""
        databases = {}
        
        for guitarist in self.guitarist_options:
            documents = get_equipment_data(guitarist)
            if documents:
                # FAISSベクトルストアを作成
                vectorstore = FAISS.from_documents(documents, self.embeddings)
                
                # 機材データをカテゴリ別に整理
                equipment_by_category = {"ギター": [], "アンプ": [], "エフェクター": []}
                all_equipment = []
                
                for doc in documents:
                    equipment_info = {
                        "name": doc.metadata.get("name", "N/A"),
                        "category": doc.metadata.get("category", "N/A"),
                        "price": doc.metadata.get("price", "N/A"),
                        "characteristics": doc.metadata.get("characteristics", "N/A"),
                        "content": doc.page_content
                    }
                    
                    all_equipment.append(equipment_info)
                    category = equipment_info["category"]
                    if category in equipment_by_category:
                        equipment_by_category[category].append(equipment_info)
                
                databases[guitarist] = {
                    "vectorstore": vectorstore,
                    "equipment_by_category": equipment_by_category,
                    "all_equipment": all_equipment
                }
        
        return databases
    
    def _create_tools(self) -> List[Tool]:
        """エージェントが使用するツールを作成"""
        tools = [
            Tool(
                name="search_equipment_by_category",
                func=self._search_equipment_by_category,
                description="指定されたギタリストとカテゴリで機材を検索します。入力: 'guitarist|category' (例: 'B'z 松本孝弘|ギター')"
            ),
            Tool(
                name="search_equipment_by_budget",
                func=self._search_equipment_by_budget,
                description="予算に基づいて機材を検索します。入力: 'guitarist|budget' (例: 'B'z 松本孝弘|500000')"
            ),
            Tool(
                name="analyze_sound_characteristics",
                func=self._analyze_sound_characteristics,
                description="ギタリストのサウンド特徴を分析します。入力: 'guitarist' (例: 'B'z 松本孝弘')"
            ),
            Tool(
                name="compare_equipment",
                func=self._compare_equipment,
                description="複数の機材を比較します。入力: 'guitarist|equipment_names' (例: 'B'z 松本孝弘|ギター1,ギター2')"
            ),
            Tool(
                name="calculate_total_cost",
                func=self._calculate_total_cost,
                description="推薦機材の総費用を計算します。入力: 'guitarist|equipment_names' (例: 'B'z 松本孝弘|ギター1,アンプ1')"
            ),
            Tool(
                name="semantic_search",
                func=self._semantic_search,
                description="セマンティック検索で関連機材を見つけます。入力: 'guitarist|query' (例: 'B'z 松本孝弘|ハードロック 歪み')"
            )
        ]
        return tools
    
    def _search_equipment_by_category(self, input_str: str) -> str:
        """カテゴリ別機材検索"""
        try:
            guitarist, category = input_str.split('|')
            
            if guitarist not in self.equipment_databases:
                return f"ギタリスト '{guitarist}' のデータが見つかりません。"
            
            equipment_list = self.equipment_databases[guitarist]["equipment_by_category"].get(category, [])
            
            if not equipment_list:
                return f"{guitarist}の{category}カテゴリに該当する機材が見つかりません。"
            
            result = f"{guitarist}の{category}機材一覧:\n"
            for i, eq in enumerate(equipment_list, 1):
                result += f"{i}. {eq['name']} - {eq['price']} - {eq['characteristics']}\n"
            
            return result
        
        except Exception as e:
            return f"検索エラー: {str(e)}"
    
    def _search_equipment_by_budget(self, input_str: str) -> str:
        """予算別機材検索"""
        try:
            guitarist, budget_str = input_str.split('|')
            budget = int(budget_str)
            
            if guitarist not in self.equipment_databases:
                return f"ギタリスト '{guitarist}' のデータが見つかりません。"
            
            all_equipment = self.equipment_databases[guitarist]["all_equipment"]
            budget_suitable = []
            
            for eq in all_equipment:
                # 価格文字列から数値を抽出
                price_match = re.search(r'(\d+(?:,\d+)*)', eq['price'])
                if price_match:
                    price = int(price_match.group(1).replace(',', ''))
                    if price <= budget:
                        budget_suitable.append((eq, price))
            
            if not budget_suitable:
                return f"予算{budget:,}円以内の機材が見つかりません。"
            
            # 価格順でソート
            budget_suitable.sort(key=lambda x: x[1])
            
            result = f"{guitarist}の予算{budget:,}円以内の機材:\n"
            for eq, price in budget_suitable:
                result += f"- {eq['name']} ({eq['category']}) - {price:,}円 - {eq['characteristics']}\n"
            
            return result
        
        except Exception as e:
            return f"予算検索エラー: {str(e)}"
    
    def _analyze_sound_characteristics(self, guitarist: str) -> str:
        """サウンド特徴分析"""
        sound_profiles = {
            "B'z 松本孝弘": {
                "特徴": "ハードロック、メタル、テクニカル、パワフル",
                "音色": "歪みの効いた太い音、クリアな高音域、パンチのある低音",
                "推奨要素": "ハムバッカーピックアップ、ハイゲインアンプ、ディストーション/オーバードライブ"
            },
            "布袋寅泰": {
                "特徴": "ロック、ポップス、メロディアス、エモーショナル",
                "音色": "温かみのある歪み、表現力豊かな中域、抜けの良い高音",
                "推奨要素": "シングルコイル+ハムバッカー、ビンテージ系アンプ、ディレイ/リバーブ"
            },
            "結束バンド 後藤ひとり": {
                "特徴": "オルタナティブロック、エモ、繊細、ダイナミック",
                "音色": "クリーンとドライブの使い分け、繊細な表現、空間系エフェクト",
                "推奨要素": "バランス型ピックアップ、クリーンアンプ、コーラス/ディレイ"
            }
        }
        
        if guitarist in sound_profiles:
            profile = sound_profiles[guitarist]
            result = f"{guitarist}のサウンド特徴分析:\n"
            result += f"音楽的特徴: {profile['特徴']}\n"
            result += f"音色的特徴: {profile['音色']}\n"
            result += f"推奨要素: {profile['推奨要素']}\n"
            return result
        
        return f"ギタリスト '{guitarist}' のサウンド分析データが見つかりません。"
    
    def _compare_equipment(self, input_str: str) -> str:
        """機材比較"""
        try:
            guitarist, equipment_names = input_str.split('|')
            names = [name.strip() for name in equipment_names.split(',')]
            
            if guitarist not in self.equipment_databases:
                return f"ギタリスト '{guitarist}' のデータが見つかりません。"
            
            all_equipment = self.equipment_databases[guitarist]["all_equipment"]
            found_equipment = []
            
            for eq in all_equipment:
                for name in names:
                    if name.lower() in eq['name'].lower():
                        found_equipment.append(eq)
                        break
            
            if not found_equipment:
                return f"指定された機材が見つかりません: {equipment_names}"
            
            result = f"{guitarist}の機材比較:\n"
            for i, eq in enumerate(found_equipment, 1):
                result += f"{i}. {eq['name']} ({eq['category']})\n"
                result += f"   価格: {eq['price']}\n"
                result += f"   特徴: {eq['characteristics']}\n\n"
            
            return result
        
        except Exception as e:
            return f"比較エラー: {str(e)}"
    
    def _calculate_total_cost(self, input_str: str) -> str:
        """総費用計算"""
        try:
            guitarist, equipment_names = input_str.split('|')
            names = [name.strip() for name in equipment_names.split(',')]
            
            if guitarist not in self.equipment_databases:
                return f"ギタリスト '{guitarist}' のデータが見つかりません。"
            
            all_equipment = self.equipment_databases[guitarist]["all_equipment"]
            total_cost = 0
            found_items = []
            
            for eq in all_equipment:
                for name in names:
                    if name.lower() in eq['name'].lower():
                        price_match = re.search(r'(\d+(?:,\d+)*)', eq['price'])
                        if price_match:
                            price = int(price_match.group(1).replace(',', ''))
                            total_cost += price
                            found_items.append((eq['name'], price))
                        break
            
            if not found_items:
                return f"指定された機材が見つかりません: {equipment_names}"
            
            result = f"{guitarist}の機材総費用計算:\n"
            for name, price in found_items:
                result += f"- {name}: {price:,}円\n"
            result += f"\n合計: {total_cost:,}円"
            
            return result
        
        except Exception as e:
            return f"費用計算エラー: {str(e)}"
    
    def _semantic_search(self, input_str: str) -> str:
        """セマンティック検索"""
        try:
            guitarist, query = input_str.split('|')
            
            if guitarist not in self.equipment_databases:
                return f"ギタリスト '{guitarist}' のデータが見つかりません。"
            
            vectorstore = self.equipment_databases[guitarist]["vectorstore"]
            docs = vectorstore.similarity_search(query, k=3)
            
            result = f"{guitarist}の'{query}'に関連する機材:\n"
            for i, doc in enumerate(docs, 1):
                result += f"{i}. {doc.metadata.get('name', 'N/A')}\n"
                result += f"   カテゴリ: {doc.metadata.get('category', 'N/A')}\n"
                result += f"   価格: {doc.metadata.get('price', 'N/A')}\n"
                result += f"   特徴: {doc.metadata.get('characteristics', 'N/A')}\n\n"
            
            return result
        
        except Exception as e:
            return f"セマンティック検索エラー: {str(e)}"
    
    def _create_agent(self) -> AgentExecutor:
        """ReActエージェントを作成"""
        
        prompt_template = """あなたは世界最高レベルのギター機材推薦スペシャリストです。
数十年の経験と深い音楽理論知識を持つプロフェッショナルとして、ユーザーの要求に応じて最適な機材を段階的に分析・推薦します。

## 専門知識と分析能力
- 各ギタリストの音楽的特徴とサウンドスタイルの深い理解
- 機材の音響特性と相互作用の詳細な知識
- 予算制約下での最適な機材選択の専門技術
- 演奏レベルに応じた段階的な機材提案の経験

## 利用可能なツール
{tools}

ツール名: {tool_names}

## 推薦プロセス
1. **サウンド分析**: 対象ギタリストの音楽的特徴を詳細分析
2. **機材検索**: カテゴリ別の機材データベースを検索
3. **予算最適化**: 予算制約内で最適な機材を特定
4. **相性評価**: 機材同士の相互作用と音響特性を評価
5. **総合判断**: 最適な組み合わせを選択し、詳細な推薦理由を提供

## 回答フォーマット
Question: 推薦したい内容
Thought: 何をする必要があるか考える（専門的な視点で分析）
Action: 使用するツール名
Action Input: ツールへの入力
Observation: ツールの結果
... (必要に応じて思考-アクション-観察を繰り返す)
Thought: 最終的な推薦を決定（音楽理論と実践経験に基づく判断）
Final Answer: 詳細な機材推薦結果（具体的な機材名、価格、選択理由、サウンド特性の説明を含む）

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(prompt_template)
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    def recommend_equipment(self, guitarist: str, budget: int, equipment_type: str, user_query: str) -> str:
        """機材推薦の実行"""
        
        query = f"""
        ギタリスト: {guitarist}
        予算: {budget:,}円
        機材タイプ: {equipment_type}
        ユーザーの要求: {user_query}
        
        この条件に最適な機材を推薦してください。以下の手順で分析を行ってください:
        1. ギタリストのサウンド特徴を分析
        2. 指定されたカテゴリの機材を検索
        3. 予算内の機材を特定
        4. 最適な組み合わせを選択
        5. 総費用を計算
        6. 推薦理由を説明
        
        最終的に、具体的な機材名、価格、選択理由を含む詳細な推薦結果を提供してください。
        """
        
        try:
            result = self.agent.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"推薦エラー: {str(e)}"

# 使用例とテスト用のヘルパー関数
def test_agent_system():
    """エージェントシステムのテスト"""
    agent = GuitarEquipmentAgent()
    
    # テストケース
    test_cases = [
        {
            "guitarist": "B'z 松本孝弘",
            "budget": 500000,
            "equipment_type": "ギター",
            "user_query": "ハードロックに最適なギターを推薦してください"
        }
    ]
    
    for case in test_cases:
        print(f"\n=== テストケース: {case['guitarist']} ===")
        result = agent.recommend_equipment(
            case["guitarist"],
            case["budget"],
            case["equipment_type"],
            case["user_query"]
        )
        print(result)

if __name__ == "__main__":
    test_agent_system() 