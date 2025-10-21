fetch("https://tidy-hoops-read.loca.lt", {
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
