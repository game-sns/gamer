from gamer.mailer import get_msg, send_msg


def notify_user(raw_message, recipient, subject):
    """
    :param recipient: str
        Email of recipient
    :param raw_message: str
        HTML message
    :return: bool
        True iff successful notification
    """

    try:
        raw_message += "</br></br>With <3 the GAME team"
        msg = get_msg("sirfoga@protonmail.com", raw_message, subject)
        send_msg(msg)
        return True
    except Exception as e:
        print(
            "Cannot send email to",
            recipient,
            "with message\n```\n", raw_message, "\n```\nbecause of", e
        )

    return False


def notify_user_of_start(recipient):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    msg = "Hi!</br>" \
          "Your GAME models are on their way!</br>" \
          "This email has been sent just to notify you that all files have" \
          "been parsed correctly and your results are coming.</br>" \
          "You will receive another email with the link to download your " \
          "results. As of now, have a nice day!" \
          "</br>" \
          "Bye!"
    return notify_user(msg, recipient, "GAME | start")


def notify_user_of_end(recipient, success, output_file,
                       debug_file, extra_output=None):
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

    msg = "Hi!</br>"
    if success:
        msg += "Your GAME models have run successfully!</br>"
    else:
        msg += "Sorry, but we encountered some errors while running your " \
               "models.</br>"

    msg += "Here are your output files:</br>" \
           "<ul>" \
           "<li><a href='" + str(debug_file) + "'>debug file</a></li>" \
                                               "<li><a href='" + str(
        output_file) + "'>output file</a></li>"

    if extra_output:
        "<li><a href='" + str(
            extra_output) + "'>additional output file</a></li>"

    msg += "</ul></br>"
    msg += "Make sure to download these files as soon as possible because we " \
           "they will be erased within two weeks!</br>" \
           "Hoping the results match your predictions ... see you soon!"

    return notify_user(msg, recipient, "GAME | your results")
