import requests

API_KEY = "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"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("AI Chatbot: Hello! Type 'bye' to exit.")

while True:
    user = input("You: ")

    if user.lower() == "bye":
        print("Bot: Goodbye!")
        break

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": user}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
            print("Bot:", reply)
        else:
            print("Error:", result)

    except Exception as e:
        print("Error:", e)