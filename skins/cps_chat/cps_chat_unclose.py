##parameters=
#$Id :$
"""unclose the chat
"""

#from Products.CMFCore.WorkflowCore import WorkflowException

wftool = context.portal_workflow

try:
    wftool.doActionFor(context,
                       'unclose',
                       comment="Closing the chat")
    psm = "psm_cps_chat_unclosed_done"
except:
    psm = "psm_cps_chat_unclosed_not_possible"

if context.REQUEST is not None:
    context.REQUEST.RESPONSE.redirect(context.absolute_url()+'?portal_status_message='+psm)
