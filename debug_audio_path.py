import os
import glob

def debug_audio_path():
    """松本孝弘のお手本音源のパス解決をデバッグする"""
    
    print("=== 松本孝弘のお手本音源パス解決デバッグ ===")
    
    # アプリで使用されているマッピング
    guitarist_audio_mapping = {
        "B'z 松本孝弘": "【TAB譜】ultra soul(ウルトラソウル)／B'z／ギターイントロ演奏動画",
        "布袋寅泰": "[TAB譜] スリル⧸布袋寅泰 Guitar solo [ギター]",
        "結束バンド 後藤ひとり": "【TAB】忘れてやらない(Wasurete Yaranai) ⧸ 結束バンド(Kessoku Band)【ギターソロ】"
    }
    
    selected_guitarist = "B'z 松本孝弘"
    target_filename = guitarist_audio_mapping.get(selected_guitarist)
    
    print(f"選択されたギタリスト: {selected_guitarist}")
    print(f"マッピングされたファイル名: {target_filename}")
    
    # パス構築
    base_path = os.path.join('separated_audio', 'htdemucs', target_filename)
    part_path = os.path.join(base_path, 'other.wav')
    
    print(f"構築されたベースパス: {base_path}")
    print(f"構築された音源パス: {part_path}")
    print(f"ベースパス存在: {os.path.exists(base_path)}")
    print(f"音源パス存在: {os.path.exists(part_path)}")
    
    # 実際のディレクトリ構造を確認
    print("\n=== 実際のディレクトリ構造 ===")
    htdemucs_path = 'separated_audio/htdemucs'
    if os.path.exists(htdemucs_path):
        for item in os.listdir(htdemucs_path):
            item_path = os.path.join(htdemucs_path, item)
            if os.path.isdir(item_path):
                print(f"ディレクトリ: {item}")
                if 'ultra' in item.lower():
                    print(f"  -> ultra関連ディレクトリ発見!")
                    other_wav = os.path.join(item_path, 'other.wav')
                    print(f"  -> other.wav存在: {os.path.exists(other_wav)}")
                    if os.path.exists(other_wav):
                        print(f"  -> ファイルサイズ: {os.path.getsize(other_wav)} bytes")
    
    # グロブパターンで検索
    print("\n=== グロブパターン検索 ===")
    pattern = 'separated_audio/htdemucs/*ultra*/other.wav'
    files = glob.glob(pattern)
    print(f"パターン: {pattern}")
    print(f"見つかったファイル: {files}")
    
    if files:
        actual_path = files[0]
        print(f"実際のパス: {actual_path}")
        
        # パスの違いを分析
        expected_dir = target_filename
        actual_dir = os.path.basename(os.path.dirname(actual_path))
        
        print(f"\n=== パス比較 ===")
        print(f"期待されるディレクトリ名: '{expected_dir}'")
        print(f"実際のディレクトリ名: '{actual_dir}'")
        print(f"一致: {expected_dir == actual_dir}")
        
        if expected_dir != actual_dir:
            print("\n🚨 問題発見: ディレクトリ名が一致しません!")
            print("解決策: app.pyのマッピングを実際のディレクトリ名に修正する必要があります")
            print(f"修正案: '{actual_dir}'")

if __name__ == "__main__":
    debug_audio_path() 