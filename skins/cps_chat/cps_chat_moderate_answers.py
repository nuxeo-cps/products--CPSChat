##parameters=REQUEST=None
#$Id$
"""Moderate some answers
"""

if REQUEST is not None:
    form = REQUEST.form
    context.moderateAnswers(form)
    REQUEST.RESPONSE.redirect(context.absolute_url())
