# AI RAG Chat Application

Gemini APIとPostgreSQL (pgvector) を活用した、ドキュメント検索機能付きAIチャットアプリです。
独自のドキュメントを学習（ベクトル化して保存）し、その内容に基づいてAIが回答します。

## 🛠 使用技術 (Tech Stack)

- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS
- **Backend:** Python (FastAPI), SQLAlchemy
- **Database:** PostgreSQL (pgvector), Docker
- **AI:** Google Gemini API (Flash 1.5), text-embedding-004

## 🚀 環境構築 (初回のみ)

### 1. 前提条件
以下のツールがインストールされていること。
- Docker Desktop
- Python 3.10以上
- Node.js 18以上

### 2. 環境変数の設定
ルートディレクトリに `.env` ファイルを作成し、以下を記述してください。

```ini
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rag_db
GEMINI_API_KEY=ここにあなたのGeminiAPIキー
````

### 3\. 依存ライブラリのインストール

**Backend:**

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化 (Windows)
.\venv\Scripts\activate
# 仮想環境の有効化 (Mac/Linux)
# source venv/bin/activate

# ライブラリインストール
pip install -r requirements.txt
# ※ requirements.txt がない場合は pip install fastapi uvicorn[standard] sqlalchemy asyncpg pgvector pydantic-settings google-generativeai python-dotenv
```

**Frontend:**

```bash
cd frontend
npm install
cd ..
```

-----

## ▶️ 起動手順 (Daily Usage)

以下の順序で起動してください。ターミナルを3つ開くと便利です。

### Step 1: データベースの起動 (Terminal 1)

Dockerコンテナを立ち上げます。

```bash
docker-compose up -d
```

※ 初回起動時はDB作成に少し時間がかかります。

### Step 2: バックエンドの起動 (Terminal 2)

FastAPIサーバーを立ち上げます。

```bash
# 仮想環境に入る (Windows)
.\venv\Scripts\activate
# (Mac/Linux: source venv/bin/activate)

# サーバー起動 (Hot Reload有効)
uvicorn app.main:app --reload
```

※ `DB connection & Tables created!!` と表示されれば接続成功です。

### Step 3: フロントエンドの起動 (Terminal 3)

Next.jsサーバーを立ち上げます。

```bash
cd frontend
npm run dev
```

### Step 4: ブラウザでアクセス

  - **チャット画面:** http://localhost:3000
  - **管理・登録画面:** http://localhost:3000/admin
  - **APIドキュメント:** http://localhost:8000/docs

-----

## ⏹ 終了手順

1.  **Frontend & Backend:**
    それぞれのターミナルで `Ctrl + C` を押して停止します。

2.  **Database:**
    以下のコマンドでコンテナを停止します（データは保持されます）。

    ```bash
    docker-compose stop
    ```

    ※ `docker-compose down -v` とするとデータが消えるので注意してください。

<!-- end list -->
