##parameters=REQUEST=None
# $Id$

"""Remove messages
"""

if REQUEST is not None:
    form = REQUEST.form
    ids = form.get('ids', [])
    context.delChatItems(ids)

    psm = '?portal_status_message=psm_messages_removed'
    url = context.absolute_url() + \
          '/cps_chat_moderate_form'
    context.REQUEST.RESPONSE.redirect(url + psm)

