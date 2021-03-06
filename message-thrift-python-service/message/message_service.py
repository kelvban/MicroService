import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from message.api import MessageService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender="imoocd@163.com"
authCode="aA111111"
class MessageServiceHandler:
    def sendEmailMessage(self, email, message):
        print("Send to:"+email+",Message:"+message)
        messageObj=MIMEText(message,"plain","utf-8")
        messageObj['From']=sender
        messageObj['To']=email
        messageObj['Subject']=Header('测试邮件','utf-8')
        try:
            smtpObj=smtplib.SMTP('smpt.163.com')
            smtpObj.login(sender,authCode)
            smtpObj.sendmail(sender,[email],messageObj.as_string())
            print("Send Email Success!")
            return True
        except smtplib.SMTPException as e:
            print("Send Email Failed!")
            print(e)
            return False

if __name__=='__main__':
    handler=MessageServiceHandler()
    processor=MessageService.Processor(handler)
    transport=TSocket.TServerSocket("127.0.0.1","9090")
    tfactory=TTransport.TFramedTransportFactory()
    pfactory=TBinaryProtocol.TBinaryProtocolFactory()

    server=TServer.TSimpleServer(processor,transport,tfactory,pfactory)
    print("Message Service Start!")
    server.serve()
    print("Message Service Exit!")

