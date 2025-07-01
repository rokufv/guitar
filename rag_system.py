# rag_system.py

# import pysqlite3
# import sys
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# 設定情報をconfig.pyからインポート
from config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHAT_MODEL, SAFETY_SETTINGS

def create_rag_prompt(guitarist: str) -> ChatPromptTemplate:
    """ギタリストに応じたRAGプロンプトを生成する"""
    system_prompt = f"""あなたは{guitarist}のサウンドを熟知したギター機材の専門家です。
    ユーザーの予算と機材レベル、そして希望する機材タイプに合わせて、最適な機材を提案してください。
    提案する機材は、提供された情報（context）の中から、{guitarist}のサウンドに最も近い特徴を持つものを選び、
    その機材がなぜ{guitarist}のサウンドに近づくのか、具体的な理由とセッティングのヒントも加えて、分かりやすく解説してください。
    予算を少し超えるが、より効果的な選択肢があれば、それも提示してください。
    以下の情報を参考にして提案してください:
    {{context}}
    """
    
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"{guitarist}のサウンドに近づきたいです。\n機材レベル: {{level}}\n予算: {{budget}}円\n機材タイプ: {{type}}\nどんな機材がおすすめですか？"),
    ])

def create_rag_chain(documents: list[Document], guitarist: str):
    """ドキュメントとギタリスト名からRAGチェーンを構築する"""
    # 1. LLMの初期化
    llm = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        temperature=0.5,
        safety_settings=SAFETY_SETTINGS,
        google_api_key=GOOGLE_API_KEY,
        max_output_tokens=1024
    )

    # 2. 埋め込みモデルの初期化
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY)

    # 3. ベクトルストアの作成
    vectorstore = Chroma.from_documents(documents, embeddings)

    # 4. 検索器の作成
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # 5. プロンプトの作成
    prompt = create_rag_prompt(guitarist)

    # 6. チェーンの構築
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain