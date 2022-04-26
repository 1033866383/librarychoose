import os
import subprocess

import schedule

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    schedule.every().day.at("23:06").do(lambda: subprocess.run("librarychoosetask_jar/start.bat"))
    app.run(host="0.0.0.0", port=8071)

    # Base.metadata.create_all(engine)
