FROM python:3.10-slim

WORKDIR /app

# 先复制 requirements 以利用 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制剩余代码
COPY . .

# 运行机器人
CMD ["python", "bot.py"]