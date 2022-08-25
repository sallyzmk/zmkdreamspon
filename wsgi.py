from app.main import app
import start

if __name__ == "__main__":
    app.run(threaded=True, port=5000)