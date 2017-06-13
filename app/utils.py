from flask import make_response
from flask import request, url_for, flash, abort

def detach_from_db_session(arr, db):
    """
    Given an array of mapped objects, detach them from the db session.
    """
    try:
        for el in arr:
            db.session.expunge(el)
    except:
        logException()

"""Logging utils"""
def logMessage(msg,level='warning'):
    from flask import current_app

    if current_app.config.get('ROLLBAR_ACCESS_TOKEN', False):
        import rollbar
        from flask import request
        rollbar.report_message(request=request, message=msg, level=level)
    else:
        print(str(msg))


def logException():
    """
    Use this in 'except' blocks to report an exception to Rollbar.
    """
    import sys
    from flask import request, current_app

    ex = sys.exc_info()
    if current_app.config.get('ROLLBAR_ACCESS_TOKEN', False):
        import rollbar
        rollbar.report_exc_info(ex, request, level='critical')
    else:
        print(str(ex))


 



