$Id$

CPSChat is a Chat product for CPS3

What is it doing ? 
------------------

 - CPSChat provides a new content type (Chat) that you can create within
   Workspaces or Sections. 

 - It can be moderated "a posteriori" (real time) or "a priori". Chat
   moderators are taking care of that.

 - You can invite a guest that may reply to chat user posts.

 - ChatPosters are allowed to post messages.
 
 - ChatGuests can, as ChatPosters, post messages and as well decide to reply to
   some posts.
 
 - ChatModerators can moderate the chat and manage local roles. 

 Within Workspaces :
  
    - WorkspaceMember can post messages:
    - WorkspaceManager can moderate the chat.
    - WorkspaceReader can view the chat only.

  You may add in the chat context specific chat local roles. 
 
 - ChatModerators may close the chat.

 Within Sections : 

    - SectionReviewer / SectionManager can moderate the chat.
    - SectionReader can view the chat.

Technical overview
------------------

Chat content type : 

 - BTreeFolder2 content type to store huge amount of posts.

 - You may adjust the refresh rate according to the purpose of the chat.

Workflows : 

 - Dedicated chat / chatItem workflows (Sections / Workspaces) 

   They are different to take into consideration where you created the chat and
   the specific local roles of the context.

 - Dedicated Permissions (chatPost, chatReply, chatModerate)

Roles / permissions : 

 - Dedicated Roles (ChatPoster, ChatGuest, ChatModerator)
   Notice you may use the standard CPS local roles in sections / workspaces
   though)

