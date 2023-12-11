"""Flask app for Cupcakes"""

import os
from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


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
    # TODO: add order (maybe alphabetical by flavor or by rating)
    cupcakes = Cupcake.query.all()
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

    if request.json.get("image_url") == '':
        request.json['image_url'] = None

    new_cupcake = Cupcake(
        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image_url = request.json.get("image_url")
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def edit_cupcake(cupcake_id):
    """Edit data for a single cupcake and return cupcake info

     Input JSON:
        {
            "flavor": "hazelnut", [optional]
            "image_url": "https://tinyurl.com/demo-cupcake", [optional]
            "rating": 5, [optional]
            "size": "large" [optional]
        }

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

    # TODO: check if there is a way to loop through input fields
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.image_url = request.json.get('image_url', cupcake.image_url)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


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
