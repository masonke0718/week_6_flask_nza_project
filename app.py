# Import for the app and route for the application

# This file is the main / master file that will be used by Flask
#'app' in '__init__' and routes is in 'routes.py'
from flask_nza import app, routes 

 # '__name__' is this file 'app.py' is the main file (it's not being imported anywhere else), run this
 # 'run' works with flask to get everything started
if __name__ == '__main__':
    app.run(debug = True)