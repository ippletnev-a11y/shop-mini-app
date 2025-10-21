import React, { useState } from "react";

export default function App() {
  const [status, setStatus] = useState("Нажми кнопку, чтобы отправить JSON");

  // ⚙️ Твой публичный URL из ngrok
  const API_URL = "https://loud-paws-count.loca.lt"; // ← сюда вставь свой адресa

  const handleSend = async () => {
    setStatus("⏳ Отправка данных...");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user: "Иван",
          product: "Candle Shield of Egypt",
          quantity: 2,
          price: 990,
          currency: "RUB"
        })
      });

      const data = await response.json();
      console.log("Ответ сервера:", data);
      setStatus("✅ Успешно отправлено!");
    } catch (error) {
      console.error("Ошибка:", error);
      setStatus("❌ Ошибка отправки данных");
    }
  };

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        textAlign: "center",
        padding: "40px",
        background: "#f3f4f6",
        minHeight: "100vh"
      }}
    >
      <h2>🕯️ Mini App — Отправка JSON</h2>
      <p>{status}</p>
      <button
        onClick={handleSend}
        style={{
          background: "#0088cc",
          color: "white",
          border: "none",
          borderRadius: "8px",
          padding: "12px 20px",
          cursor: "pointer",
          fontSize: "16px"
        }}
      >
        📤 Отправить заказ
      </button>
    </div>
  );
}
