# equipment_data.py

EQUIPMENT_DATA = {
    "B'z 松本孝弘": [
        # --- ギター ---
        {
            "name": "Gibson Tak Matsumoto Les Paul / Les Paul Standard", "type": "ギター", "price": "¥300,000 〜 ¥1,000,000以上", "level": "上級",
            "characteristics": "松本サウンドの核となる、甘く太いハムバッカーサウンドが特徴。",
            "image_url": "https://www.ishibashi.co.jp/ec/pic/product/2800003207516/2800003207516_1_l.jpg"
        },
        {
            "name": "Epiphone Les Paul Standard / Custom", "type": "ギター", "price": "¥70,000 〜 ¥120,000", "level": "中級",
            "characteristics": "Gibsonの公式傘下ブランド。見た目もサウンドも本家の特徴をよく捉えており、コストパフォーマンスが非常に高い。", "image_url": None
        },
        {
            "name": "Epiphone Les Paul Studio / Special", "type": "ギター", "price": "¥40,000 〜 ¥60,000", "level": "初級",
            "characteristics": "装飾をシンプルにして価格を抑えたモデル。レスポールらしいサウンドは健在で、最初の1本として十分なクオリティ。", "image_url": None
        },
        {
            "name": "YAMAHA MG-M / Music Man EVH", "type": "ギター", "price": "¥250,000以上（ヴィンテージ市場）", "level": "上級",
            "characteristics": "B'z初期のサウンドを支えた、テクニカルなプレイに対応しやすいギター。", 
            "image_url": "https://blog-imgs-38-origin.fc2.com/m/u/s/musicoffice/mgm-custom.jpg" 
        },
        {
            "name": "Ibanez RG Standardシリーズ / YAMAHA Pacifica 600シリーズ", "type": "ギター", "price": "¥80,000 〜 ¥150,000", "level": "中級",
            "characteristics": "薄いネックで弾きやすく、ロック式トレモロや多彩なピックアップ構成を持つモデルが多い。速弾きやアーム奏法に最適。", "image_url": None
        },
        {
            "name": "Ibanez GIOシリーズ / YAMAHA Pacifica 100・200シリーズ", "type": "ギター", "price": "¥30,000 〜 ¥50,000", "level": "初級",
            "characteristics": "世界的に評価の高い入門用ギターの定番。弾きやすさ、サウンドのバランスが良く、幅広いジャンルに対応できる。", "image_url": None
        },
        # --- アンプ ---
        {
            "name": "FAT / Bogner / PEAVEY 5150", "type": "アンプ", "price": "¥300,000以上（ヘッドアンプ）", "level": "上級",
            "characteristics": "ロックに必須の、パワフルで深く歪むサウンドを作る心臓部。",
            "image_url": "https://img.digimart.net/prdimg/m/5a/c5ae5b32d6156045029c4244957ea299cd7849.jpg" # Marshall JCM800の画像で代用
        },
        {
            "name": "BOSS KATANA-100 / Artist", "type": "アンプ", "price": "¥50,000 〜 ¥80,000", "level": "中級",
            "characteristics": "プロも使う多機能なモデリングアンプ。これ1台でクリーンから激しい歪みまで作れ、自宅練習からライブまで対応可能。", "image_url": None
        },
        {
            "name": "BOSS KATANA-50 / YAMAHA THR10II", "type": "アンプ", "price": "¥25,000 〜 ¥50,000", "level": "初級",
            "characteristics": "現代の入門アンプの決定版。小型で音質も良く、エフェクトも内蔵。USBでの録音にも対応。", "image_url": None
        },
        # --- エフェクター ---
        {
            "name": "Jim Dunlop TM95 (TAK CRY BABY)", "type": "エフェクター (ワウ)", "price": "¥30,000前後", "level": "上級",
            "characteristics": "感情的なサウンド表現に欠かせないシグネチャーモデルのワウペダル。",
            "image_url": "https://www.jimdunlop.com/content/images/products/originals/gcb95_17361138801_1.png"
        },
        {
            "name": "Jim Dunlop GCB95 (Original Cry Baby)", "type": "エフェクター (ワウ)", "price": "¥15,000前後", "level": "中級",
            "characteristics": "ワウペダルの世界標準。プロからアマまで最も多くのギタリストが使用している。", "image_url": None
        },
        {
            "name": "VOX V845", "type": "エフェクター (ワウ)", "price": "¥8,000前後", "level": "初級",
            "characteristics": "定番クライベイビーより少しマイルドな効きだが、基本性能は十分な入門モデル。", "image_url": None
        },
        {
            "name": "FAT 514.D", "type": "エフェクター (歪み)", "price": "カスタム品", "level": "上級",
            "characteristics": "アンプだけでは作れない、もう一段階上の歪みや音のハリを加えるカスタムペダル。", "image_url": None
        },
        {
            "name": "BOSS BD-2 (Blues Driver) / SD-1 (Super OverDrive)", "type": "エフェクター (歪み)", "price": "¥9,000 〜 ¥12,000", "level": "中級",
            "characteristics": "どちらも歴史的な名機。松本氏も過去に使用しており、特にBD-2は幅広いゲインに対応できる万能選手。", "image_url": None
        },
        {
            "name": "Ibanez TS MINI (Tube Screamer Mini)", "type": "エフェクター (歪み)", "price": "¥8,000前後", "level": "初級",
            "characteristics": "伝説的なTS9のサウンドを小型・低価格で実現。ブースターとして使うのが定番。", "image_url": None
        },
        {
            "name": "BOSS DD-500", "type": "エフェクター (ディレイ)", "price": "¥40,000前後", "level": "上級",
            "characteristics": "音をやまびこのように響かせ、ソロに広がりと立体感を与える高機能デジタルディレイ。", "image_url": None
        },
        {
            "name": "BOSS DD-8 / DD-3T", "type": "エフェクター (ディレイ)", "price": "¥20,000前後", "level": "中級",
            "characteristics": "コンパクトペダルのディレイの決定版。シンプルながらプロの現場でも通用する高音質。", "image_url": None
        },
        {
            "name": "Donner Yellow Fall / Mooer Reecho", "type": "エフェクター (ディレイ)", "price": "¥5,000 〜 ¥8,000", "level": "初級",
            "characteristics": "低価格ながら基本的なディレイサウンドはしっかり出せるモデル。最初のディレイとして人気。", "image_url": None
        },
        {
            "name": "DigiTech Whammy 5", "type": "エフェクター (ピッチシフター)", "price": "¥35,000前後", "level": "上級",
            "characteristics": "ペダル操作で音程を急上昇・急降下させる、彼の代名詞とも言えるエフェクト。", "image_url": None
        },
        {
            "name": "DigiTech Whammy Ricochet", "type": "エフェクター (ピッチシフター)", "price": "¥25,000前後", "level": "中級",
            "characteristics": "ペダル無しのコンパクト版。スイッチ操作でワーミーサウンドを再現でき、場所を取らない。", "image_url": None
        },
        {
            "name": "Zoom G1 Four (内蔵機能)", "type": "エフェクター (ピッチシフター)", "price": "¥10,000前後", "level": "初級",
            "characteristics": "多機能マルチエフェクターに内蔵されているピッチベンド機能で代用。他のエフェクトも試せるため入門者に最適。", "image_url": None
        },
    ],
    "布袋寅泰": [
        # --- ギター ---
        {
            "name": "Zemaitis / Zodiacworks TC-HOTEI", "type": "ギター", "price": "¥500,000以上（カスタム品）", "level": "上級",
            "characteristics": "布袋サウンドの象徴。鋭いカッティングと幾何学模様のG柄が最大の特徴。",
            "image_url": "https://i.ebayimg.com/images/g/w~MAAOSwqOtkxARw/s-l1600.jpg"
        },
        {
            "name": "Fender Made in Japan Telecaster / TE-HT (FERNANDES)", "type": "ギター", "price": "¥80,000 〜 ¥150,000", "level": "中級",
            "characteristics": "TE-HTは最も手に入れやすい布袋モデルのレプリカ。Fender Japan製のテレキャスターもシャープなサウンドでカッティングに適している。", "image_url": None
        },
        {
            "name": "Squier by Fender Classic Vibe / Affinity Telecaster", "type": "ギター", "price": "¥35,000 〜 ¥60,000", "level": "初級",
            "characteristics": "Fender直系ブランドならではの、テレキャスターらしいサウンドと弾き心地を手頃な価格で実現。", "image_url": None
        },
        # --- アンプ ---
        {
            "name": "Roland JC-120 / Pete Cornish Custom Amp", "type": "アンプ", "price": "¥150,000以上", "level": "上級",
            "characteristics": "彼のサウンドの基本となる、クリーンでありながらも芯のあるサウンド。特にJC-120のコーラスは象徴的。",
            "image_url": "https://static.roland.com/products/jc-120/features/images/jc-120_features_01.jpg"
        },
        {
            "name": "Roland JC-40 / JC-22", "type": "アンプ", "price": "¥50,000 〜 ¥80,000", "level": "中級",
            "characteristics": "伝説的なJC-120のサウンドを、より小型で自宅でも使いやすいサイズにしたモデル。美しいクリーンとコーラスは健在。", "image_url": None
        },
        {
            "name": "BOSS KATANA-50 / YAMAHA THR10II", "type": "アンプ", "price": "¥25,000 〜 ¥50,000", "level": "初級",
            "characteristics": "モデリングアンプの「JC-120」モードや「Clean」モードを使うことで、煌びやかなクリーントーンを再現可能。", "image_url": None
        },
        # --- エフェクター ---
        {
            "name": "KORG SDD-3000", "type": "エフェクター (空間系)", "price": "¥40,000以上", "level": "上級",
            "characteristics": "彼のサウンドの核。クリアで特徴的なディレイサウンド。",
            "image_url": "https://www.korg.com/us/products/effects/sdd3000_pedal/images/img_main.png"
        },
        {
            "name": "Pete Cornish / Providence SONIC DRIVE", "type": "エフェクター (歪み)", "price": "カスタム品 / ¥30,000以上", "level": "上級",
            "characteristics": "クリーンなアンプを基本に、曲に合わせて多彩な歪みを加える。", "image_url": None
        },
        {
            "name": "Proco RAT 2 / Xotic BB Preamp", "type": "エフェクター (歪み)", "price": "¥15,000 〜 ¥25,000", "level": "中級",
            "characteristics": "RATはエッジの効いたディストーションの定番。BB Preampはアンプライクで自然な歪みを作れる。", "image_url": None
        },
        {
            "name": "BOSS DS-1 (Distortion)", "type": "エフェクター (歪み)", "price": "¥8,000前後", "level": "初級",
            "characteristics": "多くのレジェンドが使用してきたディストーションの金字塔。シャープで攻撃的なサウンドが得られる。", "image_url": None
        },
        {
            "name": "Free The Tone FT-1Y / BOSS RV-500", "type": "エフェクター (空間系)", "price": "¥40,000以上", "level": "上級",
            "characteristics": "サウンドに広がりと浮遊感を与えるプロ仕様の高品質な空間系エフェクト。", "image_url": None
        },
        {
            "name": "BOSS GT-1 / Line 6 M5 Stompbox Modeler", "type": "エフェクター (空間系マルチ)", "price": "¥20,000 〜 ¥30,000", "level": "中級",
            "characteristics": "コンパクトなマルチエフェクター。ディレイ、リバーブ、コーラスなど、必要な空間系エフェクトが一台にまとまっている。", "image_url": None
        },
        {
            "name": "ZOOM G1 Four / MS-50G", "type": "エフェクター (空間系マルチ)", "price": "¥10,000前後", "level": "初級",
            "characteristics": "非常にコストパフォーマンスの高いマルチエフェクター。様々なエフェクトを試しながら、自分の好きな音を探すのに最適。", "image_url": None
        },
    ],
    "結束バンド 後藤ひとり": [
        # --- ギター ---
        {
            "name": "Gibson Les Paul Custom", "type": "ギター", "price": "¥500,000以上", "level": "上級",
            "characteristics": "\"ギターヒーロー\"としての活動初期を支えた、パワフルでロックなサウンドが特徴のギター。",
            "image_url": "https://static.gibson.com/product-images/Custom/CUSZJG839/Ebony/front-5k.png"
        },
        {
            "name": "Epiphone Les Paul Custom", "type": "ギター", "price": "¥70,000 〜 ¥100,000", "level": "中級",
            "characteristics": "Gibsonの公式傘下ブランド。ルックス、サウンド共に本家の特徴を忠実に再現しており、多くのギタリストに愛されている。", "image_url": None
        },
        {
            "name": "Epiphone Les Paul Standard", "type": "ギター", "price": "¥50,000 〜 ¥70,000", "level": "初級",
            "characteristics": "カスタムモデルから装飾をシンプルにすることで、より手頃な価格を実現したモデル。レスポールらしいサウンドは健在。", "image_url": None
        },
        {
            "name": "YAMAHA PACIFICA 611VFM (ぼっちちゃんカスタム)", "type": "ギター", "price": "非売品（ベースモデルは¥70,000前後）", "level": "上級",
            "characteristics": "ライブでのトラブルをきっかけに手に入れた、多彩な音作りと高い演奏性が魅力のギター。",
            "image_url": "https://uk.yamaha.com/en/files/pacifica-611-flamed-maple-top_1200x480_a745c11739c9f80a4a81ca5a8a1de7a9.jpg"
        },
        {
            "name": "YAMAHA PACIFICA 612VIIFM / 311H", "type": "ギター", "price": "¥50,000 〜 ¥80,000", "level": "中級",
            "characteristics": "高品質なパーツを搭載し、コイルタップ機能などで多彩なサウンドメイクが可能。ジャンルを問わず活躍できる一本。", "image_url": None
        },
        {
            "name": "YAMAHA PACIFICA 112V / 212VFM", "type": "ギター", "price": "¥35,000 〜 ¥50,000", "level": "初級",
            "characteristics": "正確な音程、高い演奏性、多彩な音色を兼ね備えた、初心者向けモデルの決定版として高い評価を得ている。", "image_url": None
        },
        # --- アンプ ---
        {
            "name": "YAMAHA THRシリーズ (THR5, THR10IIなど)", "type": "アンプ", "price": "¥25,000 〜 ¥50,000", "level": "上級/中級/初級 共通",
            "characteristics": "デスクトップアンプという新しいカテゴリを確立した人気シリーズ。様々なアンプモデルとエフェクトを内蔵し、これ一台でプロクオリティのサウンドを小音量で楽しめる。",
            "image_url": "https://usa.yamaha.com/products/musical_instruments/guitars_basses/amps_accessories/thr/classic-gallery/500x500/thr5_600_001.jpg"
        },
        # --- エフェクター ---
        {
            "name": "BOSS BD-2 (Blues Driver)", "type": "エフェクター (歪み)", "price": "¥12,000前後", "level": "中級",
            "characteristics": "ピッキングのニュアンスを忠実に再現する、クランチからオーバードライブまでカバーする定番ペダル。",
            "image_url": "https://static.roland.com/products/bd-2/features/images/bd-2_features_1_mb.jpg"
        },
         {
            "name": "ProCo RAT2", "type": "エフェクター (歪み)", "price": "¥15,000前後", "level": "上級",
            "characteristics": "ぼっちちゃんの感情豊かなギターソロを表現するのに欠かせない、定番の歪みエフェクターの組み合わせ。", "image_url": None
        },
        {
            "name": "JOYO JF-02 (Ultimate Drive) / BEHRINGER OD300", "type": "エフェクター (歪み)", "price": "¥4,000 〜 ¥7,000", "level": "初級",
            "characteristics": "手頃な価格ながら、本格的なオーバードライブサウンドが得られるペダル。初めての歪みエフェクターとしておすすめ。", "image_url": None
        },
    ]
} 