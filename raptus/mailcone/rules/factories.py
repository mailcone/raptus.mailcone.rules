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
    form_fields = []
    override_properties_ignors = ['title', 'description']

        
    @property
    def metadata(self):
        di = dict(input=self.box_input(),
             output=self.box_output(),
             title = self.box_title(),
             buttons = self.box_buttons(),
             identifer=self.identifier())
        return json.dumps(di)

    def box_title(self):
        return self._translate(self.title)
    
    def box_input(self):
        return list()
    
    def box_output(self):
        return list()
    
    def box_buttons_save(self):
        return dict(   icon='ui-icon-pencil',
                       title=self._translate(_('edit rule element')),
                       cssclass='ui-button',
                       ajax=self.box_edit())
    
    def box_buttons_delete(self):
        return dict(   icon='ui-icon-trash',
                       title=self._translate(_('delete rule element')),
                       cssclass='ui-button ui-modal-minsize',
                       ajax=self.box_delete())
    
    def box_buttons(self):
        li = list()
        li.append(self.box_buttons_delete())
        li.append(self.box_buttons_save())
        return li
    
    def box_delete(self):
        return '%s/wireit_delete' % grok.url(utils.getRequest(), self.context)

    def box_edit(self):
        return '%s/wireit_edit' % grok.url(utils.getRequest(), self.context)

    def identifier(self):
        return dict(name=getattr(self,'grokcore.component.directive.name'),
                    implements=[dict(module=i.__module__, interface=i.__name__) for i in self.__implemented__.interfaces()])
    
    def implements(self):
        [i for i in self.__implemented__.interfaces()]


    def override_properties(self):
        return [i for i in self.form_fields if i.field.getName() not in self.override_properties_ignors]


    def _translate(self, msg):
        return translate(msg, context=utils.getRequest())


class InputFactory(BaseFactory):
    grok.name('raptus.mailcone.rules.input')
    grok.implements(interfaces.IInputItemFactory)
    
    
    title = _('Input')
    description = _('All mails came through the Input Element')

    def box_buttons(self):
        li = list()
        li.append(self.box_buttons_delete())
        return li

    def box_output(self):
        li = list()
        li.append(dict(title=self._translate(_('mailoutput')) ))
        return li


class InputCustomerFactory(BaseFactory):
    grok.name('raptus.mailcone.rules.inputcustomer')
    grok.implements(interfaces.IInputItemFactory)
    
    
    title = _('Input Customer')
    description = _('All mails for each customer came in through the Input Element')

    def box_buttons(self):
        li = list()
        li.append(self.box_buttons_delete())
        return li

    def box_output(self):
        li = list()
        li.append(dict(title=self._translate(_('mailoutput')) ))
        return li
    
