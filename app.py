# app.py

import streamlit as st
from st_audiorec import st_audiorec
import datetime
import asyncio

# 自作モジュールをインポート
from config import GOOGLE_API_KEY
from data_loader import get_equipment_data, get_practice_phrase
from rag_system import create_rag_chain
from langchain_core.documents import Document

def main():
    # --- タブの設定 ---
    tab1, tab2 = st.tabs(["🎸 機材レコメンド", "🎤 フレーズ練習"])

    with tab1:
        run_recommendation_mode()

    with tab2:
        run_practice_mode()

def run_recommendation_mode():
    """機材レコメンドモードのUIとロジック"""
    st.title("🎸 貴方の音になりたくて…機材編")

    # APIキーの存在チェック
    if not GOOGLE_API_KEY:
        st.error("環境変数 'GOOGLE_API_KEY' が設定されていません。'.env' ファイルを確認するか、環境変数に設定してください。")
        st.stop()

    # --- サイドバー (ユーザー入力) ---
    with st.sidebar:
        st.markdown("### 目指すギタリストを選択")
        guitarist_options = ["B'z 松本孝弘", "布袋寅泰", "結束バンド 後藤ひとり"]
        selected_guitarist = st.radio(
            "どのギタリストのサウンドを目指しますか？",
            guitarist_options, index=0
        )
        st.markdown("---")
        
        st.markdown("#### 検索したい機材タイプ")
        selected_type = st.radio(
            "どの機材カテゴリで探しますか？",
            ("すべて", "ギター", "アンプ", "エフェクター", "ピック"), index=0
        )
        st.markdown("---")
        
        st.markdown("#### ご予算（円）")
        budget_input = st.number_input(
            "ご希望の予算を半角数字で入力してください。",
            min_value=0, max_value=1000000, value=50000, step=10000
        )
        st.markdown("---")
        
        st.markdown("#### 機材レベル")
        selected_level = st.selectbox(
            "あなたの機材レベルは？",
            ["初級", "中級", "上級"], index=0
        )
        st.markdown("---")

    # --- メインコンテンツ ---
    st.subheader(f"{selected_guitarist} サウンド 機材レコメンド")
    st.write(f"{selected_guitarist}さんの機材とサウンドに近づくためのアドバイスを提供します。")
    st.write("ご自身の機材レベルと検索したい機材タイプ、そして予算を入力してください。")

    if st.button("機材をレコメンドする"):
        if budget_input <= 0:
            st.error("有効な予算を入力してください。")
        else:
            run_recommendation(selected_guitarist, selected_level, budget_input, selected_type)

    st.markdown("---")
    st.markdown("※ このアプリはプロトタイプであり、提供される情報はダミーデータとAIの推論に基づいています。")

def run_recommendation(guitarist, level, budget, type):
    """機材レコメンドを実行し、結果を表示する"""
    with st.spinner(f"{guitarist}のサウンドに近づく機材を探索中です..."):
        try:
            equipment_data = get_equipment_data(guitarist)
            if not equipment_data:
                st.error(f"{guitarist}の機材データが見つかりませんでした。")
                return

            rag_chain = create_rag_chain(equipment_data, guitarist)
            
            st.markdown("### レコメンド結果")
            
            input_data = {
                "guitarist": guitarist,
                "level": level,
                "budget": budget,
                "type": type,
                "input": f"{guitarist}のサウンドに近づきたいです。どんな機材がおすすめですか？"
            }
            
            # 非同期関数を同期的に実行
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(rag_chain.ainvoke(input_data))
            loop.close()

            # おすすめ機材（Context）を表示
            if "context" in result and result["context"]:
                st.markdown("#### おすすめの機材はこちら！")
                for doc in result["context"]:
                    with st.expander(f"{doc.metadata.get('name', 'N/A')}", expanded=True):
                        if doc.metadata.get("image_url"):
                            st.image(doc.metadata["image_url"])
                        
                        st.markdown(f"**タイプ**: {doc.metadata.get('type', 'N/A')}")
                        st.markdown(f"**価格**: {doc.metadata.get('price', 'N/A')}")
                        st.markdown(f"**レベル**: {doc.metadata.get('level', 'N/A')}")
                        st.markdown(f"**特徴**: {doc.metadata.get('characteristics', 'N/A')}")
                st.markdown("---")

            # AIからのアドバイス（Answer）を表示
            if "answer" in result:
                st.markdown("#### AIからのアドバイス")
                st.markdown(result["answer"])

            st.success("機材レコメンドが完了しました！")

        except Exception as e:
            st.error(f"機材レコメンド中にエラーが発生しました: {e}")
            st.warning("Gemini APIキーが正しく設定されているか、インターネット接続を確認してください。")

def run_practice_mode():
    """フレーズ練習モードのUIとロジック"""
    st.title("🎸 貴方の音になりたくて…演奏編")

    st.sidebar.markdown("### 練習したいギタリストを選択")
    guitarist_options = ["B'z 松本孝弘", "布袋寅泰", "結束バンド 後藤ひとり"]
    selected_guitarist = st.sidebar.radio(
        "どのギタリストのフレーズを練習しますか？",
        guitarist_options, index=0, key="practice_guitarist"
    )

    phrase_data = get_practice_phrase(selected_guitarist)

    if phrase_data:
        st.subheader(f"{selected_guitarist} - {phrase_data['title']}")

        # サウンドチェック ボタンでマイク録音
        st.markdown("#### 🎤 サウンドチェック")
        st.write("録音ボタンを押して、あなたの演奏を録音・確認できます。")
        audio_bytes = st_audiorec()
        if audio_bytes is not None:
            st.audio(audio_bytes, format='audio/wav')
            
            # 保存機能（オプション）
            now = datetime.datetime.now()
            filename = f"sound_check_{now.strftime('%Y%m%d_%H%M%S')}.wav"
            if st.button("録音を保存"):
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                st.success(f"録音を{filename}として保存しました。")


        # レッツプレイ！ ボタンでYouTube再生
        if "youtube_url" in phrase_data:
            st.markdown("---")
            st.markdown("#### 🎶 レッツプレイ！")
            st.write("下の動画に合わせて演奏してみましょう！")
            st.video(phrase_data['youtube_url'])
        
        # タブ譜へのリンク
        if "tab_url" in phrase_data:
            st.markdown(f"[この曲のタブ譜を探す]({phrase_data['tab_url']})", unsafe_allow_html=True)
            
    else:
        st.info("このギタリストの練習フレーズはまだ登録されていません。")

if __name__ == "__main__":
    main()