
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib
import time
from RssToKindle.settings import EMAILSERVER

#Send the attachment to the appointed e-mail account
def MailToKindle(name, to, title, attachment):
    msg = MIMEMultipart()
    
    att1 = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = "attachment; filename=title"
    msg.attach(att1)    
    
    msg['to'] = to
    msg['from'] = name
    msg['subject'] = 'convert'
    
    for i in range(10):
        try:
            server = smtplib.SMTP(EMAILSERVER['ADDRESS'],EMAILSERVER['PORT'])
            print "connect to smtp server"
            server.set_debuglevel(1)
            server.connect(EMAILSERVER['ADDRESS'],port=EMAILSERVER['PORT'])
            server.login(EMAILSERVER['USERNAME'],EMAILSERVER['PASSWORD'])
        
            server.sendmail(msg['from'], msg['to'],msg.as_string())
            server.quit()
            print 'succeed to send mail'
        except Exception, e:  
            if i < 10:
                time.sleep(5)                
            else:
                break


if __name__ == '__main__':
    MailToKindle('emma', 'agnes.ping_18@kindle.cn', 'kindletest', 'c:\\123.txt')



