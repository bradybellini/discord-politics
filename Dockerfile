FROM python:3.8.1
RUN mkdir /discord/bots/discord-politics
WORKDIR /home/discord/bots/discord-politics
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "bot.py"]