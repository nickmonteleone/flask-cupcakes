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
                "image_url": "https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg",
                "rating": 9,
                "size": "small"
            }
        ]
    }
    '''

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

    new_cupcake = Cupcake(
        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image_url = request.json["image_url"]
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)