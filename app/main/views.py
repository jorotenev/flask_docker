from flask import render_template, abort
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



"""
Let's encrypt SSL
https://github.com/dmathieu/sabayon
"""
@main.route("/.well-known/acme-challenge/<token>")
def acme(token):
    key = find_key(token)
    if key is None:
        print("unsuccessful acme attempt %s"%token)
        abort(404)
    return key

def find_key(token):
    import os
    if token == os.environ.get("ACME_TOKEN"):
        return os.environ.get("ACME_KEY")
    for k, v in os.environ.items():
        if v == token and k.startswith("ACME_TOKEN_"):
            n = k.replace("ACME_TOKEN_", "")
            return os.environ.get("ACME_KEY_{}".format(n))
