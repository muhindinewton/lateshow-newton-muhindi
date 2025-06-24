#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# Root route
@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

# a. GET /episodes
class EpisodesResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        # Using serialize_rules defined in the model to avoid recursion and select specific fields
        episode_dicts = [episode.to_dict() for episode in episodes]
        return make_response(jsonify(episode_dicts), 200)

api.add_resource(EpisodesResource, '/episodes')

# b. GET /episodes/:id
# d. DELETE /episodes/:id (from Postman collection)
class EpisodeByIdResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        # Manually constructing the response to match the exact specified format
        # including nested guest details within appearances
        episode_dict = episode.to_dict(rules=('-appearances.episode',)) # Exclude episode to prevent direct recursion
        
        # Customize appearances to include guest details
        appearances_list = []
        for appearance in episode.appearances:
            guest_dict = appearance.guest.to_dict(rules=('-appearances',)) # Exclude guest appearances to prevent recursion
            appearances_list.append({
                "episode_id": appearance.episode_id,
                "guest": guest_dict,
                "guest_id": appearance.guest_id,
                "id": appearance.id,
                "rating": appearance.rating
            })
        
        episode_dict['appearances'] = appearances_list
        
        return make_response(jsonify(episode_dict), 200)

    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        
        db.session.delete(episode)
        db.session.commit()
        return make_response(jsonify({}), 204) # No Content
        
api.add_resource(EpisodeByIdResource, '/episodes/<int:id>')

# c. GET /guests
class GuestsResource(Resource):
    def get(self):
        guests = Guest.query.all()
        guest_dicts = [guest.to_dict() for guest in guests]
        return make_response(jsonify(guest_dicts), 200)

api.add_resource(GuestsResource, '/guests')

# e. POST /appearances
class AppearancesResource(Resource):
    def post(self):
        data = request.get_json()
        
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        # Check if episode and guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode:
            return make_response(jsonify({"errors": ["Episode not found"]}), 404)
        if not guest:
            return make_response(jsonify({"errors": ["Guest not found"]}), 404)

        try:
            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )
            db.session.add(new_appearance)
            db.session.commit()

            # Return the newly created appearance with nested episode and guest details
            # Using serialize_rules to control recursion
            response_dict = new_appearance.to_dict()
            return make_response(jsonify(response_dict), 201) # Created
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400) # Bad Request
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["An unexpected error occurred: " + str(e)]}), 500)

api.add_resource(AppearancesResource, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)