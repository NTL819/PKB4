import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
from flask import Flask, request # <--- THÊM FLASK

# Load biến môi trường (TOKEN) từ file .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Khai báo Intent cơ bản cho bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# === START: CẤU HÌNH WEB SERVER CHO RENDER/UPTIMEROBOT ===
# 1. Khởi tạo Flask App
app = Flask(__name__)

# 2. Xử lý yêu cầu Ping/Kiểm tra sức khỏe
@app.route('/')
def home():
    # Khi UptimeRobot hoặc Render ping, trả về mã 200 OK
    return 'Bot đang chạy và hoạt động tốt!', 200

# Lấy Port từ Render (Render tự động cung cấp)
def run_web_server():
    port = int(os.environ.get("PORT", 8080)) # Mặc định là 8080 nếu không có PORT
    # Bắt buộc phải host trên 0.0.0.0 để hoạt động trên Render
    app.run(host='0.0.0.0', port=port) 

# === END: CẤU HÌNH WEB SERVER ===

# Sự kiện bot đã sẵn sàng
@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập với tên: {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ hóa {len(synced)} lệnh (/): {[c.name for c in synced]}")
    except Exception as e:
        print(f"Lỗi đồng bộ lệnh: {e}")

# Xử lý Lệnh Slash Command /hoatdong
@bot.tree.command(name="hoatdong", description="Gợi ý một hoạt động ngẫu nhiên")
async def hoatdong_command(interaction: discord.Interaction):
    activities = [
        "Xem YouTube 🎬",
        "Chơi Liên Quân 📱",
        "Chơi Cờ Vua ♟️",
        "Học bài 📚",
        "Tập thể dục/đi bộ 🏃",
        "Đi ăn vặt 🍔"
    ]
    random_activity = random.choice(activities)
    await interaction.response.send_message(f"💡 **Hôm nay bạn nên:** {random_activity}")

# Khởi chạy bot và web server trong các luồng khác nhau
# Sử dụng thư viện threading để chạy đồng thời bot Discord và web server Flask
import threading

def start_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    # Chạy bot Discord trong một luồng riêng
    t = threading.Thread(target=start_bot)
    t.start()
    
    # Chạy web server Flask trong luồng chính
    run_web_server() 
