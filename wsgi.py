from pim_app.__init__ import create_app


if __name__=="__main__":
    app = create_app()
    app.run()
else:
    gunicorn_app=create_app()
