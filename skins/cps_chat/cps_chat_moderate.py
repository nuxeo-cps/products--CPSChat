##parameters=REQUEST=None
#$Id$
"""Moderate some messages
"""

if REQUEST is not None:
    form = REQUEST.form
    context.moderateMessages(form)
    REQUEST.RESPONSE.redirect(context.absolute_url())
