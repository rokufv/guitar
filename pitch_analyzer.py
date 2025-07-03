import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import io
from dtw import dtw

def _extract_pitch(audio_source, is_path=False):
    """
    音声ソースからピッチ(f0)と時間(times)を抽出する内部関数。
    sr=Noneでファイルのネイティブなサンプルレートを自動検出して使用する。
    """
    try:
        # ネイティブなサンプルレートで音声を読み込む
        y, sr = librosa.load(audio_source, sr=None)

        # pYINアルゴリズムでピッチを推定
        # hop_lengthはpyinのデフォルト値(win_length/4 = 2048/4 = 512)
        f0, voiced_flag, _ = librosa.pyin(
            y,
            fmin=librosa.note_to_hz('E2'),
            fmax=librosa.note_to_hz('E6'),
            sr=sr # 検出したsrを使用
        )
        
        # 正しいサンプルレートとホップ長で時間軸を生成
        times = librosa.times_like(f0, sr=sr, hop_length=512)
        
        # 有声区間のみを返す
        voiced_indices = np.where(voiced_flag)
        return f0[voiced_indices], times[voiced_indices]
        
    except Exception as e:
        print(f"Error extracting pitch: {e}")
        return None, None

def analyze_pitch_and_create_graph(audio_bytes):
    """
    単一のオーディオデータからピッチを抽出し、グラフを生成する。
    """
    f0, times = _extract_pitch(io.BytesIO(audio_bytes))
    
    if f0 is None or times is None:
        return None

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, f0, 'o', markersize=2, label='Pitch (f0)')
    ax.set_title('Pitch Analysis')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f"{int(x)}"))
    
    # ギターの開放弦の周波数を参考にグリッド表示
    E2 = librosa.note_to_hz('E2'); A2 = librosa.note_to_hz('A2'); D3 = librosa.note_to_hz('D3'); G3 = librosa.note_to_hz('G3'); B3 = librosa.note_to_hz('B3'); E4 = librosa.note_to_hz('E4')
    ax.axhline(y=E2, color='r', linestyle='--', linewidth=0.5, label='E2'); ax.axhline(y=A2, color='g', linestyle='--', linewidth=0.5, label='A2'); ax.axhline(y=D3, color='b', linestyle='--', linewidth=0.5, label='D3'); ax.axhline(y=G3, color='c', linestyle='--', linewidth=0.5, label='G3'); ax.axhline(y=B3, color='m', linestyle='--', linewidth=0.5, label='B3'); ax.axhline(y=E4, color='y', linestyle='--', linewidth=0.5, label='E4')
    
    ax.legend(loc='upper right')
    ax.grid(True, which="both", ls="--", linewidth=0.5)
    plt.tight_layout()
    return fig

def compare_pitches_and_create_graph(user_audio_bytes, reference_audio_path):
    """
    ユーザーの演奏とお手本演奏のピッチを比較し、グラフとスコアを生成する。
    """
    user_f0, user_times = _extract_pitch(io.BytesIO(user_audio_bytes))
    ref_f0, ref_times = _extract_pitch(reference_audio_path, is_path=True)

    if user_f0 is None or ref_f0 is None or len(user_f0) == 0 or len(ref_f0) == 0:
        return None, "ピッチを抽出できませんでした。もう一度録音してみてください。"

    user_midi = librosa.hz_to_midi(user_f0)
    ref_midi = librosa.hz_to_midi(ref_f0)
    
    # DTWの実行
    # お手本(query)を基準に、ユーザー演奏(reference)をアライメントする
    # これにより、お手本の全区間に対してユーザー演奏がマッピングされる
    alignment = dtw(ref_midi, user_midi, keep_internals=True, open_begin=True, open_end=True, step_pattern='asymmetric')

    score = alignment.normalizedDistance
    
    # 100点満点に変換し、0点未満にならないようにする
    similarity_score = max(0, 100 - score * 100)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # ワーピングパスを取得
    wp_ref = alignment.index1  # query (ref) のインデックス
    wp_user = alignment.index2 # reference (user) のインデックス
    
    # 1. お手本演奏のピッチを、ワーピング後の時間軸でプロット
    # これにより、X軸がお手本の時間全体に広がる
    ax.plot(ref_times[wp_ref], ref_midi[wp_ref], 'o-', label='Reference Pitch', color='dodgerblue', markersize=3)
    
    # 2. ユーザーの演奏を、同じワーピング後のお手本の時間軸でプロット
    ax.plot(ref_times[wp_ref], user_midi[wp_user], 'o-', label='Your Pitch', color='tomato', markersize=3, alpha=0.7)

    ax.set_title(f'Pitch Comparison (Similarity Score: {similarity_score:.1f} / 100)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pitch (MIDI Note Number)')
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)

    @plt.FuncFormatter
    def midi_formatter(x, pos):
        return librosa.midi_to_note(x)
    ax.yaxis.set_major_formatter(midi_formatter)

    plt.tight_layout()

    return fig, f"{similarity_score:.1f}" 