from django.conf import settings

ANDROID_IS_MOBILE = getattr(settings, 'ANDROID_IS_MOBILE', True)
IPHONE_IS_MOBILE = getattr(settings, 'IPHONE_IS_MOBILE', True)
IPAD_IS_MOBILE = getattr(settings, 'IPAD_IS_MOBILE', False)
