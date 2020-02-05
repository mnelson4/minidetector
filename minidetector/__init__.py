from django import middleware
from django.http import HttpResponseRedirect
from minidetector import settings as minidetector_settings
from minidetector.useragents import search_strings

class Middleware(object):
    #following tutorial on django 1.10 middlwares: https://docs.djangoproject.com/en/1.10/topics/http/middleware/3
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        
    def __call__(self, request):        
        """ Adds a "mobile" attribute to the request which is True or False
            depending on whether the request should be considered to come from a
            small-screen device such as a phone or a PDA"""
        if hasattr(request, 'session'):
            # session enabled
            if not request.session.get('mobile_checked', False):
                # haven't checked if mobile yet - put in request and session
                self.configure_request(request)
                self.set_session_from_request(request)
                request.session['mobile_checked'] = True
                if request.mobile and minidetector_settings.MOBILE_URL:
                    return HttpResponseRedirect(minidetector_settings.MOBILE_URL)
            else:
                # Make sure it doesn't try this again
                self.set_request_from_session(request)
        else:
            # sessions disabled - always do the work
            self.configure_request(request)

        return self.get_response(request)

    def set_session_from_request(self, request):
        request.session['mobile'] = request.mobile
        request.session['wap'] = request.wap
        request.session['browser_is_android'] = request.browser_is_android
        request.session['browser_is_ios'] = request.browser_is_ios
        request.session['browser_is_ipad'] = request.browser_is_ipad
        request.session['browser_is_iphone'] = request.browser_is_iphone
        request.session['browser_is_webkit'] = request.browser_is_webkit
        request.session['mobile_device'] = request.mobile_device
        request.session['touch_device'] = request.touch_device
        request.session['wide_device'] = request.wide_device

    def set_request_from_session(self, request):
        request.mobile = request.session['mobile']
        request.wap = request.session['wap']
        request.browser_is_android = request.session['browser_is_android']
        request.browser_is_ios = request.session['browser_is_ios']
        request.browser_is_ipad = request.session['browser_is_ipad']
        request.browser_is_iphone = request.session['browser_is_iphone']
        request.browser_is_webkit = request.session['browser_is_webkit']
        request.mobile_device = request.session['mobile_device']
        request.touch_device = request.session['touch_device']
        request.wide_device = request.session['wide_device']

    def configure_request(self, request):
        # default all possible attributes for desktop
        request.mobile = False
        request.wap = False
        request.browser_is_android = False
        request.browser_is_ios = False
        request.browser_is_ipad = False
        request.browser_is_iphone = False
        request.browser_is_webkit = False
        request.mobile_device = ''
        request.touch_device = False
        request.wide_device = True

        if "HTTP_X_OPERAMINI_FEATURES" in request.META:
            #Then it's running opera mini. 'Nuff said.
            #Reference from:
            # http://dev.opera.com/articles/view/opera-mini-request-headers/
            request.mobile = True
            return

        if "HTTP_ACCEPT" in request.META:
            s = request.META["HTTP_ACCEPT"].lower()
            if 'application/vnd.wap.xhtml+xml' in s:
                # Then it's a wap browser
                request.mobile = True
                request.wap = True
                return

        if "HTTP_USER_AGENT" in request.META:
            # This takes the most processing. Surprisingly enough, when I
            # Experimented on my own machine, this was the most efficient
            # algorithm. Certainly more so than regexes.
            # Also, Caching didn't help much, with real-world caches.
            s = request.META["HTTP_USER_AGENT"].lower()

            if 'applewebkit' in s:
                request.browser_is_webkit = True

            # some special checks for 'important' devices
            if 'ipad' in s:
                request.browser_is_ipad = True
                request.browser_is_ios = True

                request.mobile_device = 'ipad'
                request.touch_device = True
                request.wide_device = True

                # toggle setting for deciding if ipad is mobile or not
                request.mobile = minidetector_settings.IPAD_IS_MOBILE
                return

            if 'iphone' in s or 'ipod' in s:
                request.browser_is_iphone = True
                request.browser_is_ios = True

                request.mobile_device = 'iphone'
                request.touch_device = True
                request.wide_device = False

                # toggle setting for deciding if iphone is mobile or not
                request.mobile = minidetector_settings.IPHONE_IS_MOBILE
                return

            if 'android' in s:
                request.browser_is_android = True

                request.mobile_device = 'android'
                request.touch_device = True
                request.wide_device = False

                # toggle setting for deciding if iphone is mobile or not
                request.mobile = minidetector_settings.ANDROID_IS_MOBILE
                return

            for ua in search_strings:
                if ua in s:
                    request.mobile = True
                    return

def detect_mobile(view):
    """ View Decorator that adds a "mobile" attribute to the request which is
        True or False depending on whether the request should be considered
        to come from a small-screen device such as a phone or a PDA"""

    def detected(request, *args, **kwargs):
        Middleware(request)
        return view(request, *args, **kwargs)
    detected.__doc__ = "%s\n[Wrapped by detect_mobile which detects if the request is from a phone]" % view.__doc__
    return detected

__all__ = ['Middleware', 'detect_mobile']
