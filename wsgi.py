from app.main import app
import start

if __name__ == "__main__":
    #start.db_create()
    app.run(threaded=True, port=5000)