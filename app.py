# app.py

import streamlit as st
from st_audiorec import st_audiorec
import datetime

# 自作モジュールをインポート
from data_loader import get_equipment_data
from rag_system import create_rag_chain
import asyncio

def main():
    # --- タブの設定 ---
    tab1, tab2 = st.tabs(["機材レコメンド", "録音"])

    # タブ1: 機材レコメンド
    with tab1:
        st.title("ギター機材レコメンドシステム")
        
        # ギタリストの選択
        guitarist = st.selectbox(
            "参考にしたいギタリストを選択してください",
            ["HOTEI", "TAK", "GOTOH"]
        )
        
        # 予算の入力
        budget = st.number_input(
            "予算を入力してください（円）",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000
        )
        
        # 機材レベルの選択
        level = st.selectbox(
            "希望する機材レベルを選択してください",
            ["初心者向け", "中級者向け", "上級者向け"]
        )
        
        # 機材タイプの選択
        equipment_type = st.selectbox(
            "探している機材のタイプを選択してください",
            ["すべて", "ギター", "アンプ", "エフェクター", "その他"]
        )
        
        # レコメンドボタン
        if st.button("レコメンド"):
            try:
                # 機材データの取得
                documents = get_equipment_data(guitarist)
                if not documents:
                    st.error(f"{guitarist}の機材データが見つかりませんでした。")
                    return
                
                # RAGチェーンの作成
                chain = create_rag_chain(documents, guitarist)
                
                # 入力データの準備
                input_data = {
                    "budget": budget,
                    "level": level,
                    "type": equipment_type
                }
                
                # プログレスバーの表示
                with st.spinner("機材をレコメンド中..."):
                    # 非同期関数を同期的に実行
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(chain(input_data))
                    loop.close()
                
                # レコメンド結果の表示
                st.write("### レコメンド結果")
                st.write(response)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
    
    # タブ2: 録音機能
    with tab2:
        st.title("録音")
        st.write("録音ボタンを押して、あなたの演奏を録音してください。")
        
        # 録音の実行
        wav_audio_data = st_audiorec()
        
        if wav_audio_data is not None:
            # 現在の日時を取得
            now = datetime.datetime.now()
            filename = now.strftime("%Y%m%d_%H%M%S") + ".wav"
            
            # 録音データの保存
            st.write("録音が完了しました！")
            st.audio(wav_audio_data, format='audio/wav')

if __name__ == "__main__":
    main()