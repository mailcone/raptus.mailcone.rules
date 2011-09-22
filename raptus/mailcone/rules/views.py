import grok

from megrok import navigation

from zope.component import getUtility

from raptus.mailcone.layout.views import Page
from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import AddForm, EditForm, DeleteForm, DisplayForm

from raptus.mailcone.rules import _
from raptus.mailcone.rules import interfaces
from raptus.mailcone.rules import contents

grok.templatedir('templates')

""" Note: all WireIt stuff and view are located in raptus.mailcone.rules.wireit
"""


class RulesetsTable(BaseDataTable):
    grok.context(interfaces.IRulesetContainer)
    interface_fields = interfaces.IRuleset
    ignors_fields = ['id']
    actions = (dict( title = _('delete'),
                     cssclass = 'ui-icon ui-icon-trash ui-modal-minsize ui-datatable-ajaxlink',
                     link = 'deleterulesetform'),
               dict( title = _('open'),
                     cssclass = 'ui-icon ui-icon-arrow-4-diag',
                     link = 'ruleboard'),
               dict( title = _('edit'),
                     cssclass = 'ui-icon ui-icon-pencil ui-datatable-ajaxlink',
                     link = 'editrulesetform'),)

class Rulesets(Page):
    grok.name('index')
    grok.context(interfaces.IRulesetContainer)
    locatormenuitem(IOverviewMenu, interfaces.IRulesetContainerLocator, _(u'Rulesets'))
    
    @property
    def rulesetstable(self):
        return RulesetsTable(self.context, self.request).html()
    
    @property
    def addurl(self):
        return '%s/addrulesetform' % grok.url(self.request, self.context)
    

class AddRulesetForm(AddForm):
    grok.context(interfaces.IRulesetContainer)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.IRuleset).omit('id')
    label = _('Add a new ruleset')

    def create(self, **data):
        return contents.Ruleset()


class EditRulesetForm(EditForm):
    grok.context(interfaces.IRuleset)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.IRuleset).omit('id')
    label = _('Edit ruleset')


class DeleteRulesetForm(DeleteForm):
    grok.context(interfaces.IRuleset)
    grok.require('zope.Public')
    
    def item_title(self):
        return self.context.name
    
    
class DisplayFormRuleset(DisplayForm):
    grok.name('index')
    grok.context(interfaces.IRuleset)
    grok.require('zope.Public')






