FROM python:3.8.1
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD ["python3", "bot.py"]
