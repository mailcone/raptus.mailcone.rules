import json
import grok

from zope.i18n import translate

from raptus.mailcone.core import utils

from raptus.mailcone.rules import _
from raptus.mailcone.rules import interfaces



class BaseFactory(grok.Adapter):
    grok.baseclass()
    grok.context(interfaces.IRuleset)

    order = 0

        
    @property
    def metadata(self):
        di = dict(input=self.box_input(),
             output=self.box_output(),
             title = self.box_title(),
             buttons = self.box_buttons())
        return json.dumps(di)

    def box_title(self):
        return self._translate(self.title)
    
    def box_input(self):
        return list()
    
    def box_output(self):
        return list()
    
    def box_buttons(self):
        li = list()
        li.append(dict(icon='ui-icon-trash',
                       title=self._translate(_('delete rule element')),
                       cssclass='ui-button ui-modal-minsize',
                       ajax=self.box_delete()))
        li.append(dict(icon='ui-icon-pencil',
                       title=self._translate(_('edit rule element')),
                       cssclass='ui-button',
                       ajax=self.box_edit()))
        return li
    
    def box_delete(self):
        return '%s/wireit_delete' % grok.url(utils.getRequest(), self.context)

    def box_edit(self):
        return '%s/wireit_edit' % grok.url(utils.getRequest(), self.context)

    def _translate(self, msg):
        return translate(msg, context=utils.getRequest())


class InputFactory(BaseFactory):
    grok.name('raptus.mailcone.rules.input')
    grok.implements(interfaces.IInputItemFactory)
    
    
    title = _('Input')
    description = _('All mails came through the Input Element')

    def box_output(self):
        li = list()
        li.append(dict(title=self._translate(_('mailoutput')) ))
        return li


class InputCustomerFactory(BaseFactory):
    grok.name('raptus.mailcone.rules.inputcustomer')
    grok.implements(interfaces.IInputItemFactory)
    
    
    title = _('Input Customer')
    description = _('All mails for each customer came in through the Input Element')

    def box_output(self):
        li = list()
        li.append(dict(title=self._translate(_('mailoutput')) ))
        return li
    
