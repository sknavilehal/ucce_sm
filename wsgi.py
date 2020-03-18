from pyapp import app

#gunicorn_logger = logging.getLogger('gunicorn.error')
#app.logger.handlers = gunicorn_logger.handlers
#app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
