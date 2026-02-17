import os
import telebot
import psycopg2
import requests

# 从环境变量获取配置
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
DB_HOST = os.environ.get('DB_HOST', 'ak-postgres-db')
DB_NAME = os.environ.get('DB_NAME', 'ak_weather')
DB_USER = os.environ.get('DB_USER', 'ak_user')
DB_PASS = os.environ.get('DB_PASS', 'ak_password')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def log_to_db(user_id, city):
    """将查询记录写入 PostgreSQL"""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("INSERT INTO ak_weather_logs (user_id, city) VALUES (%s, %s)", (user_id, city))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Logged query for {city} by user {user_id}")
    except Exception as e:
        print(f"Database Error: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "你好！我是 AK 天气机器人。发送城市拼音（例如 beijing, london）来获取当前天气。")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            bot.reply_to(message, "找不到这个城市的天气，请检查拼写。")
            return

        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        reply_text = f"🏙️ {city} 的天气:\n🌡️ 温度: {temp}°C\n☁️ 状况: {desc}"
        
        bot.reply_to(message, reply_text)
        # 存入数据库
        log_to_db(message.from_user.id, city)
        
    except Exception as e:
        bot.reply_to(message, "API 请求出错，请稍后再试。")
        print(f"API Error: {e}")

if __name__ == '__main__':
    print("AK Bot is starting...")
    bot.polling(none_stop=True)