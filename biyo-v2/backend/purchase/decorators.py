from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect


def pin_auth_required(fn):
    def wrapper(request, *a, **kw):
        if ('employee_id' not in request.session) and (not request.user.is_authenticated()):
            return HttpResponseRedirect(reverse_lazy('quick:login'))
        return fn(request, *a, **kw)
    return wrapper