from flask import Blueprint
from flaskapp.view_functions.ivrflow import (
    username,
    check_client_type,
    save_client_type,
    call_to_friend,
    find_friend_timezone,
    end_call,
    call_to_operator,
    save_blood_pressure,
    save_feedback_service,
    save_feedback,
    search,
    get_next_reminder,
    voice_joined,
    voice,
    after_call,
    get_term_cond,
    get_privacy,
    get_profile
)
IVRFlow=Blueprint('IVRFlow',__name__)

IVRFlow.route("/voice_joined", methods=['GET', 'POST'])(voice_joined)
IVRFlow.route("/voice", methods=['GET', 'POST'])(voice)
IVRFlow.route("/after_call", methods=['GET', 'POST'])(after_call)
IVRFlow.route("/username", methods=['GET', 'POST'])(username)
IVRFlow.route("/check_client_type", methods=['GET', 'POST'])(check_client_type)
IVRFlow.route("/save_client_type", methods=['GET', 'POST'])(save_client_type)
IVRFlow.route("/call_to_friend", methods=['GET', 'POST'])(call_to_friend)
IVRFlow.route("/find_friend_timezone", methods=['GET', 'POST'])(find_friend_timezone)
IVRFlow.route('/end_call', methods=['GET', 'POST'])(end_call)
IVRFlow.route("/call_to_operator", methods=['GET', 'POST'])(call_to_operator)
IVRFlow.route("/save_blood_pressure", methods=['GET', 'POST'])(save_blood_pressure)
IVRFlow.route("/save_feedback_service", methods=['GET', 'POST'])(save_feedback_service)
IVRFlow.route("/save_feedback", methods=['GET', 'POST'])(save_feedback)
IVRFlow.route("/search", methods=['GET', 'POST'])(search)
IVRFlow.route("/get_next_reminder", methods=['GET', 'POST'])(get_next_reminder)
IVRFlow.route("/term_cond", methods=['GET', 'POST'])(get_term_cond)
IVRFlow.route("/privacy", methods=['GET', 'POST'])(get_privacy)
IVRFlow.route("/authenticate/get_profile", methods=['GET', 'POST'])(get_profile)
