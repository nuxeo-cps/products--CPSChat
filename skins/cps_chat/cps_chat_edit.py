##parameters=REQUEST=None
# $Id$

"""Edit the chat properties
"""

if REQUEST is not None:
    form = REQUEST.form

    kw = {}
    kw['title'] = form.get('title', '')
    kw['description'] = form.get('description', '')
    kw['cps_chat_guest'] = form.get('cps_chat_guest', '')
    kw['is_moderated'] = form.get('is_moderated', 0) and 1
    kw['cps_chat_refresh_rate'] = form.get('cps_chat_refresh_rate')

    # Updating attributes
    context.editProps(**kw)

    url = context.absolute_url()+'/cps_chat_edit_form/'
    psm = '?portal_status_message=psm_cps_chat_properties_modified'
    context.REQUEST.RESPONSE.redirect(url+psm)

