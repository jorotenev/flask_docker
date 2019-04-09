from flask import render_template
from . import main
from logging import info


@main.route('/', methods=['GET', 'POST'])
def index():
    info('opsa')
    return render_template('index.html')
