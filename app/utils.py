from flask import make_response
from flask import request, url_for, flash, abort
from sqlalchemy.exc import DataError


MONEY_QUANTIZE_PRECISION = '0.00'


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


def make_response_from_binary_pdf(pdf, filename):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'attachment; filename=%s.pdf' % filename
    return response



def quantize_value(val, quantize=MONEY_QUANTIZE_PRECISION):
    """
    :argument :val - numeric value - either a int/float/etc. or a string which can be evaluated to a number
    :return: return :val, but as a Decimal, with :quantize number of digits after the .
    """
    from decimal import Decimal as D
    # https://docs.python.org/3/library/decimal.html#decimal.Decimal.quantize
    return D(str(val)).quantize(D(quantize))



def detach_from_db_session(arr, db):
    """
    Given an array of mapped objects, detach them from the db session.
    """
    try:
        for el in arr:
            db.session.expunge(el)
    except:
        logException()



