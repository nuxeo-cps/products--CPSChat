## Python (script) "Chat_edit.py"
##parameters=
# $Id$

"""
Moderator change the question.
"""

if context.REQUEST is not None:
    form = context.REQUEST.form
    id_question = form.get('id_question', None)
    if id_question is not None:
        the_question = context.getQuestion(int(id_question))
        new_answer_from_moderator = form.get('answer', '')
        the_question.setAnswer(new_answer_from_moderator)

context.REQUEST.RESPONSE.redirect('./Chat_moderateForm')
