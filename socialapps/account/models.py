from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import get_language_from_request, ugettext_lazy as _

#from timezones.fields import TimeZoneField
if hasattr(settings,'THEMES'):
    THEMES = settings.THEMES
    DEFAULT_THEME = settings.DEFAULT_THEME
else:
    THEMES = (('theme1','Theme 1'),)
    DEFAULT_THEME = 'theme1'


class PersonalSettings(models.Model):
    
    user = models.ForeignKey(User, unique=True, verbose_name=_("user"))
    
#    timezone = TimeZoneField(_("timezone"))
    language = models.CharField(_("language"),
        max_length = 10, 
        choices = settings.LANGUAGES,
        default = settings.LANGUAGE_CODE,
    )
    theme = models.CharField(_("theme"),
        max_length = 15, 
        choices = THEMES,
        default = DEFAULT_THEME,
    )

    def __unicode__(self):
        return self.user.username

