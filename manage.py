from  app import create_app,db
from flask_script import  Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Post,Comment


# app = create_app('development')
app= create_app('production')
# app= create_app('test')

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command('server', Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, User=User, Post=Post, Comment=Comment )


if __name__ == '__main__':
   manager.run()