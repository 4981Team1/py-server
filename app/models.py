# """Data models."""
# # currently not used..
# from . import db

# # class Users(db.Model):
# #     """Data model for user accounts."""

# #     __tablename__ = "Users"
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(64), index=False, unique=True, nullable=False)
# #     email = db.Column(db.String(80), index=True, unique=True, nullable=False)

# #     def __repr__(self):
# #         return "<User {}>".format(self.username)
# class Voter(db.Document):
#     name = db.StringField()
#     email = db.StringField()

#     def to_json(self):
#         return {"name": self.name,
#                 "email": self.email}
