import requests
import json
import time
from .classes import Interaction
from .utils import convert_to_string, URLS


def carterRequest(url, data, headers):
    try:
        response = requests.post(
            url, data=json.dumps(data), headers=headers)
        carter_data = response.json()
        return {"carter_data": carter_data, "status_code": response.status_code, "status_message": response.reason, "ok": response.ok, "url": response.url}
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        return None


class Carter:
    def __init__(self, api_key, speak=False):
        self.api_key = api_key
        self.history = []
        self.speak_default = speak

    def say(self, text, user_id, speak=None):
        text = convert_to_string("text", text)
        user_id = convert_to_string("user_id", user_id)
        start = time.perf_counter()
        speak_now = speak if speak is not None else self.speak_default
        data = {
            "text": text,
            "user_id": user_id,
            "key": self.api_key,
            "speak": speak_now
        }

        headersList = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }

        response_data = carterRequest(URLS["say"], data, headers=headersList)
        time_taken = int((time.perf_counter() - start) * 1000)
        interaction = Interaction("say", data, response_data, time_taken)
        if interaction.ok:
            self.history.insert(0, interaction)
        return interaction

    def opener(self, user_id, speak=None):
        user_id = convert_to_string("user_id", user_id)
        start = time.perf_counter()
        speak_now = speak if speak is not None else self.speak_default
        data = {
            "user_id": user_id,
            "key": self.api_key,
            "speak": speak_now,
            "personal": True
        }
        headersList = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        response = carterRequest(
            URLS["opener"], headers=headersList, data=data)
        time_taken = int((time.perf_counter() - start) * 1000)
        interaction = Interaction("opener", data, response, time_taken)
        if interaction.ok:
            self.history.insert(0, interaction)
        return interaction

    def personalise(self, text, user_id, speak=None):
        text = convert_to_string("text", text)
        start = time.perf_counter()
        speak_now = speak if speak is not None else self.speak_default
        data = {
            "text": text,
            "key": self.api_key,
            "speak": speak_now,
            "user_id": user_id
        }
        headersList = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        response = carterRequest(
            URLS["personalise"], headers=headersList, data=data)
        time_taken = int((time.perf_counter() - start) * 1000)
        interaction = Interaction("personalise", data, response, time_taken)
        return interaction
