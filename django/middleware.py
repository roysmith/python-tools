from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from utils import BadRequest, Forbidden, NotFound

class HttpErrorHandler(object):
    def process_exception(self, request, ex):
        if isinstance(ex, NotFound):
            return HttpResponseNotFound(str(ex))
        if isinstance(ex, BadRequest):
            return HttpResponseBadRequest(str(ex))
        if isinstance(ex, Forbidden):
            return HttpResponseForbidden(str(ex))
        return None
