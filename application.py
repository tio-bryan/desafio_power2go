#!/usr/bin/env python3

from flask import Flask
from flask_graphql import GraphQLView

from database import db_session
from schema import schema


application = Flask(__name__)
application.debug = True

application.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@application.teardown_appcontext
def shutdown_session(_exception=None):
    db_session.remove()


if __name__ == '__main__':
    application.run()
