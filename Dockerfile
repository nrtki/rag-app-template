# Python 3.11 の軽量版イメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# ビルドに必要なシステム依存関係をインストール
# (PostgreSQL用ドライバ asyncpg/psycopg2 などで必要になる場合があるため)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# uvicornサーバーを起動
# --host 0.0.0.0 はコンテナ外からアクセスするために必須
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]