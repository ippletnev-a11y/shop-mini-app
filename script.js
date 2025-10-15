const homeButton = document.getElementById('homeButton');

homeButton.addEventListener('click', () => {
  // Отправляем данные в Telegram или закрываем WebApp
  if (window.Telegram.WebApp) {
    Telegram.WebApp.close(); // Закрывает мини-приложение
  } else {
    console.log('Назад');
  }
});