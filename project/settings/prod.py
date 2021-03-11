from .base import *


# Whitenoise config
# =====================================

# Insert Whitenoise Middleware.
try:
    pos = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
except ValueError:
    pos = 0
MIDDLEWARE.insert(pos, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Enable GZip.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'