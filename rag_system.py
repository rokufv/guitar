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

def format_docs(docs: List[Document]) -> str:
    """ドキュメントをフォーマットする補助関数"""
    return "\n\n".join(doc.page_content for doc in docs)

class RAGSystem:
    """
    機材推薦のためのRAGシステム全体を管理するクラス。
    重い初期化処理を一度だけ行い、キャッシュして使用されることを想定。
    """
    def __init__(self):
        self.version = "1.4" # デバッグ用のバージョン情報
        print(f"RAGSystemの初期化を開始します v{self.version} ... (この処理は起動時に一度だけ実行されます)")
        self.guitarist_options = ["B'z 松本孝弘", "布袋寅泰", "結束バンド 後藤ひとり"]
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
        self.retrievers_by_guitarist = self._initialize_all_retrievers()
        print(f"RAGSystem v{self.version} の初期化が完了しました。")

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
            print(f"  - {guitarist} のリトリーバーを構築しました。")
        return all_retrievers

    def create_rag_chain(self, guitarist: str):
        """
        【最終デバッグ】データ検索部をバイパスし、問題箇所を特定する。
        """
        # 見やすく、端的な出力を指示するプロンプト
        template = """あなたは、ユーザーが目指すギタリストのサウンドに近づくための機材を推薦する、プロの楽器アドバイザーです。
        以下の情報に基づき、回答は非常に明瞭で、見やすく、そして端的にまとめてください。

        ---
        ### ユーザー情報
        - **目標のギタリスト:** {guitarist}
        - **探している機材:** {type}
        - **予算:** {budget}円

        ### 参考機材データ (コンテキスト)
        【デバッグモード】現在、データベース検索はバイパスされています。
        {context}
        ---

        ### 回答の構成案
        1.  **タイトル:** 「{guitarist}風サウンドへの推薦機材」のような、一目で内容がわかるタイトルを付けてください。
        2.  **推薦機材リスト:**
            - コンテキストから、ユーザーの予算と希望に最も合う機材を**最大3つまで**選び、以下の形式で箇条書きにしてください。
            - **【機材名】** (カテゴリ)
              - **価格相場:** (価格)
              - **ポイント:** (なぜその機材が推薦できるのか、サウンドの特徴などを**1〜2行で要約**)
        3.  **総括アドバイス:**
            - なぜこれらの機材を選んだのか、そして予算内でどのように組み合わせると効果的かなどを、**3〜4行程度の短い文章で**アドバイスしてください。

        以上の構成案に従って、プロフェッショナルかつ親切な口調で回答を生成してください。
        """
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
            return {"answer": answer_str, "context": llm_input["context"]}

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

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)
    
    prompt_template = f"""あなたは、{guitarist}のプレイスタイルとサウンドを熟知した、経験豊富なプロのギター講師です。
    生徒の演奏を採点し、具体的な改善点を非常に分かりやすく、そしてモチベーションが上がるようにアドバイスします。
    今回は、生徒が{guitarist}のフレーズに挑戦した結果、以下の評価が出ました。
    ---
    採点結果: {score:.1f}点 / 100点, 評価ランク: {rank}, 講師からの一言: {feedback}
    ---
    この評価結果を踏まえて、生徒が{guitarist}のサウンドと演奏にさらに近づくための、具体的で実践的なアドバイスをしてください。
    アドバイスに含めるべきポイント：
    1. まず、生徒の演奏の良かった点を具体的に褒めて、モチベーションを高めてください。
    2. 次に、改善すべき点を、音楽理論やテクニック（例：ピッキング、ビブラート、リズム感、音の強弱など）に基づいて、{guitarist}の演奏の特徴と関連付けながら、最大2つまで、分かりやすく指摘してください。
    3. 最後に、今後の練習方法や意識すべきことを具体的に提案し、生徒を力強く励ますポジティブなメッセージで締めくくってください。
    回答は、フレンドリーかつ尊敬の念を込めた、プロのギター講師らしい口調でお願いします。
    """
    try:
        response = await llm.ainvoke(prompt_template)
        return response.content if isinstance(response.content, str) else str(response.content)
    except Exception as e:
        print(f"Error getting practice advice: {e}")
        return "アドバイスの生成中にエラーが発生しました。しばらくしてからもう一度お試しください。"