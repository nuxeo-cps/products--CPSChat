## Python (script) "Chat_add_question.py"
##parameters=
# $Id$

"""
Moderator : add a reply .
"""

if context.REQUEST is not None:
    form = context.REQUEST.form
    id_question = form.get('id_question', None)
    if id_question is not None:
        the_question = context.getQuestion(int(id_question))
        answer_from_moderator = form.get('answer', '')
        the_question.setAnswer(answer_from_moderator)
	the_question.setStatus("ANSWERED")

context.REQUEST.RESPONSE.redirect('./Chat_moderateForm')
