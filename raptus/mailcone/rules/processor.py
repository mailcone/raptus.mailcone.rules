import logging
from megrok import rdb

from zope import component
from datetime import datetime

from raptus.mailcone.mails.contents import Mail
from raptus.mailcone.persistentlog.logger import PersistentLogHandler
from raptus.mailcone.persistentlog.interfaces import ILogContainerLocator
from raptus.mailcone.rules import interfaces





logger = logging.getLogger('raptus.mailcone.rules')
handler = PersistentLogHandler(u'cronjob', ILogContainerLocator)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
handler.setLevel(0)
logger.addHandler(handler)

def process():
    logger.info('starting rule process')
    charter = MailCharter()
    for container in component.getUtility(interfaces.IRulesetContainerLocator)().objects():
        for input in container.objects():
            if interfaces.IInputItem.providedBy(input):
                input.process(charter.copy())
    #charter.markAsProcessed()
    logger.info('%s mails marked as processed' % len(charter.mails))
    handler.persist()
    


class MailCharter(object):
    
    customer = None
    mails = list()
    
    
    def __init__(self, mails=None):
        if mails is None:
            session = rdb.Session()
            self.mails = session.query(Mail).filter(Mail.processed_on == None).all()
            logger.info('%s mails selected and read to be processed' % len(self.mails))
        else:
            self.mails = mails
    
    def markAsProcessed(self):
        for mail in self.mails:
            mail.processed_on = datetime.now()
    
    def copy(self, mails=None):
        if mails is None:
            mails = self.mails + []
        else:
            mails = mails
        inst = self.__class__(mails)
        return inst


