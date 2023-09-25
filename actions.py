# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from flask import Flask, request, jsonify
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

app = Flask(__name__)


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProvidePPTDownloadLink(Action):
    def name(self):
        return "action_provide_ppt_download_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Get the list of entities from the latest user message
        entities = tracker.latest_message.get("entities")

        # Check if there are entities and if the "use_case" entity is present
        if entities:
            use_case_entity = next((entity for entity in entities if entity["entity"] == "use_case"), None)

            if use_case_entity:
                use_case = use_case_entity["value"]
                print(f"Use Case: {use_case}")

                # TODO: Use the use_case to generate/download the PPT link
                # You can replace the next line with your code to get the download link
                download_link = "C:/Users/dell/Desktop/rsa/ppt" + use_case

                dispatcher.utter_message(f"Sure! You can download the PPT on {use_case} from this link: {download_link}")
            else:
                dispatcher.utter_message("I couldn't detect a use case in your message.")
        else:
            dispatcher.utter_message("I couldn't detect any entities in your message.")

        return []
        
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    action_name = data["next_action"]
    dispatcher = CollectingDispatcher()
    tracker = Tracker(data["sender_id"], data["user"], data["slots"], data["latest_message"])
    domain = data["domain"]

    if action_name == "action_provide_ppt_download_link":
        action = ActionProvidePPTDownloadLink()
        action.run(dispatcher, tracker, domain)

    return jsonify(dispatcher.messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)