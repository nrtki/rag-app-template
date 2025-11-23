# Node.js 18 の軽量版イメージを使用
FROM node:20-alpine
# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm install

# ソースコードをコピー
COPY . .

# Next.js アプリのビルド (本番用)
# 開発モード(npm run dev)で動かしたい場合はここをスキップしてCMDを変える
RUN npm run build

# ポート公開
EXPOSE 3000

# アプリ起動
CMD ["npm", "start"]