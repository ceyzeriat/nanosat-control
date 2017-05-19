import pexpect
from mailing import Mailing
import hein
from param import param_all

class MailRec(hein.SocReceiver):
    def __init__(self, **kwargs):
        super(MailRec, self).__init__(**kwargs)
        self.terminal = None
        
    def _newconnection(self):
        return None
    
    def process(self, key, data):
        # we ignore everything except 'raw' and forward it directly to child terminal
        # without checking anything
        if (key == 'raw'):
            self.terminal.sendline(str(data))
            

child = pexpect.spawn('piccontrol')

MAILING_REC = MailRec(port = 49999, name = 'mailing', connect=True, connectWait=0.5, portname = 'mailingport', hostname = 'localhost')
MAILING_REC.terminal = child

child.interact()
