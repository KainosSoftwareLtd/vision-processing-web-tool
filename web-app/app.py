import os
import logging
from flask import Flask, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
import items
import machine_learning
import settings
import helpers

app = Flask(__name__)
app.config.from_object('config')


@app.route('/all')
def all():
    page = int(helpers.get_arg(request.args.get('page'), 1))
    count = int(helpers.get_arg(request.args.get('count'), settings.items_per_page))
    itms = items.get_items()
    num_pages = items.get_num_pages(itms, count)
    labels_json = items.get_page(itms, page, count)

    return render_template('custom/index.html', labels_json=labels_json,
                           num_pages=num_pages, page_num=page)


@app.route('/')
def home():
    tag = helpers.get_arg(request.args.get('tag'), 'untagged')
    page = int(helpers.get_arg(request.args.get('page'), 1))
    count = int(helpers.get_arg(request.args.get(
        'count'), settings.items_per_page))
    itms = items.get_items()
    num_pages = items.get_num_pages(itms, count, tag='untagged')
    labels_json = items.get_page(items.get_tag(itms, tag), page, count)
    return render_template('custom/index.html', labels_json=labels_json,
                           num_pages=num_pages, page_num=page)


@app.route('/summary')
def summary():
    return render_template('custom/summary.html', data=items.summarise_items(items.get_items()))


@app.route('/suggestions')
def suggestions():
    # For demo load fake suggestions
    return render_template('custom/suggestions.html',
                           labels_json=items.get_suggestions('static/images/suggestions/'))


@app.route('/classify', methods=['POST'])
def classify():
    predictions = machine_learning.predict(
        dict(ImmutableMultiDict(request.form))['items[]'])
    return render_template('custom/suggestions.html',
                           labels_json=predictions)


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file[]')
    dir_name = os.path.dirname(os.path.join(
        settings.upload_folder, 'untagged/'))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for f in files:
        f.save(os.path.join(os.path.join(
            settings.upload_folder, 'untagged/'), f.filename))
    return redirect('/')


@app.route('/tag', methods=['POST'])
def tag():
    print dict(request.form)
    items.process_tags(dict(ImmutableMultiDict(request.form)))
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    items.delete_items(dict(ImmutableMultiDict(request.form)))
    return redirect('/')


@app.route('/train', methods=['GET'])
def train():
    items.split_train_validation()
    machine_learning.train_model(augment_data_trigger=False)
    return redirect('/')


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = logging.FileHandler('error.log')
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', settings.port))
    app.run(host='0.0.0.0', port=port)
