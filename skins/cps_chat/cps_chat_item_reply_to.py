##parameters=REQUEST=None
#$Id$
"""Reply th the post
"""

if REQUEST is not None:
    form = REQUEST.form
    message = form.get('message', '')
    context.addReply(message=message)

    psm = '?portal_status_message=psm_chat_item_reply'
    url = context.aq_parent.aq_inner.absolute_url() + \
          '/cps_chat_answer_form'
    REQUEST.RESPONSE.redirect(url + psm)

