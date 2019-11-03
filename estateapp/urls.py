from django.urls import path
from django.conf.urls import url

from django.contrib.auth import views as auth_views


from . import views
urlpatterns=[
    path('index/', views.index ,name='index'),

    path('register/', views.signup),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('login/', views.loginview, name='login'),
    path('pg/', views.payingview, name='pg'),
    path('pglist/', views.pglistview, name='pglist'),
    path('pgview/<int:id>/', views.pgview ,name='pgview'),
    path('update/<int:editid>/',views.editview, name='upd' ),
    path('sample/<int:val>/', views.sample_ajax_view, name='ajax'),
    path('update/<int:editid>/',views.editview, name='upd' ),
    path('delete/<int:id>/', views.deleteview, name='delete'),
    path('logout/', views.logoutview, name='logout'),
    path('searchtwo/', views.searchtwo),
    url(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        ),
        name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
        
    ),
        name='password_reset_done'),
    
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
      
    ),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html',
        
    ),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'
    ),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ),
        name='password_change_done')
]
    

