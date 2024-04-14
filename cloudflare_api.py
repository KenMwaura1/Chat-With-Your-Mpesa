import requests
from dotenv import load_dotenv
import os
from getpass import getpass

load_dotenv()

account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
api_token = os.getenv("CLOUDFLARE_API_TOKEN")

if "CLOUDFLARE_API_TOKEN" in os.environ:
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
else:
    api_token = getpass("Enter you Cloudflare API Token")
    
if "CLOUDFLARE_ACCOUNT_ID" in os.environ:
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
else:
    account_id = getpass("Enter your account id")

model_name = "@cf/facebook/bart-large-cnn"

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}"

prompt = "# A function that checks if a given word is a palindrome"

payload = {
    "input_text": f"{prompt}",
    "max_length": 1024,
 }

response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}",
    headers={"Authorization": f"Bearer {api_token}"}, json=payload
)
inference = response.json()
# code = inference["result"]["response"]

print(inference)
