from app.main import app
from start

if __name__ == "__main__":
    start.db_create()
    app.run(threaded=True, port=5000)