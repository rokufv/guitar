# rag_system.py

# import pysqlite3
# import sys
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 設定情報をconfig.pyからインポート
from config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHAT_MODEL, SAFETY_SETTINGS

def format_docs(docs):
    """ドキュメントをフォーマットする補助関数"""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_prompt(guitarist: str) -> ChatPromptTemplate:
    """ギタリストに応じたRAGプロンプトを生成する"""
    system_prompt = f"""あなたは{guitarist}のサウンドを熟知したギター機材の専門家です。
    ユーザーの予算と機材レベル、そして希望する機材タイプに合わせて、最適な機材を提案してください。
    提案する機材は、提供された情報（context）の中から、{guitarist}のサウンドに最も近い特徴を持つものを選び、
    その機材がなぜ{guitarist}のサウンドに近づくのか、具体的な理由とセッティングのヒントも加えて、分かりやすく解説してください。
    予算を少し超えるが、より効果的な選択肢があれば、それも提示してください。

    機材情報は以下のような形式で提供されます：
    機材名: [機材の名前]
    タイプ: [機材のタイプ]
    価格: [価格]
    レベル: [機材の難易度]
    特徴: [機材の特徴]

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
        model="gemini-pro",
        google_api_key=GOOGLE_API_KEY,
        convert_system_message_to_human=True,
        temperature=0.7
    )

    # 2. エンベッディングモデルの初期化
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    # 3. ベクトルストアの作成
    vectorstore = FAISS.from_documents(
        documents,
        embeddings,
    )

    # 4. 検索の実行
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    # 5. プロンプトテンプレートの作成
    template = """あなたは{guitarist}の機材に詳しい楽器アドバイザーです。
    以下の条件とユーザーからの質問に基づいて、{guitarist}のサウンドに近づくための機材をレコメンドしてください。

    条件：
    - 予算: {budget}円
    - 機材レベル: {level}
    - 探している機材タイプ: {type}

    以下の機材情報（コンテキスト）を参考にしてください：
    {context}

    ユーザーからの質問:
    {input}

    レコメンドする際は以下の点に気をつけてください：
    1. 予算内（{budget}円以下）で購入可能な機材を優先的に提案する
    2. ユーザーの機材レベル（{level}）に合った機材を選ぶ
    3. 指定された機材タイプ（{type}）の中から選ぶ（「すべて」の場合は制限なし）
    4. {guitarist}のサウンドの特徴と、それを実現するための機材の役割を説明する
    5. 可能であれば、予算や機材レベルに応じた代替案も提案する

    回答は日本語で、フレンドリーな口調でお願いします。
    """

    # 6. プロンプトの作成
    prompt = ChatPromptTemplate.from_template(template)
    
    # 7. RAGチェーンの作成
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    return chain