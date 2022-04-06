import os
import subprocess

import schedule as schedule

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')


def job_java():
    cmd = ["java", "-jar", "Task.jar"]
    res = subprocess.Popen(cmd)
    if res.returncode == 0:
        print("success")
    else:
        print("failed")

if __name__ == '__main__':
    try:
        schedule.every().day.at('23:18').do(job_java)
    except Exception as e:
        print(e)
    app.run(host="0.0.0.0", port=8071)

    # Base.metadata.create_all(engine)
