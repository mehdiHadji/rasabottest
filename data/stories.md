## happy path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## unhappy path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* chitchat
    - utter_chitchat
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## very unhappy path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* chitchat
    - utter_chitchat
    - certificate_form
* chitchat
    - utter_chitchat
    - certificate_form
* chitchat
    - utter_chitchat
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* stop
    - utter_ask_continue
* affirm
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop and really stop path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## chitchat stop but continue path
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* chitchat
    - utter_chitchat
    - certificate_form
* stop
    - utter_ask_continue
* affirm
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue and chitchat path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* stop
    - utter_ask_continue
* affirm
    - certificate_form
* chitchat
    - utter_chitchat
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat stop but continue and chitchat path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* chitchat
    - utter_chitchat
    - certificate_form
* stop
    - utter_ask_continue
* affirm
    - certificate_form
* chitchat
    - utter_chitchat
    - certificate_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat, stop and really stop path
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
* chitchat
    - utter_chitchat
    - certificate_form
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## Generated Story 3490283781720101690 (example from interactive learning, "form: " will be excluded from training)
* greet
    - utter_greet
* request_certificate
    - certificate_form
    - form{"name": "certificate_form"}
    - slot{"requested_slot": "certif_type"}
* chitchat
    - utter_chitchat  <!-- certificate_form was predicted by FormPolicy and rejected, other policy predicted utter_chitchat -->
    - certificate_form
    - slot{"requested_slot": "certif_type"}
* form: inform{"certif_type": "work certificate"}
    - slot{"certif_type": "work certificate"}
    - form: certificate_form
    - slot{"certif_type": "work certificate"}
    - slot{"requested_slot": "period"}
* form: inform{"date": "tomorrow"}
    - form: certificate_form
    - slot{"period": "2"}
    - slot{"requested_slot": "langue"}
* chitchat
    - utter_chitchat
    - certificate_form
    - slot{"requested_slot": "langue"}
* stop
    - utter_ask_continue
* affirm
    - certificate_form  <!-- FormPolicy predicted FormValidation(False), other policy predicted certificate_form -->
    - slot{"requested_slot": "langue"}





* form: affirm
    - form: certificate_form
    - slot{"langue": true}
    - slot{"requested_slot": "purpose"}
* form: inform
    - form: certificate_form
    - slot{"purpose": "/inform"}
    - slot{"requested_slot": "details"}
* form: inform{"details": "need it for a matter"}
    - slot{"details": "need it for a matter"}
    - form: certificate_form
    - slot{"details": "need it for a matter"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## bot challenge
* bot_challenge
  - utter_iamabot
