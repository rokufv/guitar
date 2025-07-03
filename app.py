# app.py

import streamlit as st
from st_audiorec import st_audiorec
import datetime
import asyncio
import os

# 自作モジュールをインポート
from config import GOOGLE_API_KEY
from data_loader import get_practice_phrase # get_equipment_dataはRAGSystem内で呼ばれる
from rag_system import RAGSystem, get_practice_advice # RAGSystemをインポート
from langchain_core.documents import Document
from pitch_analyzer import analyze_pitch_and_create_graph, compare_pitches_and_create_graph

# --- グローバルなリソースのキャッシュ ---
# @st.cache_resource # ★デバッグのため一時的にキャッシュを無効化
def load_rag_system():
    """
    RAGSystemのインスタンスをロードし、Streamlitのセッション間でキャッシュする。
    重い初期化処理（モデルロード、データ読み込み、ベクトル化）は初回のみ実行される。
    """
    return RAGSystem()

def main():
    # --- セッションステートの初期化 ---
    if 'pitch_graph' not in st.session_state:
        st.session_state.pitch_graph = None
    if 'pitch_score' not in st.session_state:
        st.session_state.pitch_score = None
    if 'practice_advice' not in st.session_state:
        st.session_state.practice_advice = None
    if 'reference_audio_path' not in st.session_state:
        st.session_state.reference_audio_path = None
    if 'reference_pitch_graph' not in st.session_state:
        st.session_state.reference_pitch_graph = None

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

    # キャッシュされたRAGシステムをロード
    try:
        rag_system = load_rag_system()
    except Exception as e:
        st.error(f"RAGシステムの初期化中にエラーが発生しました: {e}")
        st.info("Google APIキーが正しいか、またはネットワーク接続に問題がないか確認してください。")
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
            ("すべて", "ギター", "アンプ", "エフェクター"), index=0
        )
        st.markdown("---")
        
        st.markdown("#### ご予算（円）")
        budget_input = st.number_input(
            "ご希望の予算を半角数字で入力してください。",
            min_value=0, max_value=10000000, value=500000, step=100000
        )
        st.markdown("---")

    # --- メインコンテンツ ---
    st.subheader(f"{selected_guitarist} サウンド 機材レコメンド")
    st.write(f"{selected_guitarist}さんの機材とサウンドに近づくためのアドバイスを提供します。")
    st.write("ご自身の検索したい機材タイプ、そして予算を入力してください。")

    if st.button("機材をレコメンドする"):
        if budget_input <= 0:
            st.error("有効な予算を入力してください。")
        else:
            run_recommendation(rag_system, selected_guitarist, budget_input, selected_type)

    st.markdown("---")
    st.markdown("※ このアプリはプロトタイプであり、提供される情報はダミーデータとAIの推論に基づいています。")

def run_recommendation(rag_system: RAGSystem, guitarist: str, budget: int, equipment_type: str):
    """機材レコメンドを実行し、結果を表示する"""
    with st.spinner(f"{guitarist}のサウンドに近づく機材を探索中です..."):
        try:
            rag_chain = rag_system.create_rag_chain(guitarist)
            
            st.markdown("### レコメンド結果")
            
            input_data = {
                "budget": budget,
                "type": equipment_type,
                "input": f"{guitarist}のサウンドに近づきたいです。どんな機材がおすすめですか？"
            }
            
            response_data = rag_chain.invoke(input_data)

            st.markdown("#### AIからのアドバイス")

            if isinstance(response_data, dict) and 'answer' in response_data:
                st.markdown(str(response_data['answer']))
            else:
                st.markdown(str(response_data))

            st.success("機材レコメンドが完了しました！")

        except Exception as e:
            st.error(f"機材レコメンド中にエラーが発生しました: {e}")
            st.error(f"エラーの型: {e.__class__.__name__}")
            import traceback
            st.error("完全なトレースバック:")
            st.code(traceback.format_exc())
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

    # 練習フレーズの表示
    st.header("🎸 練習フレーズ")
    phrase_data = get_practice_phrase(selected_guitarist)

    if phrase_data:
        st.subheader(phrase_data["title"])

        # --- 練習セッション ---
        st.write("---")
        st.header("🎶 練習セッション")
        st.info("下の動画や分離された音源を再生して練習しましょう！\n\n**⚠️ 音が重ならないように、不要な音源はミュートしてください。**")
        
        # --- パート別音源のパス設定 ---
        # この処理は一度だけ行い、結果をセッションステートに保存する
        if not st.session_state.reference_audio_path:
            download_dir = "downloaded_audio"
            original_audio_path = None
            if os.path.exists(download_dir):
                for file in sorted(os.listdir(download_dir)):
                    if file.lower().endswith(".wav"):
                        original_audio_path = os.path.join(download_dir, file)
                        break
            
            if original_audio_path:
                original_filename_base = os.path.splitext(os.path.basename(original_audio_path))[0]
                base_path = os.path.join('separated_audio', 'htdemucs', original_filename_base)
                part_path = os.path.join(base_path, 'other.wav')
                if os.path.exists(part_path):
                    st.session_state.reference_audio_path = part_path

        # --- 練習セッションのレイアウト ---
        st.subheader("▶️ お手本動画")
        st.video(phrase_data['youtube_url'])
        
        # --- 録音セクション ---
        st.write("---")
        with st.expander("###### 🎸自分の演奏を録音＆比較分析", expanded=True):
            # まず説明を表示
            st.info("【練習の手順】\n1. 下のお手本音源の再生ボタンを押す\n2. タイミングを合わせて下の録音ボタンを押し、演奏を始める")
            st.warning("️️⚠️ **ヘッドホン・オーディオインターフェース推奨**\n\nお手本を再生しながら録音する場合は、ヘッドホンを使用しないとご自身の演奏が正しく録音されないことがあります。\n\nよりクリアな音質で録音するために、オーディオインターフェース（ギターをPCに直接接続する機材）の使用もおすすめです。")
            

            # 次に音源プレーヤー
            st.subheader("🎧 お手本ギター音源")
            if st.session_state.reference_audio_path:
                st.audio(st.session_state.reference_audio_path)
            else:
                st.warning("お手本ギター音源が見つかりません。")
            
            # 最後に録音ウィジェット
            audio_bytes = st_audiorec()
            
            if audio_bytes:
                st.audio(audio_bytes, format='audio/wav')
                
                # 比較ボタンは、お手本音源がある場合のみ表示
                if st.session_state.reference_audio_path:
                    if st.button("今の演奏を比較・分析する"):
                        with st.spinner("演奏を比較・分析し、アドバイスを生成中です..."):
                            # ピッチ比較を実行し、グラフとスコアを生成
                            fig, score = compare_pitches_and_create_graph(
                                audio_bytes, 
                                st.session_state.reference_audio_path
                            )
                            
                            # 結果をセッションステートに保存
                            st.session_state.pitch_graph = fig
                            st.session_state.pitch_score = score
                            
                            # アドバイスを非同期で取得
                            try:
                                advice = asyncio.run(get_practice_advice(float(score), selected_guitarist))
                                st.session_state.practice_advice = advice
                            except Exception as e:
                                st.session_state.practice_advice = f"アドバイスの生成中にエラーが発生しました: {e}"

                else:
                    st.warning("比較対象のお手本音源が見つからないため、比較できません。")
        
        # --- 分析結果の表示 ---
        if st.session_state.pitch_graph and st.session_state.pitch_score:
            st.markdown("---")
            st.header("📈 あなたの演奏分析結果")

            # スコアを大きく表示
            st.metric(label="類似度スコア", value=f"{st.session_state.pitch_score} / 100")

            st.pyplot(st.session_state.pitch_graph)
            st.info("青線がお手本、赤線があなたの演奏のピッチ（音の高さ）です。線が近いほど、タイミングと音程が合っていることを示します。")

            # AI講師からのアドバイス表示
            if st.session_state.practice_advice:
                st.markdown("---")
                st.subheader("🤖 AIギター講師からのワンポイントアドバイス")
                st.info(st.session_state.practice_advice)

        # タブ譜へのリンク
        if "tab_url" in phrase_data:
            st.markdown(f"---")
            st.markdown(f"[この曲のタブ譜を探す]({phrase_data['tab_url']})", unsafe_allow_html=True)

    else:
        st.info("このギタリストの練習フレーズはまだ登録されていません。")

if __name__ == "__main__":
    # session_state の初期化
    if 'audio_bytes' not in st.session_state:
        st.session_state.audio_bytes = None

    main()