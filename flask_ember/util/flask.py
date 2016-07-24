from flask import _app_ctx_stack as ctx_stack


def get_current_app(app=None, assert_text=None):
    """ Returns that currently active app. If app is specified, it is directly
    returned. Otherwise the app is taken from the application context stack. If
    there is None and an assert text is specified an assertion is thrown.
    Otherwise None is returned.

    :param app: the fallback application that is always returned first
    :type app: flask.Flask
    :param assert_text: the text of the assertion if there is no current app
    :type assert_text: str
    :rtype: flask.Flask
    """
    if app:
        return app
    ctx = ctx_stack.top
    if ctx is not None:
        return ctx.app
    if assert_text:
        assert False, assert_text
    return None
