from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import datetime
from slackclient import SlackClient
import requests
import json

SLACK_BOT_TOKEN = "xoxb-774540282707-807010447156-DarOEvj5aPXmZwwt5jxj5QG3"
API_ENDPOINT = "http://localhost:5000/setdata"
slack_client = SlackClient(SLACK_BOT_TOKEN)


def slackitems(tracker):
    username = tracker.sender_id
    print("username", username)
    userinfo = slack_client.api_call("users.info", user=username)
    email = userinfo['user']['profile']['email']
    real_name = userinfo['user']['profile']['real_name']
    return email, real_name


class CertificateForm(FormAction):

    def name(self) -> Text:
        return "certificate_form"

    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        if tracker.get_slot("certif_type") == "expense report":
            return ["period","purpose","details"]
        if tracker.get_slot("certif_type") == "work certificate" or tracker.get_slot("certif_type") == "salary certificate":
            return ["langue","copies_num"]
        if tracker.get_slot("certif_type") == "mission order":
            return ["endroit","period","purpose"]
        if tracker.get_slot("certif_type") == "leave authorization":
            return ["dep_date", "dep_date_half_day", "end_date", "end_date_half_day"]
        else:
            return ["certif_type", "period", "purpose", "details", "langue","endroit"]

    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "certif_type": self.from_entity(entity="certif_type", not_intent="chitchat"),
            "period": [self.from_entity(entity="period"), self.from_text()],
            "purpose": [self.from_entity(entity="purpose"), self.from_text()],
            "details": [self.from_entity(entity="details"), self.from_text()],
            "langue": [self.from_entity(entity="langue"), self.from_text()],
            "copies_num": [self.from_entity(entity="copies_num", intent=["inform"]),self.from_entity(entity="number"),],
            "endroit": [self.from_entity(entity="endroit"), self.from_text()],
            "dep_date": [self.from_entity(entity="dep_date"), self.from_text()],
            "dep_date_half_day": [self.from_entity(entity="dep_date_half_day"), self.from_text()],
            "end_date": [self.from_entity(entity="end_date"), self.from_text()],
            "end_date_half_day": [self.from_entity(entity="end_date_half_day"), self.from_text()],
        }


    @staticmethod
    def certif_db() -> List[Text]:
        return ["expense report","leave authorization","mission order","pay statement","salary certificate","work certificate",]

    
    @staticmethod
    def period_db() -> List[Text]:
        return ["tomorrow","tomorrow morning","30-10-2019","next monday","next week","next month",]

    
    @staticmethod
    def langue_db() -> List[Text]:
        return ["fr","en","french","english",]


    @staticmethod
    def endroit_db() -> List[Text]:
        return ["rabat","casablanca","agadir",]


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
            return {"langue": value}
        else:
            return dispatcher.utter_template("utter_wrong_langue", tracker)
    

    def validate_copies_num(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if self.is_int(value) and int(value) > 0:
            return {"copies_num": value}
        else:
            dispatcher.utter_template("utter_wrong_copies_num", tracker)
            return {"copies_num": None}


    def validate_endroit(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value in self.endroit_db():
            return {"endroit": value}
        else:
            return dispatcher.utter_template("utter_wrong_endroit", tracker)


    def validate_dep_date(
                    self,
                    value: Text,
                    dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any],
                ) -> Dict[Text, Any]:
            
                    connection_file = open('learning_data.json', 'r')
                    learn_data = json.load(connection_file)
                    connection_file.close()

                    time_slot = tracker.get_slot("time") if tracker.get_slot("time") is not None else learn_data["time"]
                    return {"dep_date": time_slot}
                    
                    """if value.lower() in self.period_db():
                                                                                    return {"dep_date": time_slot}
                                                                                else:
                                                                                    dispatcher.utter_template("utter_wrong_dep_date", tracker)
                                                                                    return {"dep_date": None}"""


    def validate_end_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.period_db():
            return {"end_date": value}
        else:
            dispatcher.utter_template("utter_wrong_end_date", tracker)
            return {"end_date": None}


    def validate_dep_date_sshalf_day(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if isinstance(value, str):
            if "yes" in value:
                return {"dep_date_half_day": True}
            elif "no" in value:
                return {"dep_date_half_day": False}
            else:
                dispatcher.utter_template("utter_wrong_dep_date_half_day", tracker)
                return {"dep_date_half_day": None}

        else:
            return {"dep_date_half_day": value}


    def validate_end_date_half_day(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if isinstance(value, str):
            if value == "yes":
                return {"end_date_half_day": value}
            elif value == "no":
                return {"end_date_half_day": value}
            else:
                dispatcher.utter_template("utter_wrong_end_date_half_day", tracker)
                return {"end_date_half_day": None}

        else:
            return {"end_date_half_day": value}


    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        certificate_type = tracker.get_slot('certif_type')
        if certificate_type == "work certificate" or certificate_type == "salary certificate":
            email = slackitems(tracker)[0]
            username = slackitems(tracker)[1]
            #change them in respect to saad requirements
            body = {'certif_type':tracker.slots['certif_type'],
            'slack_username': username,
            "mail":email,
            "langue":tracker.slots['langue'],
            "copies_num":tracker.slots['copies_num']
            }
            headers = {'content-type': 'application/json'}
            post_data = requests.post(API_ENDPOINT, data = json.dumps(body),headers=headers)
            dispatcher.utter_template("utter_submit_work_salary_certificate", tracker, **tracker.slots)
            return []
        
        if certificate_type == "expense report":
            email = slackitems(tracker)[0]
            username = slackitems(tracker)[1]
            #change them in respect to saad requirements
            body = {'certif_type':tracker.slots['certif_type'],
            'slack_username': username,
            "mail":email,
            "period":tracker.slots['period'],
            "purpose":tracker.slots['purpose'],
            "details":tracker.slots['details']
            }
            headers = {'content-type': 'application/json'}
            post_data = requests.post(API_ENDPOINT, data = json.dumps(body),headers=headers)
            dispatcher.utter_template("utter_submit_expense_report", tracker, **tracker.slots)
            return []
        
        if certificate_type == "mission order":
            email = slackitems(tracker)[0]
            username = slackitems(tracker)[1]
            #change them in respect to saad requirements
            body = {'certif_type':tracker.slots['certif_type'],
            'slack_username': username,
            "mail":email,
            "period":tracker.slots['period'],
            "purpose":tracker.slots['purpose'],
            "endroit":tracker.slots['endroit']
            }
            headers = {'content-type': 'application/json'}
            post_data = requests.post(API_ENDPOINT, data = json.dumps(body),headers=headers)
            dispatcher.utter_template("utter_submit_mission_order", tracker, **tracker.slots)
            return []
        
        if certificate_type == "leave authorization":

            email = slackitems(tracker)[0]
            username = slackitems(tracker)[1]
            #change them in respect to saad requirements
            body = {'certif_type':tracker.slots['certif_type'],
            'slack_username': username,
            "mail":email,
            "departure_date":tracker.slots['dep_date'],
            "dep_date_half_day":tracker.slots['dep_date_half_day'],
            "end_date":tracker.slots['end_date'],
            "end_date_half_day":tracker.slots['end_date_half_day']
            }
            headers = {'content-type': 'application/json'}
            post_data = requests.post(API_ENDPOINT, data = json.dumps(body),headers=headers)
            dispatcher.utter_template("utter_submit_leave_authorization", tracker, **tracker.slots)
            return []