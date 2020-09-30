from project import init_app
import os

app = init_app()

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='localhost',port=9527, debug=False)

