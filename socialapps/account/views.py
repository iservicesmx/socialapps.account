#-*- coding: utf8 -*-
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from django.views.generic.edit import FormView
from socialapps.account.forms import LoginForm
#from socialapps.core.views import UpdateView
from socialapps.account.models import PersonalSettings

class Login(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        requested_redirect = self.request.REQUEST.get(REDIRECT_FIELD_NAME, False)
        if requested_redirect:
            return requested_redirect
        return settings.LOGIN_REDIRECT_URL
        
    def form_valid(self, form):
        identification, password, remember_me = (form.cleaned_data['identification'],
                                                 form.cleaned_data['password'],
                                                 form.cleaned_data['remember_me'])
        user = authenticate(identification=identification,
                            password=password)
        if user.is_active:
            login(self.request, user)
            if remember_me:
                self.request.session.set_expiry(settings.LOGIN_REMEMBER_ME_DAYS * 3600)
            else: self.request.session.set_expiry(0)

            messages.success(self.request, _('You have been signed in.'),
                                 fail_silently=True)
        else:
            messages.error(self.request, _("Your user is not active, please validate via the link we emailed you"),
                                     fail_silently=True)
            #TODO: we need to make the disable view
            #return redirect(reverse('socialapps_disabled',
            #                         kwargs={'username': user.username}))
        
        return super(Login, self).form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, _("Please enter a correct username or email and password."),
                             fail_silently=True)
        return super(Login, self).form_invalid(form)

#class SettingsView(UpdateView):
#    model = PersonalSettings
    # Cambio de Password
    # Cambio de correo
    # Cambio de idioma
    # combio de timezone
#    pass
    
#class SelectThemeView(UpdateView):
#    model = PersonalSettings
#    pass
    
def get_user_info(request, user, profile, client):
    
    return client.get_user_info()