from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('comment/reply/', views.reply_page, name="reply"),
    path('postcomments', views.postcomments, name='postcomments'),
    path('postreply', views.postreply, name='postreply'),
    # path('successpage/<path:path>', views.successpage, name='successpage')
]
