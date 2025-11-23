"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// メッセージの型定義
type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  // 入力中のテキスト
  const [input, setInput] = useState("");
  // チャット履歴（初期値は空）
  const [messages, setMessages] = useState<Message[]>([]);
  // 送信中のローディング状態
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // 1. ユーザーのメッセージを画面に即時表示
    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput(""); // 入力欄をクリア
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const aiMessage:Message = {
        role: "assistant",
        content: data.reply
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev, 
        { role: "assistant", content: "エラーが発生しました。バックエンドが起動しているか確認してください。" }
      ]);
    } finally {
      setIsLoading(false);
    }

  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      {/* ヘッダー */}
      <header className="p-4 border-b border-gray-700 bg-gray-800">
        <h1 className="text-xl font-bold">My RAG App</h1>
      </header>

      {/* チャットエリア（メッセージ一覧） */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            何でも質問してください
          </div>
        )}
        
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white" // ユーザーの吹き出し色
                  : "bg-gray-700 text-gray-100" // AIの吹き出し色
              }`}
            >
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  // デザイン調整（Tailwindでスタイルがリセットされるため）
                  strong: ({node, ...props}) => <span className="font-bold text-yellow-300" {...props} />,
                  a: ({node, ...props}) => <a className="text-blue-400 underline" target="_blank" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc pl-4 my-2" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal pl-4 my-2" {...props} />,
                }}
                >
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        
        {/* ローディング表示 */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 p-3 rounded-lg animate-pulse">
              考え中...
            </div>
          </div>
        )}
      </div>

      {/* 入力エリア */}
      <div className="p-4 bg-gray-800 border-t border-gray-700">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-gray-700 border border-gray-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="メッセージを入力..."
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 transition-colors"
          >
            送信
          </button>
        </form>
      </div>
    </div>
  );
}