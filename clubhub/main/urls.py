import django.conf.urls
from django.conf.urls import url
from . import views

urlpatterns = [

    # Auth views
    # --- Login/Logout views
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # --- Account creation views
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^confirm_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_email, name='confirm_email'),

    # --- Account recovery views
    url(r'^recover_account/$', views.password_reset,
        {'template_name': 'registration/recover_account.html',
         'email_template_name': 'mail/recover_account.html',
         'post_reset_redirect': 'recover_account_sent'},
        name='recover_account'),
    url(r'^recover_account/sent/$', views.password_reset_done,
        {'template_name': 'registration/recover_sent.html'}, name='recover_account_sent'),
    url(r'^recover_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {'template_name': 'registration/reset_password.html', 'post_reset_redirect': 'recover_account_complete'},
        name='password_reset'),
    url(r'^recover_account/complete/$', views.password_reset_complete,
        {'template_name': 'registration/reset_complete.html'}, name='recover_account_complete'),

    # External views
    url(r'^about/$', views.about, name='about'),

    # Submit view
    url(r'^submit/$', views.submit, name='submit'),

    # Slideshow views
    url(r'^present/h/(?P<hub_group>[0-9A-Za-z_]+)$', views.present, name='present_group'),
    url(r'^present/$', views.present, {'hub_group': None}, name='present'),
    url(r'^factory/slides$', views.slide_factory, name='factory.slides'),

    # Misc views
    url(None, views.set_timezone, name='set_timezone'),

    # Main page views
    url(r'^h/(?P<hub_group>[0-9A-Za-z_]+)$', views.index, name='index_group'),
    url(r'^$', views.index, {'hub_group': None}, name='index'),
]

# Link in our 404 page.
django.conf.urls.handler404 = views.error404
