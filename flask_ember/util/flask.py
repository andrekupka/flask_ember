from flask import _app_ctx_stack as ctx_stack


def get_current_app(app=None, assert_text=None):
    if app:
        return app
    ctx = ctx_stack.top
    if ctx is not None:
        return ctx.app
    if assert_text:
        assert False, assert_text
    return None
