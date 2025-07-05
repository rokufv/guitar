# ギター音響分析・機材推薦システム

AI技術を活用したギター音響分析と機材推薦システムです。音源分離、ピッチ分析、RAG（Retrieval-Augmented Generation）xAgentsシステムを組み合わせて、高精度な機材推薦を実現しています。

## 🎯 主要機能

### 1. 音源分離
- **htdemucs**を使用した高精度な音源分離
- ギター、ベース、ドラム、ボーカルを自動分離
- 複数の音源フォーマットに対応（wav, mp3, flac等）

### 2. YouTube動画ダウンロード
- YouTube動画から音源を自動抽出
- 高品質な音源データの取得
- 自動的な音源分離処理

### 3. ピッチ分析
- リアルタイムピッチ検出
- 楽器の音程分析
- 音響特性の詳細解析

### 4. 機材推薦システム
- **RAG x Agentsシステム**による高精度推薦
- 6つの専門ツールによる段階的分析
- 予算別・カテゴリ別機材検索
- 有名ギタリストのサウンド再現提案

## 🚀 RAG x Agentsシステムの特徴

### 専門ツール
1. **カテゴリ別機材検索**: ギター、アンプ、エフェクター別の詳細検索
2. **予算別機材検索**: 指定予算内での最適機材組み合わせ
3. **サウンド特徴分析**: 音楽的特徴とサウンド特性の分析
4. **機材比較**: 複数機材の詳細比較と選択支援
5. **費用計算**: 総費用の自動計算と予算調整
6. **セマンティック検索**: 意味的な機材検索

### 推薦プロセス
1. **サウンド分析**: 目標とするサウンドの特徴を詳細分析
2. **予算最適化**: 予算内での最適な機材配分を計算
3. **機材選定**: カテゴリ別の最適機材を選択
4. **比較検討**: 候補機材の詳細比較
5. **費用調整**: 総費用の計算と予算内調整
6. **詳細推薦**: 具体的な購入アドバイスと接続方法

## 🛠️ 技術スタック

### フロントエンド
- **Streamlit**: Webアプリケーションフレームワーク
- **Python**: メインプログラミング言語

### AI・機械学習
- **LangChain**: エージェントシステム構築
- **OpenAI GPT**: 自然言語処理
- **RAG**: 検索拡張生成システム
- **htdemucs**: 音源分離AI

### データ処理
- **librosa**: 音響信号処理
- **numpy**: 数値計算
- **pandas**: データ分析

### その他
- **yt-dlp**: YouTube動画ダウンロード
- **streamlit-option-menu**: UI拡張

## 📦 インストール

### 1. リポジトリのクローン
```bash
git clone https://github.com/rokufv/guitar.git
cd guitar_sound
```

### 2. 仮想環境の作成
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境設定
```bash
# .envファイルを作成してOpenAI APIキーを設定
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## 🎵 使用方法

### 1. アプリケーション起動
```bash
streamlit run app.py
```

### 2. 機能選択
- **音源分離**: 音楽ファイルをアップロードして楽器別に分離
- **YouTube分析**: YouTube URLから音源を取得・分析
- **ピッチ分析**: 音程とピッチの詳細分析
- **機材推薦**: AI による機材推薦システム

### 3. 機材推薦の使用例
```
1. 目標ギタリストを選択（例: B'z 松本孝弘）
2. 予算を設定（例: 100万円）
3. 機材タイプを選択（ギター、アンプ、エフェクター）
4. エージェント推薦を有効化
5. 詳細な推薦結果を確認
```

## 📁 ファイル構成

```
guitar_sound/
├── app.py                    # メインアプリケーション
├── agent_system.py           # RAG x Agentsシステム
├── rag_system.py            # RAGシステム
├── audio_separator.py       # 音源分離
├── youtube_downloader.py    # YouTube動画ダウンロード
├── pitch_analyzer.py        # ピッチ分析
├── data_loader.py           # データローダー
├── config.py                # 設定ファイル
├── test_agent_system.py     # テストシステム
├── requirements.txt         # 依存関係
├── package.json            # Node.js依存関係
├── downloaded_audio/        # ダウンロード音源
├── separated_audio/         # 分離済み音源
└── env/                    # 仮想環境
```

## 🔧 設定ファイル

### config.py
```python
# OpenAI APIキーの設定
OPENAI_API_KEY = "your_api_key"

# 音源分離設定
AUDIO_SEPARATOR_MODEL = "htdemucs"
OUTPUT_FORMAT = "wav"

# 機材データベース設定
EQUIPMENT_DATABASE = "equipment_data.json"
```

## 🎸 サポート対象ギタリスト

- **B'z 松本孝弘**: ハードロック・ヘヴィメタル
- **結束バンド 後藤ひとり**: オルタナティブロック・エモ
- **その他多数**: システム拡張により追加可能

## 🧪 テスト

```bash
# エージェントシステムのテスト実行
python test_agent_system.py
```

## 📊 パフォーマンス

- **音源分離精度**: 高品質（htdemucs使用）
- **推薦精度**: 高精度（RAG x Agents）
- **処理速度**: 最適化済み
- **メモリ使用量**: 効率的

## 🔍 トラブルシューティング

### 一般的な問題

1. **OpenAI APIキーエラー**
   ```bash
   # .envファイルを確認
   cat .env
   ```

2. **音源分離エラー**
   ```bash
   # htdemucsdependenciesを再インストール
   pip install --upgrade demucs
   ```

3. **メモリ不足**
   ```bash
   # より小さなモデルを使用
   # config.pyでモデルサイズを調整
   ```

## 🚀 今後の拡張予定

- [ ] より多くのギタリストサポート
- [ ] リアルタイム音源分離
- [ ] モバイルアプリ対応
- [ ] 機材在庫連携
- [ ] コミュニティ機能

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

プルリクエストや issue の報告を歓迎します。

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/新機能`)
3. 変更をコミット (`git commit -am '新機能を追加'`)
4. ブランチをプッシュ (`git push origin feature/新機能`)
5. プルリクエストを作成

## 📞 サポート

- **Issues**: [GitHub Issues](https://github.com/rokufv/guitar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rokufv/guitar/discussions)

## 🙏 謝辞

- **htdemucs**: 高品質な音源分離技術
- **LangChain**: 柔軟なエージェントシステム
- **OpenAI**: 強力な言語モデル
- **Streamlit**: 簡単なWebアプリ構築

---

**作成者**: rokufv  
**バージョン**: 2.0  
**最終更新**: 2025年1月
