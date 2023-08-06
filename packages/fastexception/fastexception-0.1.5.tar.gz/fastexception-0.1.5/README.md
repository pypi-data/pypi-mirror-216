fast exception
===================
This package is a plugin for easier handling of Exception and sending HTTP status code.

Installing
============

    pip install fastexception

Usage
=======
You can use FastAPI itself as follows:

    @app.get("/")
    def index(password: str):
        if password.validate():
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="message")

    status code : 400
    message : message
But the simpler and more readable way to use fastexception is as follows:


    @app.get("/")
    def index(password: str):
        if password.validate():
            FastException.HTTP_400_BAD_REQUEST.http("message")


    status code : 400
    message : message

You can write your desired message in http, if you don't write it, fastexception will show the appropriate message.

    @app.get("/")
    def index(password: str):
        if password.validate():
            FastException.HTTP_400_BAD_REQUEST.http()


    status code : 400
    message : Bad Request