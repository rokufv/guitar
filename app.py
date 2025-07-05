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
@st.cache_resource  # ★キャッシュを有効化してパフォーマンス改善
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
    
    # RAGシステムの初期化状態を管理
    if 'rag_system_loaded' not in st.session_state:
        st.session_state.rag_system_loaded = False

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

    # キャッシュされたRAGシステムをロード（初回のみ初期化メッセージを表示）
    try:
        if not st.session_state.rag_system_loaded:
            with st.spinner("RAGシステムを初期化中...（初回のみ）"):
                rag_system = load_rag_system()
                st.session_state.rag_system_loaded = True
                # st.success("RAGシステムの初期化が完了しました！")
        else:
            rag_system = load_rag_system()  # キャッシュから高速取得
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
        
        st.markdown("#### 推薦システム選択")
        use_agent = st.checkbox(
            "🤖 AIエージェント推薦を使用",
            value=True,
            help="より詳細な分析と段階的な推薦を行います（推薦品質向上・処理時間増加）"
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
            run_recommendation(rag_system, selected_guitarist, budget_input, selected_type, use_agent)

    st.markdown("---")
    st.markdown("※ このアプリはプロトタイプであり、提供される情報はダミーデータとAIの推論に基づいています。")

def run_recommendation(rag_system: RAGSystem, guitarist: str, budget: int, equipment_type: str, use_agent: bool = False):
    """機材レコメンドを実行し、結果を表示する"""
    
    # エージェントシステムの場合は異なるスピナーメッセージを表示
    if use_agent:
        spinner_message = f"🤖 AIエージェントが{guitarist}のサウンドを詳細分析中です...\n（段階的な推薦プロセスを実行中）"
    else:
        spinner_message = f"{guitarist}のサウンドに近づく機材を探索中です..."
    
    with st.spinner(spinner_message):
        try:
            rag_chain = rag_system.create_rag_chain(guitarist, use_agent=use_agent)
            
            st.markdown("### レコメンド結果")
            
            input_data = {
                "budget": budget,
                "type": equipment_type,
                "input": f"{guitarist}のサウンドに近づきたいです。どんな機材がおすすめですか？"
            }
            
            response_data = rag_chain.invoke(input_data)

            # 推薦方法を表示
            if isinstance(response_data, dict) and 'method' in response_data:
                method = response_data['method']
                if method == "agent_based":
                    st.info("🤖 AIエージェントによる高精度推薦結果")
                elif method == "simple":
                    st.info("⚡ 高速推薦結果")
                elif method == "error_fallback":
                    st.warning("⚠️ エラー発生のため標準推薦にフォールバック")

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
        # 選択されたギタリストに応じて適切な音源を選択
        download_dir = "downloaded_audio"
        reference_audio_path = None
        
        # ギタリスト別の音源検索パターン
        guitarist_search_patterns = {
            "B'z 松本孝弘": "*ultra*",
            "布袋寅泰": "*スリル*",
            "結束バンド 後藤ひとり": "*忘れてやらない*"
        }
        
        # 選択されたギタリストの音源を動的に探す
        search_pattern = guitarist_search_patterns.get(selected_guitarist)
        if search_pattern:
            import glob
            pattern = os.path.join('separated_audio', 'htdemucs', search_pattern, 'other.wav')
            matching_files = glob.glob(pattern)
            if matching_files:
                reference_audio_path = matching_files[0]
        
        # セッションステートに保存（ギタリスト変更時に更新されるよう）
        st.session_state.reference_audio_path = reference_audio_path

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
            st.markdown("#### 🎤 あなたの演奏を録音してください")
            st.info("**💡 クリアな録音のための手順:**\n1. **推奨方法**: お手本音源を聞いて覚える → 音源を停止 → 録音開始\n2. **同時録音する場合**: 有線ヘッドホン必須 + 音源音量を最小に\n3. **最高品質**: オーディオインターフェース使用")
            st.warning("⚠️ **重要**: お手本音源と同時録音すると、ブラウザのエコーキャンセレーション機能により音質が劣化する場合があります。最もクリアな録音には、音源を停止してから録音することをお勧めします。")
            
            # 録音方法の選択
            recording_method = st.radio(
                "録音方法を選択してください：",
                ("🎤 ブラウザで直接録音", "📁 録音ファイルをアップロード"),
                help="音質に問題がある場合は、外部アプリで録音してアップロードをお試しください"
            )
            
            audio_bytes = None
            if recording_method == "🎤 ブラウザで直接録音":
                audio_bytes = st_audiorec()
            else:
                uploaded_file = st.file_uploader(
                    "録音ファイルをアップロードしてください",
                    type=['wav', 'mp3', 'ogg', 'm4a'],
                    help="Audacity、GarageBand、スマホの録音アプリなどで録音したファイルをアップロードできます"
                )
                if uploaded_file is not None:
                    audio_bytes = uploaded_file.read()
            
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