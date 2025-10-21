from http.server import BaseHTTPRequestHandler
import json
import os
import requests
import logging

class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "Python Bot API is running!",
            "framework": "Vercel Serverless Functions"
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            action = data.get('action')
            product = data.get('product')
            user_data = data.get('user_data', {})
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if action == 'create_order':
                # Обработка заказа
                order_id = self.create_order(product, user_data)
                
                # Отправка уведомления в Telegram
                self.send_telegram_notification(product, user_data, order_id)
                
                response = {
                    "success": True,
                    "message": f"Заказ '{product}' принят!",
                    "order_id": order_id
                }
            else:
                response = {
                    "success": False,
                    "message": "Unknown action"
                }
                
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"success": False, "error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def create_order(self, product, user_data):
        # Генерация ID заказа (в реальном приложении сохраняйте в БД)
        import random
        order_id = random.randint(1000, 9999)
        
        # Логирование заказа
        print(f"📦 New order: ID={order_id}, Product={product}, User={user_data.get('user', {}).get('first_name', 'Unknown')}")
        
        return order_id
    
    def send_telegram_notification(self, product, user_data, order_id):
        try:
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            admin_chat_id = os.environ.get('ADMIN_CHAT_ID')
            
            if not bot_token or not admin_chat_id:
                print("⚠️ Telegram credentials not set")
                return
            
            user_name = user_data.get('user', {}).get('first_name', 'Unknown')
            
            message = f"""
📦 **Новый заказ!**

🆔 **ID заказа:** #{order_id}
📱 **Товар:** {product}
👤 **Пользователь:** {user_name}
🌐 **Через:** Mini App
            """
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': admin_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code != 200:
                print(f"⚠️ Telegram API error: {response.text}")
                
        except Exception as e:
            print(f"⚠️ Error sending Telegram notification: {e}")