from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import datetime
from slackclient import SlackClient

SLACK_BOT_TOKEN = "xoxb-774540282707-781128700355-8MscTytuxmkbgoqdMGpefZGm"
slack_client = SlackClient(SLACK_BOT_TOKEN)


def slackitems(tracker):
    username = tracker.sender_id
    print("username", username)
    userinfo = slack_client.api_call("users.info", user=username)
    email = userinfo['user']['profile']['email']
    real_name = userinfo['user']['profile']['real_name']
    return email, real_name


class CertificateForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "certificate_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["certif_type", "period", "purpose", "details", "langue"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "certif_type": self.from_entity(entity="certif_type", not_intent="chitchat"),
            "period": [self.from_entity(entity="period"), self.from_text()],
            "purpose": [self.from_entity(entity="purpose"), self.from_text()],
            "details": [self.from_entity(entity="details"), self.from_text()],
            "langue": [self.from_entity(entity="langue"), self.from_text()],
        }


    @staticmethod
    def certif_db() -> List[Text]:
        return [
            "expense report",
            "leave authorization",
            "mission order",
            "pay statement",
            "salary certificate",
            "work certificate",
        ]

    @staticmethod
    def period_db() -> List[Text]:
        return [
            "tomorrow",
            "tomorrow morning",
            "30-10-2019",
            "next monday",
            "next week",
            "next month",
        ]

    @staticmethod
    def langue_db() -> List[Text]:
        return [
            "fr",
            "en",
            "french",
            "english",
        ]


    @staticmethod
    def is_int(string: Text) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False


    def validate_certif_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.certif_db():
            return {"certif_type": value}
        else:
            dispatcher.utter_template("utter_wrong_certif_type", tracker)
            return {"certif_type": None}

    def validate_period(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.period_db():
            return {"period": value}
        else:
            dispatcher.utter_template("utter_wrong_period", tracker)
            return {"period": None}

    def validate_langue(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.langue_db():
            return {"langue": True}
        else:
            return dispatcher.utter_template("utter_wrong_langue", tracker)
                

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template


        dispatcher.utter_template("utter_submit", tracker)
        return []
