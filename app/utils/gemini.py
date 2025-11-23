import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# APIキー設定
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. テキストをベクトル化する関数
async def get_embedding(text: str):
    # text-embedding-004 (768次元) を使用
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document" # 検索用として最適化
    )
    return result['embedding']

# 2. 検索結果を元に回答を生成する関数
async def generate_answer(query: str, context: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    あなたは役に立つアシスタントです。以下の「参考情報」を使って、ユーザーの質問に答えてください。
    参考情報に答えがない場合は、「その情報は持ち合わせていません」と答えてください。

    【参考情報】
    {context}

    【質問】
    {query}
    """
    
    response = await model.generate_content_async(prompt)
    return response.text