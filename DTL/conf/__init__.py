import os
from django.conf import LazySettings, Settings
from django.core.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "DTL_SETTINGS_MODULE"

class DTLSettings(LazySettings):
    
    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        try:
            settings_module = os.environ[ENVIRONMENT_VARIABLE]
            if not settings_module: # If it's set but is an empty string.
                settings_module = 'DTL.conf.global_settings'
        except:
            settings_module = 'DTL.conf.global_settings'

        self._wrapped = Settings(settings_module)
        self._configure_logging()

settings = DTLSettings()