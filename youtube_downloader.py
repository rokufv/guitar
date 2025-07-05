import yt_dlp
import os

def download_audio_from_youtube(url, output_path='.', file_format='wav'):
    """
    YouTubeの動画から音声をダウンロードし、指定されたフォーマットで保存する。

    :param url: YouTube動画のURL
    :param output_path: 保存先のディレクトリ
    :param file_format: 保存する音声フォーマット (例: 'wav', 'mp3')
    """
    # 出力先のディレクトリが存在しない場合は作成
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': file_format,
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"'{url}' から音声をダウンロードして{file_format}形式に変換します...")
            ydl.download([url])
            # yt-dlp はダウンロードと変換を自動で行うため、
            # 完了メッセージを表示する
            print("処理が完了しました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    import sys
    
    # コマンドライン引数からURLを取得
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
    else:
        # デフォルトURL（松本孝弘の例）
        youtube_url = "https://www.youtube.com/watch?v=P53EuU4-p8Y"
    
    # 保存先ディレクトリ
    download_dir = "downloaded_audio"

    download_audio_from_youtube(youtube_url, output_path=download_dir, file_format='wav') 