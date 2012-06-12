from zope.i18n import translate

from raptus.mailcone.core import utils





class RuleItemException(Exception):

    def __init__(self, message, ruleitem):
        msg = 'Error in ruleitem "%s": %s' % (ruleitem.title, translate(self.message, context=utils.getRequest()),)
        super(RuleItemException, self).__init__(msg)
        self.message = message
        self.ruleitem = ruleitem



