# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Send emails """

import base64
import locale
import os
from email.mime.text import MIMEText

# script settings
from gamer.emails.gmail import GMailApiOAuth, send_email

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
OAUTH_FOLDER = os.path.join(THIS_FOLDER, ".user_credentials", "gmail")

# email settings
EMAIL_DRIVER = GMailApiOAuth(
    "GAME",
    os.path.join(OAUTH_FOLDER, "client_secret.json"),
    os.path.join(OAUTH_FOLDER, "gmail.json")
).create_driver()
EMAIL_SENDER = "game.cosmosns@gmail.com"

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


def notify_user(raw_message, recipient, subject):
    """
    :param recipient: str
        Email of recipient
    :param raw_message: str
        HTML message
    :return: bool
        True iff successful notification
    """

    raw_message += "<br><br>With <3, the GAME team"
    raw_message = "Hi!<br><br>" + raw_message
    msg = get_msg(recipient, raw_message, subject)
    send_msg(msg)
    return True


def notify_user_of_start(recipient):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    msg = "Your GAME models are on their way! " \
          "This email has been sent just to notify you that all files have" \
          " been parsed correctly and your results are coming.<br>" \
          "You will receive another email with the link to download your " \
          "results. As of now, have a nice day!" \
          "<br>" \
          "Bye!"
    return notify_user(msg, recipient, "GAME | start")


def notify_user_of_end(recipient, success, output_file,
                       debug_file, extra_output):
    """
    :param recipient: str
        Email of recipient
    :param output_file: str
        Path to output file
    :param extra_output: str
        Path to output file with additional labels
    :return: bool
        True iff successful notification
    """

    if success:
        msg = "Your GAME models have run successfully!<br>"
    else:
        msg = "Sorry, but we encountered some errors while running your " \
              "models.<br>"

    msg += "Here are your output files:<br>" \
           "<ul>" \
           "<li><a href='" + str(debug_file) + "'>debug file</a></li>" \
                                               "<li><a href='" + str(
        output_file) + "'>output file</a></li>"

    if extra_output is not None:
        msg += "<li><a href='" + str(
            extra_output) + "'>additional output file</a></li>"

    msg += "</ul><br>"
    msg += "Make sure to download these files as soon as possible because we " \
           "they will be erased within two weeks!<br>" \
           "Hoping the results match your predictions ... see you soon!"

    return notify_user(msg, recipient, "GAME | your results")
