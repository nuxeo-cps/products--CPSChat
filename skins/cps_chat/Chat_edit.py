## Python (script) "Chat_edit.py"
##parameters=
# $Id$

"""
Edit the chat properties
"""

if context.REQUEST is not None:
    form = context.REQUEST.form

    description = form.get('description', '')
    host = form.get('host', '')
    title = form.get('title', '')

    # Updating attributes
    context.editProperties(title=title, description=description, host=host)

    context.REQUEST.RESPONSE.redirect('./metadata_edit_form')

