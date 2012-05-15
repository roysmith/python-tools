from datetime import datetime
import dateutil.parser

class HttpError(Exception): pass
class NotFound(HttpError): pass
class BadRequest(HttpError): pass
class Forbidden(HttpError): pass

def _param(request, param_name, default=None):
    """Return the value of a parameter (either GET or POST) from the
    request.

    If the parameter doesn't exist and there's no default, raise
    BadRequest.

    """
    try:
        return request.REQUEST[param_name]
    except KeyError:
        if default is not None:
            return default
        else:
            raise BadRequest("missing required parameter (%s)" % param_name)

def _int_param(request, param_name, default=None):
    """Return the integer value of a parameter (either GET or POST)
    from the request.

    If the parameter doesn't exist and there's no default, raise
    BadRequest.  If you pass a default, it must be an integer.

    """
    assert default is None or isinstance(default, int)
    try:
        string_value = request.REQUEST[param_name]
    except KeyError:
        if default is not None:
            return default
        else:
            raise BadRequest("missing required parameter (%s)" % param_name)
    try:
        return int(string_value)
    except ValueError:
        raise BadRequest("parameter '%s' isn't a valid integer (%r)" % (param_name, string_value))

def _int_param_list(request, param_name):
    """Return a list of integer values for a multi-valued parameter
    (either GET or POST) from the request.

    If no such parameters exist, return an empty list.  If any of the
    values are not valid integers, raise BadRequest.

    """
    ints = []
    for s in request.REQUEST.getlist(param_name):
        try:
            ints.append(int(s))
        except ValueError:
            raise BadRequest("parameter '%s' isn't a valid integer (%r)" % (param_name, s))
    return ints

def _datetime_param(request, param_name, default = None):
    """Return the datetime of a parameter (either GET or POST)
    from the request.

    If the parameter string is an integer or float, it is taken as a
    unix timestamp (seconds since midnight, Jan 1, 1970 UTC).
    Otherwise, we try to parse it as something dateutil.parser
    understands.

    If the parameter doesn't exist and there's no default, raise
    BadRequest.  If you pass a default, it must be a datetime or
    a callable yielding a datetime

    """
    assert default is None or not (isinstance(default, int) or callable(default))
    try:
        string_value = request.REQUEST[param_name]
    except KeyError:
        if default is not None:
            return default() if callable(default) else default
        else:
            raise BadRequest("missing required parameter (%s)" % param_name)
    try:
        return datetime.utcfromtimestamp(float(string_value))
    except ValueError:
        pass

    try:
        return dateutil.parser.parse(string_value)
    except ValueError:
        raise BadRequest("parameter '%s' isn't a valid datetime (%r)" % (param_name, string_value))

def _bool_param(request, param_name, default=None):
    """Return the boolean value of a parameter (either GET or POST)
    from the request.

    If the parameter doesn't exist and there's no default, raise
    BadRequest.  If you pass a default, it must be an integer.

    """
    assert default is None or isinstance(default, bool)
    try:
        string_value = request.REQUEST[param_name]
    except KeyError:
        if default is not None:
            return default
        else:
            raise BadRequest("missing required parameter (%s)" % param_name)
    return _is_true(string_value)
