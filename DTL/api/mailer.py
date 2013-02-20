import os.path
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import smtplib

from . import Settings, Singleton

#------------------------------------------------------------
#------------------------------------------------------------
class Mailer(Singleton):
    '''Class to handle common mailing routines'''
    #------------------------------------------------------------
    def send_mail(self, subject, message):
        if not Settings.ENABLEMAILER :
            return
        messageHTML = '<pre>\n'
        #Just inherit the regular message formatting
        messageHTML += message + '</pre>'
        self._send(Settings.DISTROLIST,
                   Settings.CCDISTORLIST,
                   "[" + Settings.PKGNAME + "] - " + subject,
                   message,
                   messageHTML)

    #------------------------------------------------------------
    def _send(self, toAddrs, ccAddrs, subject, textMsg, htmlMsg, attachments, highImportance=0):
        '''Sends E-mails with the given information'''
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = Settings.SMTPUSER
        msgRoot['To'] = ', '.join(toAddrs)
        msgRoot['Cc'] = ', '.join(ccAddrs)
        if highImportance:
            msgRoot['Importance'] = "high"
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgAlternative.attach(MIMEText(textMsg))
        msgAlternative.attach(MIMEText(htmlMsg,'html'))

        for name, filePath in attachments.iteritems():
            msgAttachment = MIMEBase('application', "octet-stream")
            msgAttachment.set_payload( open(filePath,"rb").read() )
            Encoders.encode_base64(msgAttachment)
            msgAttachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filePath))
            msgRoot.attach(msgAttachment)

        # Send the email
        smtp = smtplib.SMTP()
        smtp.connect(Settings.SMTPSERVER)
        smtp.login(Settings.SMTPUSER, Settings.SMTPPASSWORD)
        smtp.sendmail(Settings.SMTPUSER, toAddrs, msgRoot.as_string())
        smtp.quit()