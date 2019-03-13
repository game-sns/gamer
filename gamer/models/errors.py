# -*- coding: utf-8 -*-


from enum import Enum


class GamerErrorsCode(Enum):
    # network: 260 - 269
    NETWORK = 260  # general

    # emails
    EMAIL = 261
    EMAIL_NOT_WELL_FORMAT = 262


class GamerException(Exception):
    OUTPUT_FORMAT = '{} (code {})'
    EMAIL_EXCEPTION_FORMAT = 'Cannot send email to {}'

    def __init__(self, message, ref_code):
        """
        :param message: explain code
        :param ref_code: reference code of error. Use the following table:
        - codes between (including) 210 and 219: files errors
        - codes between (including) 220 and 229: system (cpu, memory) errors
        """

        super(GamerException, self).__init__(message)
        self.ref_code = int(ref_code)

    def __str__(self):
        return self.OUTPUT_FORMAT.format(self.message, self.ref_code)

    @staticmethod
    def build(message, code):
        return GamerException(message, code)

    @staticmethod
    def build_network_exception(message):
        return GamerException(message, GamerErrorsCode.NETWORK)

    @staticmethod
    def build_email_exception(email_address):
        message = GamerException.EMAIL_EXCEPTION_FORMAT.format(email_address)
        return GamerException(message, GamerErrorsCode.EMAIL)
