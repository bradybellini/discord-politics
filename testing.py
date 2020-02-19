import httpx
import urllib3

webhook_url = "https://discordapp.com/api/webhooks/679439396780507136/2mlrIl-1Dkzy5HaRllKhcbgICH5OCTq-ICom7YLyI4nG5CNVXMSOWxqEh72zfnnx3m-o"
data = {'content':'hello'}
httpx.post(webhook_url,data=data)
