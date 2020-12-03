# This file is used for hosting at PythonAnywhere.com
# 'app' must point to a Flask Application object.

from app import create_app

app=create_app()
app.run(debug=True, host="127.0.0.1") # run the Flask web application

