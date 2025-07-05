# rag_system.py

# import pysqlite3
# import sys
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# BM25とEnsembleRetrieverを一時的に無効化
# from langchain.retrievers import BM25Retriever, EnsembleRetriever 
from langchain_core.retrievers import BaseRetriever
from typing import List, Dict
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 設定情報をconfig.pyからインポート
from config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHAT_MODEL, SAFETY_SETTINGS
from data_loader import get_equipment_data # data_loaderを直接使用

# RAG x Agentsシステムをインポート
from agent_system import GuitarEquipmentAgent

def format_docs(docs: List[Document]) -> str:
    """ドキュメントをフォーマットする補助関数"""
    return "\n\n".join(doc.page_content for doc in docs)

class RAGSystem:
    """
    機材推薦のためのRAGシステム全体を管理するクラス。
    重い初期化処理を一度だけ行い、キャッシュして使用されることを想定。
    v2.0: RAG x Agentsシステムを統合
    """
    def __init__(self):
        self.version = "2.0"  # RAG x Agentsシステム統合版
        # print(f"RAGSystemの初期化を開始します v{self.version} ... (この処理は起動時に一度だけ実行されます)")
        self.guitarist_options = ["B'z 松本孝弘", "布袋寅泰", "結束バンド 後藤ひとり"]
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.5,
            max_tokens=300,  # 応答長を制限して高速化
            timeout=10  # タイムアウトを短縮
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
        self.retrievers_by_guitarist = self._initialize_all_retrievers()
        
        # RAG x Agentsシステムを初期化
        self.agent_system = GuitarEquipmentAgent()
        # print(f"RAGSystem v{self.version} の初期化が完了しました。")

    def _create_retriever(self, documents: List[Document]) -> BaseRetriever:
        """【デバッグ用】FAISS Retrieverのみを構築する"""
        if not documents:
            class EmptyRetriever(BaseRetriever):
                def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]: return []
            return EmptyRetriever()

        # FAISSによるセマンティック検索のみを行う
        return FAISS.from_documents(documents, self.embeddings).as_retriever(search_kwargs={"k": 5})

    def _initialize_all_retrievers(self) -> Dict[str, Dict[str, BaseRetriever]]:
        """
        全ギタリストのデータを読み込み、カテゴリ別にリトリーバーを構築する。
        """
        all_retrievers = {}
        for guitarist in self.guitarist_options:
            documents = get_equipment_data(guitarist)

            # --- データ検証ステップを追加 ---
            for i, doc in enumerate(documents):
                if not isinstance(doc.page_content, str):
                    error_msg = (
                        f"データ検証エラー: ギタリスト '{guitarist}' のデータに問題があります。\n"
                        f"ドキュメントNo.{i} の page_content が文字列ではなく、{type(doc.page_content)} 型になっています。\n"
                        f"問題のデータ内容: {doc.page_content}\n"
                        f"data_loader.py または元のデータファイルを確認してください。"
                    )
                    raise TypeError(error_msg)
            # --- データ検証ここまで ---
            
            chunked_documents = self.text_splitter.split_documents(documents)
            
            docs_by_category: Dict[str, List[Document]] = {"ギター": [], "アンプ": [], "エフェクター": []}
            for doc in chunked_documents:
                category = doc.metadata.get("category")
                if category in docs_by_category:
                    docs_by_category[category].append(doc)
            docs_by_category["すべて"] = chunked_documents

            guitarist_retrievers = {
                # デバッグ用に単純化されたRetriever作成関数を呼ぶ
                category: self._create_retriever(docs)
                for category, docs in docs_by_category.items()
            }
            all_retrievers[guitarist] = guitarist_retrievers
            # print(f"  - {guitarist} のリトリーバーを構築しました。")
        return all_retrievers

    def create_rag_chain(self, guitarist: str, use_agent: bool = False):
        """
        機材推薦チェーンを作成する。
        
        Args:
            guitarist: 対象ギタリスト名
            use_agent: エージェントベースの推薦を使用するかどうか
        """
        if use_agent:
            # エージェントベースの推薦を使用
            def run_agent_recommendation(input_dict: dict) -> dict:
                try:
                    budget = input_dict.get("budget", 500000)
                    equipment_type = input_dict.get("type", "すべて")
                    user_query = input_dict.get("input", f"{guitarist}のサウンドに近づく機材を推薦してください")
                    
                    # エージェントシステムを使用して推薦を実行
                    answer_str = self.agent_system.recommend_equipment(
                        guitarist, budget, equipment_type, user_query
                    )
                    
                    return {
                        "answer": answer_str,
                        "context": f"エージェントベースの詳細分析による推薦結果",
                        "method": "agent_based"
                    }
                except Exception as e:
                    return {
                        "answer": f"エージェントベースの推薦中にエラーが発生しました: {str(e)}",
                        "context": "エラーが発生したため、標準的な推薦にフォールバックしました。",
                        "method": "error_fallback"
                    }
            
            return RunnableLambda(run_agent_recommendation)
        
        else:
            # 従来の簡潔な推薦を使用
            template = """{guitarist}のサウンドに近づくための機材推薦をします。

**予算:** {budget}円
**機材タイプ:** {type}

## 推薦機材（上位3つ）
1. **機材名** - 価格帯・特徴（1行）
2. **機材名** - 価格帯・特徴（1行）  
3. **機材名** - 価格帯・特徴（1行）

## 一言アドバイス
{guitarist}らしいサウンドを作るポイントを2行で簡潔に。

簡潔に回答してください。"""
            prompt = ChatPromptTemplate.from_template(template)

            # LLMに応答を生成させる部分のチェーン
            llm_chain = prompt | self.llm | StrOutputParser()

            def run_llm_chain_only(input_dict: dict) -> dict:
                """
                データ検索を完全にバイパスし、LLMチェーンのみを実行する。
                """
                # LLMチェーンへの入力を準備
                llm_input = {
                    "guitarist": guitarist,
                    "budget": input_dict.get("budget", "指定なし"),
                    "type": input_dict.get("type", "指定なし"),
                    "input": input_dict.get("input", ""),
                    "context": "これは固定のコンテキスト情報です。データベースからの検索は行われていません。"
                }
                # LLMチェーンを実行して回答文字列を取得
                answer_str = llm_chain.invoke(llm_input)
                
                # app.pyが期待する形式で辞書を返す
                return {"answer": answer_str, "context": llm_input["context"], "method": "simple"}

            # 複雑なチェーンの代わりに、単純なPython関数をRunnableとして返す
            return RunnableLambda(run_llm_chain_only)

async def get_practice_advice(score: float, guitarist: str) -> str:
    """
    演奏のスコアとギタリスト名に基づき、ギター講師としてのアドバイスを生成する。
    """
    if score >= 95: rank, feedback = "S (素晴らしい！)", "ほぼ完璧な演奏です！プロレベルの精度に達しています。"
    elif score >= 80: rank, feedback = "A (上手い！)", "非常に上手な演奏です。細かいニュアンスまで再現できています。"
    elif score >= 60: rank, feedback = "B (良い感じ！)", "良い演奏です！あと少しでさらに良くなります。"
    elif score >= 40: rank, feedback = "C (もう一息！)", "惜しい！フレーズの要点は掴めています。"
    else: rank, feedback = "D (要練習)", "基本からもう一度確認してみましょう。"

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.6,
        max_tokens=200,  # 応答長を制限
        timeout=8  # タイムアウトを短縮
    )
    
    prompt_template = f"""ギター講師として{guitarist}風演奏のアドバイスをします。

**演奏結果:** {score:.1f}点 ({rank})
{feedback}

## 良かった点
（1行で具体的に褒める）

## 改善ポイント  
1. （技術的改善点を1行で）
2. （練習方法を1行で）

## 次回への励まし
（{guitarist}らしい演奏に近づくための前向きなメッセージを2行で）

簡潔にお願いします。"""
    try:
        response = await llm.ainvoke(prompt_template)
        return response.content if isinstance(response.content, str) else str(response.content)
    except Exception as e:
        print(f"Error getting practice advice: {e}")
        return "アドバイスの生成中にエラーが発生しました。しばらくしてからもう一度お試しください。"