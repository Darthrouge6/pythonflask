#!/usr/bin/python
# -*- coding: UTF-8 -*-


from flask_script import Manager, Server
from backend import create_app,db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

app.debug = app.config["DEBUG"]

host = app.config["HOST"]
port = app.config["PORT"]

# Init manager object via app object
manager = Manager(app)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("runserver", Server(host=host,port=port,threaded=True))

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,db=db)

#创建数据库脚本
@manager.command
def create_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.create_all()
    db.session.commit()

@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()