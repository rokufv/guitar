import os
import subprocess

def separate_audio(input_file_path, output_path='separated_audio'):
    """
    demucs を使用して音声ファイルを「ボーカル」と「伴奏」の2つに分離する。

    :param input_file_path: 分離する音声ファイルのパス
    :param output_path: 分離されたファイルを保存するディレクトリ
    """
    if not os.path.exists(input_file_path):
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
        return

    # demucsコマンドを組み立てる
    # --out: 出力ディレクトリ指定
    # 4ステム(vocals, drums, bass, other)に分離する
    # 仮想環境のPythonを使用
    command = [
        'env/bin/python', '-m', 'demucs',
        '--out', output_path,
        input_file_path
    ]

    print(f"'{input_file_path}' の音源分離を開始します (demucs, 4-stems)...")

    try:
        # demucs をサブプロセスとして実行
        # stdoutとstderrをキャプチャして、より詳細な情報を表示
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("----- エラー出力 -----")
            print(result.stderr)
        print(f"音源分離が完了しました。ファイルは '{output_path}' に保存されています。")

    except subprocess.CalledProcessError as e:
        print(f"demucsの実行中にエラーが発生しました。")
        print(f"コマンド: {' '.join(e.cmd)}")
        print(f"終了コード: {e.returncode}")
        print("----- 標準出力 -----")
        print(e.stdout)
        print("----- 標準エラー出力 -----")
        print(e.stderr)
    except FileNotFoundError:
        print("エラー: 'python -m demucs' コマンドが見つかりません。demucsが正しくインストールされているか確認してください。")


if __name__ == '__main__':
    download_dir = "downloaded_audio"
    input_audio_file = None

    # downloaded_audio ディレクトリ内の最初の .wav ファイルを探す
    if os.path.exists(download_dir):
        for file in os.listdir(download_dir):
            if file.lower().endswith(".wav"):
                input_audio_file = os.path.join(download_dir, file)
                print(f"処理対象ファイルが見つかりました: {input_audio_file}")
                break

    if input_audio_file:
        separate_audio(input_audio_file)
    else:
        print(f"エラー: '{download_dir}' ディレクトリに処理対象の.wavファイルが見つかりません。")
        print("まず youtube_downloader.py を実行して、音声ファイルをダウンロードしてください。") 