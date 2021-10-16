#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
This file is a part of heartvoices.org project.

The software embedded in or related to heartvoices.org
is provided under a some-rights-reserved license. This means
that Users are granted broad rights, including but not limited
to the rights to use, execute, copy or distribute the software,
to the extent determined by such license. The terms of such
license shall always prevail upon conflicting, divergent or
inconsistent provisions of these Terms. In particular, heartvoices.org
and/or the software thereto related are provided under a GNU GPLv3 license,
allowing Users to access and use the software’s source code.
Terms and conditions: https://www.goandtodo.org/terms-and-conditions

Created Date: Sunday September 26th 2021
Author: GO and to DO Inc
E-mail: heartvoices.org@gmail.com
-----
Last Modified: Saturday, October 16th 2021, 8:21:57 am
Modified By: GO and to DO Inc
-----
Copyright (c) 2021
"""


from supermemo2 import SMTwo
import numpy as np
import time
import datetime
import json
from twilio.rest import Client
import logging
from googleapiclient.discovery import build
from flaskapp.models.storages import (gs_users_existing, gs_users_calls,
                                      gs_health_metric_data)
from flaskapp.tools.utils import cleanup_phone_number, send_mail
from flaskapp.models.ivr_models import (User, PhoneNumber, HealthMetric,
                                        SmartReminder)
from flaskapp.settings import (GOOGLE_API_KEY, GOOGLE_CSE_ID,
                               GOOGLE_CSE_MAX_NUM,
                               TWILIO_MAIN_PHONE_NUMBER,
                               TWILIO_ACCOUNT_SID,
                               TWILIO_AUTH_TOKEN)


logger = logging.getLogger(__name__)


def out_bound_call(phone_number=''):
    """ Function for making outbound call

    :param phone_number: the phone number to call to, defaults to ''
    :type phone_number: str
    """

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # FIXME: I don't like hardcoded twilio flow ids; we need to
    # handle this somehow

    if not is_user_new(phone_number):
        logger.info(
            f"Put existing user to flow (id = FW66222e22d7301b1f1e0f02ca198c440a), \
            phone number: {phone_number}"
        )
        client.studio \
            .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
            .executions \
            .create(to=phone_number, from_=TWILIO_MAIN_PHONE_NUMBER)
    else:
        logger.info(
            f"Put new user to flow (id = FW21a0b56a4c5d0d9635f9f86616036b9c), \
            phone number: {phone_number}"
        )
        client.studio \
            .flows('FW21a0b56a4c5d0d9635f9f86616036b9c') \
            .executions \
            .create(to=phone_number, from_=TWILIO_MAIN_PHONE_NUMBER)


def call_flow(flow_sid, phone_number=''):
    """Function for calling any flow from Twilio Studio

    :param flow_sid: internal id of twilio flow
    :type flow_sid: str
    :param phone_number: a phone number to call to, defaults to ''
    :type phone_number: str, optional
    """

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if phone_number:
        if not is_user_new(phone_number):
            logger.info(
                    f"Put existing user to flow (id = {flow_sid}), \
                    phone number: {phone_number}"
                )

            execution = client.studio \
                .flows(flow_sid) \
                .executions \
                .create(to=phone_number, from_=TWILIO_MAIN_PHONE_NUMBER)

            # wait for getting data from studio flow
            client.studio.flows(flow_sid) \
                .executions(execution.sid) \
                .steps \
                .list(limit=20)
        else:
            logger.info(
                    f"Put new user to flow (id = FW66222e22d7301b1f1e0f02ca198c440a), \
                    phone number: {phone_number}"
                )
            client.studio \
                .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
                .executions \
                .create(to=phone_number, from_=TWILIO_MAIN_PHONE_NUMBER)
    else:
        logger.warning("Empty phone number provided;\
                       I am silent, but you should discover why...")


def profile_detail():
    """Function for gathering profile information from the Client
    """

    def logged_call_flow(flow_sid, phone_number, what):
        logger.info(f"Getting {what} from {phone_number}...")
        call_flow(flow_sid, phone_number)

    # FIXME: Should be moved to settings or somewhere else...
    call_flow_mapper = {
        'dob':    "FWa23b5f2570ae23e2e1d68448378af0d0",
        'gender': "FWa23b5f2570ae23e2e1d68448378af0d0",

        'weight': "FW6661af875fa71bfcc36030d653e745ec",
        'height': "FW6661af875fa71bfcc36030d653e745ec",

        'activity': "FW8db981daac5317452c78944626de52ac",
        'hobby':    "FW8db981daac5317452c78944626de52ac",

        'time zone':  "FWac7f7be3dcc167fed511d4c08cf76f8c",
        'call time':  "FWac7f7be3dcc167fed511d4c08cf76f8c",

        'emergency phone': "FW21a0b56a4c5d0d9635f9f86616036b9c",
        'emergency name':  "FW21a0b56a4c5d0d9635f9f86616036b9c"
    }

    for row in gs_users_existing.get_all_records():
        phone_number = row.get('Phone Number')

        for feature_name, value in row.items():
            if not value:
                flow_sid = call_flow_mapper.get(feature_name, '')
                if flow_sid:
                    logged_call_flow(flow_sid, phone_number, feature_name)
            else:
                logger.info(f'Value of {feature_name} for {phone_number}:\
                    {value},  is already defined')


# FIXME: highly desirable to rename this function to something meaning...
# update_blood_pressure etc.
def call_to_check_bld():
    """Function for checking blood pressure and saving results to
    google spreadsheet
    """

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # FIXME: All hardcoded flow ids should be placed to settings
    # (or somewhere else) and called by human-readable names,
    # e.g. MY_FLOW_THAT_DO_SOMETHING = 'flow_id'

    execution = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions \
        .create(to='+16692419870', from_=TWILIO_MAIN_PHONE_NUMBER)

    steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps \
        .list(limit=20)

    # FIXME: I don't understand what 20 and 12 magic numbers mean;
    # These number should be defined in settings file,
    # and have meaningful names

    while len(steps) < 12:
        steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            .executions(execution.sid) \
            .steps \
            .list(limit=20)
        time.sleep(5)  # NOTE: Do we really need this?
        logger.info(f"The number of steps: {len(steps)}.")

    last_step_sid = steps[0].sid
    execution_step_context = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps(last_step_sid) \
        .step_context() \
        .fetch()

    # FIXME: I don't like 'UP' and 'DOWN' terms at all;
    systolic_blood_pressure = \
        execution_step_context.context['flow']['variables'].get('UP')
    diastolic_blood_pressure = \
        execution_step_context.context['flow']['variables'].get('DOWN')

    # NOTE: probably we need some validation systolic and diastolic
    # blood pressure values:
    # 1) systolic > diastolic ;
    # 2) systolic shouldn't be too low (e.g. 30 mm probably very low)
    # 3) diastolic shouldn't be very high;
    # 4) systolic shouldn't be very high, e.g. 250 mm is too high...

    # store data to gs-spreadsheet using proxy object
    gs_health_metric_data.append_row_to_sheet([
        json.dumps(datetime.datetime.now(),
                   indent=4, sort_keys=True, default=str),
        systolic_blood_pressure,
        diastolic_blood_pressure
    ])

    time.sleep(5)  # NOTE: Is this really necessary (not sure...)


def is_user_new(phone_number=''):
    """Check if the user already registered in the System

    :param phone_number: User's phone number, defaults to ''
    :type phone_number: str, optional
    :return: False if the user already registered and True otherwise
    :rtype: True or False
    """

    all_sheets = gs_users_existing.get_all_values()
    cleaned_phone_number = cleanup_phone_number(phone_number)
    return not any([True for a in all_sheets if cleaned_phone_number == a[0]])\
        or not PhoneNumber.select().where(
            PhoneNumber.number == cleaned_phone_number
        ).exists()


def save_new_user(phone_number='', tab=''):
    """Function for saving NEW user in google spreadsheet
    and ProstgreSQL database.

    Once objects are created this function sends notification email.

    :param phone_number: phone number, defaults to ''
    :type phone_number: str, optional
    :param tab: sheet name for google docs, defaults to ''
    :type tab: str, optional
    """

    cleaned_phone_number = cleanup_phone_number(phone_number)

    # --- store data to google spreadsheet ( TODO: drop gs support)
    gs_proxy_sheet = gs_users_existing if tab.lower() == 'existing'\
        else gs_users_calls

    # FIXME: Awkward and hardcoded values in new_row variable (changes needed)
    new_row = [
        cleaned_phone_number, '', '', '', '', '', '', '', '', '', '', '',
        json.dumps(datetime.datetime.now(), indent=4, sort_keys=True,
                   default=str), '19258609793', '19258609793'
    ]

    gs_proxy_sheet.append_row_to_sheet(new_row)
    logger.info("Informational row about new user"
                f"added to gspread: sheetname=({tab})")

    # --- store new user and related call
    try:
        phone_obj = PhoneNumber.get_or_create(
            number=cleaned_phone_number
        )
        user_obj = User.get_or_create(phone_number=phone_obj)
        logger.info(f"User object ({user_obj.id}) and "
                    f"corresponding phone object ({phone_obj.id})"
                    f"are created (phone: {phone_number}).")
    except Exception as e:
        logger.error(f"Exception raised during DB operation: {e}")
    logger.info(f"Sending notification email for phone num.={phone_number}.")
    send_mail("NEW USER", phone=phone_number)
    logger.info(f"Notification email for phone num.={phone_number} was sent.")


def save_data_to_postgres(
        feature_name,
        value,
        phone_number,
        date=datetime.datetime.now()
):
    """Save data to Prostgres database

    if feature_name is a field name of User model,
    function override its value with new (value);
    otherwise, it create related HealthMetric object
    and save data to its bson field (data field).

    :param feature_name: feature name to be saved
    :type feature_name: str
    :param value: feature value to be stored
    :type value: Any
    :param phone_number: user's phone number
    :type phone_number: str
    """

    query = \
        PhoneNumber.select().join(User).where(
            PhoneNumber.number == phone_number
        )

    if query.exists():
        first_occurrence = query.first()

        # If feature_name is in User's field names, write its immediately
        if feature_name in User._meta.sorted_field_names:
            logger.info(
                "Feature name is in User model; its value will be overriden. "
                f"{feature_name} = {value}; phone_number = {phone_number}"
            )
            setattr(first_occurrence.user, feature_name, value)
            first_occurrence.user.save()
            return

        health_metric = HealthMetric.select().where(
            (HealthMetric.user == first_occurrence.user) &
            (HealthMetric.created == date)
        )

        if health_metric.exists():
            health_obj = health_metric.first()
        else:
            health_obj = HealthMetric.create(user=first_occurrence.user)
            if date:
                health_obj.created = date

        bson_field = health_obj.data
        if bson_field and bson_field.get(feature_name, None) is not None:
            raise ValueError(f"Feature {feature_name} already defined "
                             f"for phone={phone_number} for date={date}.")
        elif bson_field is not None:
            bson_field[feature_name] = value
        else:
            bson_field = {feature_name: value}
        health_obj.data = bson_field
        health_obj.save()

    else:
        logger.error(f"Phone number ({phone_number}) is unknown;"
                     f"couldn't associate data: {feature_name} = {value}.")


def save_data(col_name, value, phone_number, date=None):
    """Function for saving data to google spreadsheet

    :param col_name: column name in google spreadsheet
    :type col_name: str
    :param value: value to be stored
    :type value: str
    :param phone_number: user's phone number
    :type phone_number: str
    """

    phone_number = cleanup_phone_number(phone_number)

    # TODO: gs-support should be dropped
    all_data = gs_users_existing.get_all_records()
    all_data = np.array(all_data)
    phone_num_index = np.argmax(all_data[:, 0] == phone_number)
    col_name_index = np.argmax(all_data[0, :] == col_name)
    gs_users_existing.update_cell(phone_num_index, col_name_index, value)

    save_data_to_postgres(
        col_name,
        value,
        phone_number,
        date=date or datetime.datetime.now()
    )


def google_search(search_term):
    """ Search a term using Google Custom Search Engine

    :param search_term: a term to search for;
    :type search_term: str

    NOTE
    ----
        see: https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list   # noqa: E501
    """

    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(
        q=search_term,
        cx=GOOGLE_CSE_ID,
        num=GOOGLE_CSE_MAX_NUM
    ).execute()
    return res.get('items', '')


def update_reminder(id):
    """Update reminder by id

    :param id: reminder's id
    :type id: int
    """

    # get smart reminder by ID
    smart_reminder = SmartReminder.get(SmartReminder.id == id)

    if smart_reminder.last_time is None:
        # first review
        review = SMTwo.first_review(3)
    else:
        # next review
        review = SMTwo(
            smart_reminder.easiness,
            smart_reminder.interval,
            smart_reminder.repetitions
        ).review(3)

    logger.info(f"Review: {review}")
    smart_reminder.interval = review.interval
    smart_reminder.easiness = review.easiness
    smart_reminder.repetitions = review.repetitions
    smart_reminder.last_time = datetime.datetime.now()
    smart_reminder.next_time = review.review_date
    smart_reminder.save()
