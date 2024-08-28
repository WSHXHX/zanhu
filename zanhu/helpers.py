from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseBadRequest("not a ajax required")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequireMixin(View):
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

