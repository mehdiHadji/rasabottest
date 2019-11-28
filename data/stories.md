## certif path1
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
* thankyou
    - utter_noworries
* goodbye
  - utter_goodbye
  - action_restart


## certif path2
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
* thankyou
    - utter_noworries
* goodbye
  - utter_goodbye
  - action_restart


## certif path3
* greet
    - utter_greet
* request_unknown_certificate
    - utter_ask_certif_type
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
* thankyou
    - utter_noworries
* goodbye
  - utter_goodbye
  - action_restart


## certif path 4
* greet
  - utter_greet
* request_unknown_certificate
    - utter_ask_certif_type
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
    - utter_did_that_help
* deny
  - utter_ask_again
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
    - utter_did_that_help
* affirm
  - utter_noworries
* goodbye
  - utter_goodbye


## goodbye path
* goodbye
  - utter_goodbye
  - action_restart


## fallback
- utter_unclear