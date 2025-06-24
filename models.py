from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationships
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    # Serialization rules to prevent recursion
    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.id}: {self.number} on {self.date}>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationships
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Serialization rules to prevent recursion
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'))

    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # Serialization rules to prevent recursion
    serialize_rules = ('-episode.appearances', '-guest.appearances',)

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5, inclusive.")
        return rating

    def __repr__(self):
        return f'<Appearance {self.id}: Rating {self.rating} for Episode {self.episode_id} with Guest {self.guest_id}>'