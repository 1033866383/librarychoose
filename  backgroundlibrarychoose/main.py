import os

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8071)

    # Base.metadata.create_all(engine)
