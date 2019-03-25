# !/usr/bin/python2
# coding: utf-8


""" Send emails """

import base64
import datetime
import json
import locale
import os
from email.mime.text import MIMEText

# script settings
from gamer.emails.gmail import GMailApiOAuth, send_email
from models.errors import GamerException, GamerErrorsCode

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
OAUTH_FOLDER = os.path.join(THIS_FOLDER, ".user_credentials", "gmail")
CONFIG_FOLDER = os.path.join(THIS_FOLDER, "config")

# email settings
EMAIL_DRIVER = GMailApiOAuth(
    "GAME",
    os.path.join(OAUTH_FOLDER, "client_secret.json"),
    os.path.join(OAUTH_FOLDER, "gmail.json")
).create_driver()
EMAIL_SENDER = "game.cosmosns@gmail.com"
ADMIN_CONFIG_FILE = os.path.join(CONFIG_FOLDER, 'admins.json')
ADMIN_CONFIG = json.load(open(ADMIN_CONFIG_FILE, 'r'))
HELP_EMAIL = ADMIN_CONFIG[0]
# todo hooks for ["on_download", "on_missing_additional", "on_chunks"] events

# setting locale
locale.setlocale(locale.LC_ALL, "it_IT.UTF-8")  # italian


def get_msg(recipient, html_content, subject):
    """
    :return: MIMEText
        Personalized message to notify user
    """

    message = MIMEText(
        "<html>" + html_content + "</html>", "html"
    )
    message["subject"] = subject
    message["to"] = str(recipient).strip()

    return {
        "raw": base64.urlsafe_b64encode(bytes(message)).decode()
    }


def send_msg(msg):
    """
    :param msg: str
        Message to send to me
    :return: void
        Sends email to me with this message
    """

    send_email(
        EMAIL_SENDER,
        msg,
        EMAIL_DRIVER
    )


def notify_user(raw_message, recipient, name_surname, subject):
    """
    :param raw_message: str
        HTML message
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    raw_message = "Dear {},</br></br>".format(name_surname) + raw_message
    raw_message += "</br></br>Regards,</br></br>GAME developers",  # end

    try:
        msg = get_msg(recipient, raw_message, subject)
    except:
        exception = GamerException.build('Cannot build email',
                                         GamerErrorsCode.EMAIL_NOT_WELL_FORMAT)
        raise exception

    try:
        send_msg(msg)
    except:
        exception = GamerException.build_email_exception(recipient)
        raise exception

    return True


def notify_user_of_start(recipient, name_surname):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    msg = "GAME has started crunching your input. " \
          "This email has been sent just to notify you that all files have" \
          " been parsed correctly and the results are being computed.</br>" \
          "You will receive another email with the link to download the " \
          "output. As of now, have a nice day!"
    return notify_user(msg, recipient, name_surname, "GAME | start")


def notify_user_of_missing_additional(recipient, name_surname):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    msg = "This email is just a notification that the additional files will " \
          "be missing: this is because it would require too much memory. When " \
          "done, we'll email you again with the link to download the output " \
          "files. "
    return notify_user(msg, recipient, name_surname, "GAME | additional files")


def notify_user_of_chunks(recipient, name_surname, n_chunks):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    link_to_readme = 'https://game.sns.it/static/data/readme_GAME.pdf'
    msg = "GAME tried to crunch your files but encountered an error. In " \
          "particular it seems that the input files did not follow the " \
          "guidelines specified in the <a href='{}'>README</a>. We advise to " \
          "split your input files into {} chunks." \
        .format(link_to_readme, n_chunks)
    return notify_user(msg, recipient, name_surname, "GAME | input error")


def notify_user_of_end(recipient, name_surname, success, out_link):
    if success:
        msg = "GAME completed successfully. You can download the output files " \
              "<a href='{}'>here</a>.</br>The link will expire in {} " \
              "days: please be sure to download the output!" \
            .format(out_link, 10)
    else:
        msg = "GAME did not complete: an unknown error occurred. Please " \
              "contact <a href='mailto:{}'>{}</a>." \
            .format(HELP_EMAIL['EMAIL'], HELP_EMAIL['name'])

    return notify_user(msg, recipient, name_surname, "GAME | your results")


def notify_admins(user_email, user_name, user_school, event):
    for admin in ADMIN_CONFIG:
        if event in admin['events']:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user = '{} ({} of {})'.format(
                user_name, user_email, user_school
            )

            if event == 'on_start':
                msg = 'At {} GAME started running input submitted by {}.' \
                    .format(now, user)
            elif event == 'on_fail':
                msg = 'At {} GAME failed running input submitted by {}!' \
                    .format(now, user)
            elif event == 'on_success':
                msg = 'At {} GAME completed input submitted by {}.' \
                    .format(now, user)
            elif event == 'on_download':
                msg = 'At {} {} downloaded output.' \
                    .format(now, user)
            elif event == 'on_missing_additional':
                msg = 'At {} GAME removed additional option from input ' \
                      'submitted by {}.' \
                    .format(now, user)
            elif event == 'on_chunks':
                msg = 'At {} GAME failed: input submitted by {} has to be ' \
                      'chunked!' \
                    .format(now, user)
            else:  # shouldn't arrive here
                msg = 'At {} something happened relative to {}' \
                    .format(now, user)

            notify_user(
                msg, admin['email'], admin['name'],
                "GAME admin | {} event".format(event)
            )
