from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import datetime
import requests
import json
from datetime import datetime, date


def validate_date(date_input,marge):
    dep_dat = datetime.fromisoformat(date_input)
    now = datetime.now()
    t1 = date(year = dep_dat.year, month = dep_dat.month, day = dep_dat.day)
    t2 = date(year = now.year, month = now.month, day = now.day)
    delta = t1 - t2
    if delta.days > marge or delta.days < 0:
        return False
    else:
        return True


def validate_period_date(date_deb, date_end):
    dep_dat = datetime.fromisoformat(date_deb)
    end_dat = datetime.fromisoformat(date_end)
    t1 = date(year = dep_dat.year, month = dep_dat.month, day = dep_dat.day)
    t2 = date(year = end_dat.year, month = end_dat.month, day = end_dat.day)
    delta = t2 - t1
    if delta.days >= 0:
        return True
    else:
        return False


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


    def validate_dep_date(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        if validate_date(value,30):
            return {"dep_date": value}
        else:
            dispatcher.utter_template("utter_wrong_dep_date", tracker)
            return {"dep_date": None}


    def validate_end_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if validate_period_date(tracker.slots['dep_date'],value):
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
            print('#####################')
            print('#####################')
            print('#####################')
            print('#####################')
            dispatcher.utter_template("utter_submit_work_salary_certificate", tracker, **tracker.slots)
            return []
        
        if certificate_type == "expense report":
            dispatcher.utter_template("utter_submit_expense_report", tracker, **tracker.slots)
            return []
        
        if certificate_type == "mission order":
            dispatcher.utter_template("utter_submit_mission_order", tracker, **tracker.slots)
            return []
        
        if certificate_type == "leave authorization":
            dispatcher.utter_template("utter_submit_leave_authorization", tracker, **tracker.slots)
            return []