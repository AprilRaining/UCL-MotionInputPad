import os
import json
import sys
import win32com.client as client
import win32com
import smtplib
import imapclient
from imapclient import SEEN, FLAGGED
import pyzmail
import time
import traceback

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from text_to_speech.text_to_speech import SpeechIBM

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config_exe.json')) as path_file:
    configs = json.load(path_file)


class MailOperation(object):
    def __init__(self):
        self.smtpserver = configs['SMTP']['server']
        self.port = configs['SMTP']['port']
        self.email = configs['SMTP']['email']
        self.password = configs['SMTP']['password']
        self.smtpobj = smtplib.SMTP(self.smtpserver, self.port)
        self.smtpobj.ehlo()
        self.smtpobj.starttls()
        self.smtpobj.login(self.email, self.password)

        self.imapserver = configs['IMAP']['server']
        self.imapobj = imapclient.IMAPClient(self.imapserver)
        self.imapobj.login(self.email, self.password)
        self.speech = SpeechIBM()

        # print( self.smtpobj.login(self.email, self.password))
        # print(self.smtpobj.ehlo())
        # print(self.smtpobj)

    def sendemail(self, to, subject, text):
        main_text = 'Subject: ' + subject + '\n\r' + text
        self.smtpobj.sendmail(self.email, to, main_text)

    def search_email_uid(self, email_type="INBOX", keywords=None):
        if email_type not in ["INBOX", "Sent", "Drafts", "Deleted", "Junk"]:
            self.speech.speech("Wrong Type of email, input again please.")
        self.imapobj.select_folder(email_type, readonly=False)
        if not keywords:
            return self.imapobj.search()
        else:
            return self.imapobj.search(keywords)

    def fetch_messages(self, uids):
        rawMessages = self.imapobj.fetch(uids, ['BODY[]'])
        count = 1
        for id, rawMessage in rawMessages.items():
            message = pyzmail.PyzMessage.factory(rawMessage[b'BODY[]'])
            subject = message.get_subject()
            from_text = message.get_addresses('from')[0][0]
            # print(id, message)
            to_text = ""
            # print(message.get_addresses('to'))
            for to_address in message.get_addresses('to'):
                to_text += to_address[0]
                to_text += ", "

            cc_text = ""
            # print(message.get_addresses('cc'))
            for cc_ in message.get_addresses('cc'):
                cc_text += cc_[0]
                cc_text += ", "

            bcc_text = ""
            for bcc_ in message.get_addresses('bcc'):
                bcc_text += bcc_[0]
                bcc_text += ", "

            voice_text = f"{ordinal(count)} email: The subject is {subject}, from {from_text} to {to_text} "
            if len(cc_text):
                voice_text += f"carbon copy to {cc_text} "
            if len(bcc_text):
                voice_text += f"blind carbon copy to {bcc_text} "

            voice_text += " main text is, "
            main_text = message.text_part.get_payload().decode(message.text_part.charset)

            self.speech.speech(voice_text + main_text)
            # self.imapobj.set_flags(id, "Unseen")
            # print(id, self.imapobj.get_flags(id))
            #
            # if count >= 2:
            #     return

            count += 1


def ordinal(num):
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix






if __name__ == '__main__':
    mail = MailOperation()
    # for i in range(10):
    #     mail.sendemail('LPChen_test@outlook.com', 'test_email' + str(i),
    #                    "This is a test email. \n The second line \n\nBest wishes,\nLingpeng")
    # print(mail.search_email_uid())
    # mail.fetch_messages(mail.search_email_uid(keywords=['UNSEEN']))
    mail.fetch_messages(mail.search_email_uid())

