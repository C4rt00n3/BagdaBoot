from flask import Flask, request, jsonify
from models import MessageReceived, WhatsAppEvent
from utils import Interpreter
import random
from ChatBoot import ChatBoot

# Testes
import json
import random
import string

app = Flask(__name__)


#  Test


def create_json_file_with_string(data):
    file_name: str = str(random.randint(1, 10 * 1000)) + ".json"
    with open(file_name, "w") as file:
        json.dump(data, file)


@app.route("/hook", methods=["POST"])
def handle_hook():
    message_received: MessageReceived | None = None
    try:
        data = request.json
        whatsAppEvent = WhatsAppEvent(json.dumps(data))
        value = whatsAppEvent.entry[0].changes[0].value
        message_received = MessageReceived(
            destination=value.messages[0].from_number,
            name=value.contacts[0].profile.name,
            message=value.messages[0].text.body,
            wmaid=value.messages[0].id,
            type=value.messages[0].type,
        )

        Interpreter(
            message_received,
            whatsAppEvent,
        ).interpreter()
    except Exception as e:
        if message_received != None:
            message_received.message = "Tivemos um probleminha."
            ChatBoot.textGenerate(message_received)
        print(e)

    return jsonify({}), 200


@app.route("/hook", methods=["GET"])
def verify_hook():
    return request.args.get("hub.challenge", ""), 200


@app.route("/send_message", methods=["POST"])
def create_command():
    url = "https://graph.facebook.com/v19.0/PHONE_NUMBER_ID/conversational_automation"
    headers = {
        "Authorization": "Bearer ACCESS_TOKEN",
        "Content-Type": "application/json",
    }
    data = {
        "enable_welcome_message": True,
        "commands": {"name": "cookie", "description": "Bake a cookie"},
        "prompts": ["Book a flight", "plan a vacation"],
    }


if __name__ == "__main__":
    app.run(port=5000, debug=True)
