__author__ = 'tarzan'


def jsonize_uncaught_exception_tween_factory(handler, registry):
    """
    This tween prevent all uncaught exception and return JSON response with error code 500
    """
    def jsonize_uncaught_exception_tween(request):
        """
        :type request: pyramid.request.Request
        :rtype : pyramid.response.Response
        """
        try:
            return handler(request)
        except BaseException, e:
            import json
            from pyramid import response

            body = json.dumps({
                'error': e.__class__.__name__,
                'code': 500,
                'status': '500 Internal Server Error',
                'message': e.message,
            })
            return response.Response(
                body=body,
                status='500 Internal Server Error',
                content_type='application/json',
            )

    return jsonize_uncaught_exception_tween