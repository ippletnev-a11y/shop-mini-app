window.Telegram.WebApp.ready();
window.Telegram.WebApp.expand();
window.Telegram.WebApp.setBackgroundColor('#f0f0f0');
window.Telegram.WebApp.setHeaderColor('#f0f0f0');
window.Telegram.WebApp.MainButton.setText('Перейти к покупкам').show();
console.log('Telegram WebApp загружен');
document.body.insertAdjacentHTML('beforeend', '<p>Тест: Каталог категорий загружен</p>');