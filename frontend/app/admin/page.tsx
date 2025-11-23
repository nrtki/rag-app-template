"use client";

import { useState } from "react";
import Link from "next/link";

export default function AdminPage() {
  const [content, setContent] = useState("");
  const [source, setSource] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content) return;

    try {
      setStatus("送信中...");
      
      // バックエンドの /documents API を叩く
      const res = await fetch("http://localhost:8000/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, source }),
      });

      if (!res.ok) throw new Error("登録に失敗しました");

      setStatus("✅ 登録完了！");
      setContent(""); // フォームをクリア
      setSource("");
    } catch (error) {
      console.error(error);
      setStatus("❌ エラーが発生しました");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">ドキュメント登録 (Admin)</h1>
          <Link href="/" className="text-blue-400 hover:underline">
            ← チャットに戻る
          </Link>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 bg-gray-800 p-6 rounded-lg">
          {/* ソース入力欄 */}
          <div>
            <label className="block text-sm font-medium mb-2">出典・タイトル</label>
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              placeholder="例: 社内規定.pdf, Wikipediaなど"
              className="w-full bg-gray-700 border border-gray-600 rounded p-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          {/* 本文入力欄 */}
          <div>
            <label className="block text-sm font-medium mb-2">ドキュメント本文</label>
            <textarea
              rows={6}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="ここにAIに覚えさせたいテキストを入力してください..."
              className="w-full bg-gray-700 border border-gray-600 rounded p-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded transition-colors"
          >
            データベースに登録
          </button>

          {status && <p className="text-center text-lg mt-4">{status}</p>}
        </form>
      </div>
    </div>
  );
}