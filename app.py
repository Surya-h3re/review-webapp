from os.path import dirname, join
from flask import Flask, jsonify, render_template, redirect
from flask import request, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import csv
import os

app = Flask(__name__)

current_dir = dirname(__file__)
file_path = join(current_dir, "./data/reviews.csv")


class ReviewForm(Form):
    name = TextField('Full Name*', validators=[validators.DataRequired()])
    product = TextField(
        'Product Name*', validators=[validators.DataRequired()])
    review = TextAreaField('Review*', validators=[validators.DataRequired()])


@app.route('/', methods=['POST', 'GET'])
def index():
    form = ReviewForm(request.form)
    x = 0  # to specify if valid data is given
    if (request.method == 'POST') or (request.method == 'GET'):
        with open(file_path) as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            first_line = True
            reviews = []
            for row in data:
                if not first_line:
                    if row:
                        reviews.append({
                            "name": row[0],
                            "product": row[1],
                            "review": row[2]
                        })
                else:
                    first_line = False
    if request.method == 'POST' and form.validate():
        form = dict(request.form)
        name = form["name"].strip()
        product = form["product"].strip()
        review = form["review"].strip()
        # strip() function is used to remove leading and trailing whitespaces
        if len(name) > 1 and len(product) > 2 and (len(review) > 5):
            with open(file_path, mode='a') as csv_file:
                # with open(r'data/reviews.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([name, product, review])
                return redirect('http://localhost:5000/')
        else:
            x = 1  # valid data not given
    form = ReviewForm()
    if (x == 1):
        return render_template("index.html", reviews=reviews, form=form, datavalid="*Please Enter Valid Data (Review - min. 10 characters)")
    else:
        return render_template("index.html", reviews=reviews, form=form)


if __name__ == '__main__':
    app.run(debug=True)

# http://localhost:5000/
