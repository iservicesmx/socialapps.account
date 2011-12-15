from django.conf.urls.defaults import *
from django.contrib.auth.views import logout

from socialapps.account.views import Login
from socialapps.account.forms import RegistrationFormOnlyEmail
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$',logout, {"next_page":"/"}, name='logout'),
    url(r'^register/$', 'registration.views.register',
                   {'form_class':RegistrationFormOnlyEmail,
                   'backend':'registration.backends.default.DefaultBackend'},
                   name="register"),
    (r'', include('registration.backends.default.urls')), 
    url(r'^$', TemplateView.as_view(template_name='registration/account.html'), name='account'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),    
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    
)
