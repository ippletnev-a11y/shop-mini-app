fetch("https://abc1234.ngrok.io/data", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    user: "Ivan",
    product: "Candle Shield of Egypt",
    quantity: 2
  })
})
  .then(res => res.json())
  .then(data => console.log("Ответ:", data))
  .catch(err => console.error("Ошибка:", err));
