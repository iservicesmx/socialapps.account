# encoding: utf-8
"""
forms.py

Copyright (c) 2010 iServices de México All rights reserved.
"""
import random
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.hashcompat import sha_constructor
from django.conf import settings

attrs_dict = {'class': 'required'}

class RegistrationForm(forms.Form):
    """
    Form for creating a new user account.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice and the Terms of Service to
    be accepted.

    """
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must contain only letters, numbers, dots and underscores.')})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('This username is already taken.'))
            
        return self.cleaned_data['username']

    def clean_email(self):
        """ 
        Validate that the e-mail address is unique. 
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('This email is already in use. Please supply a different email.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Validates that the values entered into the two password fields match.
        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('The two password fields didn\'t match.'))
        return self.cleaned_data


class RegistrationFormOnlyEmail(RegistrationForm):
    """
    Form for creating a new user account but not needing a username.
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationFormOnlyEmail, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean(self):
        """ Generate a random username before falling back to parent signup form """
        while True:
            username = sha_constructor(str(random.random())).hexdigest()[:5]
            try:
                User.objects.get(username__iexact=username)
            except User.DoesNotExist: break

        self.cleaned_data['username'] = username
        return super(RegistrationFormOnlyEmail, self).clean()

class RegistrationFormTos(RegistrationFormOnlyEmail):
    """ Add a Terms of Service button to the ``RegistrationFormOnlyEmail``. """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _('You must agree to the terms to register.')})
                             
class RegistrationFormSocial(RegistrationFormOnlyEmail):
    """
    Form for creating a new user account but not needing a username.
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationFormSocial, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']
    
    def save(self, request, user, profile, client):
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')    
        user.save()
        profile.user = user
        profile.save()
        return user, profile

class RegistrationFormSocialTos(RegistrationFormSocial, RegistrationFormTos):
    pass

class LoginForm(forms.Form):
    """
    A custom 'LoginForm' where the identification can be a e-mail
    address or username.
    """
    identification = forms.CharField(label = _("Username"),
                                widget = forms.TextInput(attrs = attrs_dict),
                                max_length = 75,
                                error_messages = {'required': _('Either supply us with your email or username.')})
    password = forms.CharField(label = _("Password"),
                              widget = forms.PasswordInput(attrs = attrs_dict, render_value=False))
                              
    remember_me = forms.BooleanField(widget = forms.CheckboxInput(attrs = attrs_dict),
                                    required = False,
                                    label = _(u'Remember me for %(days)s days' % {'days': settings.LOGIN_REMEMBER_ME_DAYS}))
                                    #TODO: habilitar solo la leyenda de rememberme... quitar los días

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid signin error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            user = authenticate(identification=identification, password=password)
            if user is None:
                raise forms.ValidationError("")
        return self.cleaned_data
        