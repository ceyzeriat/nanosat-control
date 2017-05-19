import imaplib
import email 
import time
import hein
import threading

AUTHORIZED_SENDERS = ['picsat@laposte.net', '"nowak mathias" <mathias.nowak@obspm.fr>']
IMAP_SERVER = 'imap.laposte.net'
LOGIN = 'picsat@laposte.net'
PASSWORD = 'BetaPictoris386'

DELETE_MAILS = True

LOOP_PERIOD = 2 # in s

COMMAND_ALIASES = dict([])
lines = open('command_easy_aliases.txt', 'r').readlines()
for line in lines:
    line = ''.join(line.replace('\r', '\n').split('\n'))
    aliases = line.split(';')
    for a in aliases:
        COMMAND_ALIASES[a] = aliases[0]


class Mailing(object):
    def __init__(self):
        self.box = imaplib.IMAP4_SSL(IMAP_SERVER)
        self.running = False
        self.transmitter = hein.SocTransmitter(port = 49999, nreceivermax = 1, start = False, portname = 'mailingport')
        self.accept_mail = True
        self.thread = threading.Thread(target = self.run, args = ())
        self.thread.daemon = True

    def _openBox(self):
        self.box.list()
        self.box.select('inbox')

    def _closeBox(self):
        self.box.expunge()        
        self.box.close()

    def _reportMessage(self, msg):
        print('Got new mail from '+msg['from']) 
        return None       


    def getMailIds(self, which):
        (result, data) = self.box.search(None, which)
        ids = data[0].split()
        return ids        

    def processId(self, mailId, delete = False):
        (res, data) = self.box.fetch(mailId, "(RFC822)") # get new mail
        raw_mail = data[0][1]
        if (delete == True):
            self.box.store(mailId, '+FLAGS', '\\Deleted')
        self.processMail(raw_mail)

    def sendCommand(self, command_string):
        self.transmitter.tell_raw(command_string + '\n')
        
    def _executionAuthorized(self, msg):
        res = False
        try:
             res = (msg['from'] in AUTHORIZED_SENDERS) & (msg['subject'] == 'picsat')
        except:
            pass
        return res
        
    def processMail(self, raw_mail):
        msg = email.message_from_string(raw_mail)
        self._reportMessage(msg)        
        if self._executionAuthorized(msg):
            print('forwarding command to control')
            command = msg.get_payload().replace('\r', '\n').split('\n')
            command[:] = [c.rstrip() for c in command if c != '']
            if COMMAND_ALIASES.has_key(command[0]):
                command_string = 'c1.' + COMMAND_ALIASES[command[0]]
                k = 1
                while k<len(command):
                    line = command[k].split()
                    line[:] = [l for l in line if l != '']
                    if len(line) == 2:
                        command_string = command_string + '(' + line[0] + ' = ' + line[1]
                    k = k+1
                command_string = command_string + ')'
                self.sendCommand(command_string)
            else:
                print(command[0] + ' not found')
        else:
            print('ignoring')
                    
            
    def run(self):
        while(self.running == True):
            if (self.accept_mail == True):
                self._openBox()
                ids = self.getMailIds('ALL')
                for mailId in ids:
                    self.processId(mailId, delete = DELETE_MAILS)
                self._closeBox()
            time.sleep(LOOP_PERIOD)

    def start(self):
        self.transmitter.start()
        self.running = True
        self.box.login(LOGIN, PASSWORD)                        
        self.thread.start()

    def stop(self):
        self.running = False
        self.box.logout()





        





        


        
        
