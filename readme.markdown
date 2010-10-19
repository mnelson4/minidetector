Info
====

This application is a simple middleware and associated decorator that will add a ".mobile" attribute to your request objects, which, if True, means the requester is coming to you from a mobile phone (cellphone), PDA, or other device that should be considered small screened, or have an underpowered browser, such as games consoles.

This mostly works using a list of search strings, though there are a couple of other tricks, like detecting the presence of Opera Mini. The strings are in an easily-parseable text file, and thus can be used for other similar projects.

It also includes a pretty extensive list of user agents to test against.

If sessions are enabled subsequent requests obtain mobile attributes from the session without parsing the requestor's meta data.

Optionally "mobile" requestors can be redirected to a mobile domain. If they come back to the non-mobile domain the presence of session data keeps them from be automatically redirected back to the mobile domain.

Installation
============

Using minidetector is very simple. Simply place the minidetector package into your project's path, and then add:

	minidetector.Middleware

to your `MIDDLEWARE_CLASSES` tuple in your settings.py

Then in your view you can check `request.mobile` - if it's `True` then treat it like a small screen device. If it's `False` then it's probably a desktop browser, or a spider or something else.

If you only have certain views that need the distinction, you can choose not to search every request you receive. All you need to do is wrap the relevant views like this:

	from minidetector import detect_mobile

	@detect_mobile
	def my_mobile_view(request):
		if request.mobile:
			#do something with mobile

"Special" Devices
=================

minidetector also adds some extra info for popular devices to the request object. The defaults for a desktop browser:

	- request.wap = False
	- request.browser_is_android = False
	- request.browser_is_ios = False
	- request.browser_is_ipad = False
	- request.browser_is_iphone = False
	- request.browser_is_webkit = False
	- request.mobile_device = ''
	- request.touch_device = False
	- request.wide_device = True


Extra Info
----------

for webkit:

	request.browser_is_webkit = True

for the iPad:

	request.browser_is_ipad = True
	request.mobile_device = 'ipad'

for the iPhone or iPod touch:

	request.browser_is_iphone = True
	request.mobile_device = 'iphone'

for iOS in general:

	request.browser_is_ios = True

and for Android:

	request.browser_is_android = True
	request.mobile_device = 'android'

I also send 'request.touch_device' as True for all webkit touch devices (iOS and android.)

I also now send 'request.wide_device' as True for all 'wide' devices. Currently this covers all desktops and the ipad. I'll revisit this when other tablets (webOS or android) come out (if I can detect it.)

Override mobile treatment
-------------------------

By default the iPad is not treated as a mobile browser. If you want to reverse this, add the following to your settings.py:

	IPAD_IS_MOBILE = True

You can do the reverse for iphone and android (i.e. having them treat your site as non-mobile.)

	IPHONE_IS_MOBILE = False
	ANDROID_IS_MOBILE = False

Redirect to mobile domain
------------------------

By default only the request is modified as described above. If `MOBILE_URL` is set to a non empty string and the request.mobile is True the requestor will be redirected to the `MOBILE_URL`.

If sessions are enabled and a requestor returns to the non mobile site they will not be redirected again to the `MOBILE_URL` site.

The intent is to allow automatically sending mobile devices to a mobile website while still allowing the user to choose to use the non-mobile website.
