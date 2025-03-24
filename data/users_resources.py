from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('modified_data', required=True)
parser.add_argument('jobs', required=True)


def abort_if_users_not_found(news_id):
    session = db_session.create_session()
    users = session.query(User).get(news_id)
    if not users:
        abort(404, message=f"News {news_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'users': users.to_dict(
            rules=('-jobs.user', '-hashed_password'))})

    def delete(self, news_id):
        abort_if_users_not_found(news_id)
        session = db_session.create_session()
        news = session.query(User).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            orules=('-jobs.user', '-hashed_password')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            is_published=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        user.set_password(args['password'])
        if args.get('modified_date'):
            user['modified_date'] = args['modified_date']
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})