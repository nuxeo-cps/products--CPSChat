##parameters=
# $Id$

"""Edit the chat item properties
"""

if context.REQUEST is not None:
    form = context.REQUEST.form

    kw = {}
    kw['message'] = form.get('message', '')

    # Updating attributes
    context.editProps(**kw)

    psm = '?portal_status_message=psm_chat_item_properties_updated'
    url = context.aq_parent.aq_inner.absolute_url() + \
          '/cps_chat_moderate_form'
    context.REQUEST.RESPONSE.redirect(url + psm)

