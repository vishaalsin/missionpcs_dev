import time

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
            return

        init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())

        expire_seconds = getattr(
            settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )

        session_is_expired = time.time() - init_time > expire_seconds

        if session_is_expired:
            request.session.flush()
            redirect_url = getattr(settings, "SESSION_TIMEOUT_REDIRECT", None)
            return redirect(r'^home')
            # if redirect_url:
            #     return redirect(redirect_url)
            # else:
            #     return redirect_to_login(next=request.path)

        expire_since_last_activity = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY", False
        )
        grace_period = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", 1
        )

        if expire_since_last_activity and time.time() - init_time > grace_period:
            request.session[SESSION_TIMEOUT_KEY] = time.time()
# from django.conf import settings
# from django.contrib import auth
# from yaksh.models import Last_visit
# from datetime import datetime, timedelta,date
# from django.utils.deprecation import MiddlewareMixin
# import dateutil.parser
# from json import dumps
# from pandas.io.parsers import ParserError
# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""
#
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     raise TypeError ("Type %s not serializable" % type(obj))
# class AutoLogout(MiddlewareMixin):
#   def process_request(self, request):
#     if not request.user.is_authenticated :
#       #Can't log out if not logged in
#       return
#     x = Last_visit.objects.filter(userr=request.user).get()
#     print("date ")
#     try:
#         if datetime.now() - dateutil.parser.parse(request.session['last_touch']) > timedelta(0, settings.AUTO_LOGOUT_DELAY * 10, 0):
#             logout(request)
#             print("check here ",datetime.strptime(dumps(datetime.now(), default=json_serial), '%Y-%m-%dT%H:%M:%S.%f%z')  - dateutil.parser.parse(request.session['last_touch'],tzinfo=dateutil.tz.tzutc()))
#             print("inside this")
#             del request.session['last_touch']
#             return self.get_response(request)
#         else:
#             request.session['last_touch'] = datetime.now()
#             return self.get_response(request)
#     except KeyError:#(, ValueError)
#         request.session['last_touch'] = dumps(datetime.now(), default=json_serial)
#         print(KeyError)# KeyError thrown if last touch doesn't exist, so set it.
#     print("here",x.last_visit,request.session['last_touch'])
#     x.last_visit = datetime.now()
#     x.save()
#         # request.session['last_touch'] = datetime.now()
