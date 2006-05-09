##parameters=REQUEST=None

if REQUEST is not None:
    if getattr(REQUEST, 'form', None):
        form = REQUEST.form
        message = form.get('message', '')
        pseudo = form.get('pseudo', '')
        if message:
            if not pseudo and context.portal_membership.isAnonymousUser():
                pseudo = 'Anonymous'
            context.addChatItem(message=message, pseudo=pseudo)
return context.cps_chat_main_frame()
