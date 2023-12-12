"""Flask app for Cupcakes"""

import os
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def index():

    return render_template("index.html")

@app.get('/api/cupcakes')
def list_cupcakes():
    '''Return data about all cupcakes

        Returns JSON: {
        "cupcakes": [
            {
                "flavor": "cherry",
                "id": 1,
                "image_url": "https://tinyurl.com/demo-cupcake",
                "rating": 5,
                "size": "large"
            },
            {
                "flavor": "chocolate",
                "id": 2,
                "image_url": "https://image_url_here",
                "rating": 9,
                "size": "small"
            }
        ]
    }
    '''

    cupcakes = Cupcake.query.order_by("flavor").all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Return data for a single cupcake

    Returns JSON:
        {
        "cupcake": {
            "flavor": "cherry",
            "id": 1,
            "image_url": "https://tinyurl.com/demo-cupcake",
            "rating": 5,
            "size": "large"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """Create cupcake from posted JSON data and return it.

    Input JSON:
        {
            "flavor": "hazelnut",
            "image_url": "https://tinyurl.com/demo-cupcake", [optional]
            "rating": 5,
            "size": "large"
        }

    Returns JSON:
        {
        "cupcake": {
            "flavor": "hazelnut",
            "id": 3,
            "image_url": "https://tinyurl.com/demo-cupcake",
            "rating": 5,
            "size": "large"
        }
    }
    """

    data = request.json

    if data.get('image_url') is not None \
        and len(data['image_url'].strip()) == 0:
        data['image_url'] = None

    new_cupcake = Cupcake(
        flavor = data["flavor"],
        size = data["size"],
        rating = data["rating"],
        image_url = data.get("image_url")
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def edit_cupcake(cupcake_id):
    """Edit data for a single cupcake and return cupcake info

     Input JSON:
     {flavor, image_url, rating, size} [all fields optional]

    Returns JSON:
    {cupcake: {flavor, id, image_url, rating, size}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    if 'image_url' in data:
        if data['image_url'] is None or len(data['image_url'].strip()) == 0:
            cupcake.image_url = DEFAULT_IMAGE_URL
    else:
        cupcake.image_url = data.get('image_url', cupcake.image_url)

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.size = data.get('size', cupcake.size)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete data for a single cupcake and returns deleted cupcake id.

    Returns JSON:
       {deleted: 1}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=cupcake.id)

