import os
import sys
import time
import subprocess
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    with open('templates/content.html', 'r') as f:
        content = f.read()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Flask App</title>
        <script>
            setTimeout(function() {{
                location.reload();
            }}, 3000);
        </script>
    </head>
    <body>
        {content}
    </body>
    </html>
    '''

def check_git_status():
    try:
        print("Checking git status...")
        fetch_result = subprocess.run(['git', 'fetch'], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        print(f"Git fetch result: {fetch_result.returncode}, stderr: {fetch_result.stderr}")
        
        status_result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        print(f"Git status output: {status_result.stdout}")
        
        if 'Your branch is behind' in status_result.stdout:
            print("Repository is behind origin, pulling changes...")
            pull_result = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=os.path.dirname(__file__))
            print(f"Git pull result: {pull_result.stdout}")
            
            if pull_result.returncode == 0:
                print("Changes pulled successfully. Restarting app...")
                os._exit(0)
            else:
                print(f"Git pull failed: {pull_result.stderr}")
        else:
            print("Repository is up to date")
                
    except Exception as e:
        print(f"Git check failed: {e}")

def git_monitor():
    while True:
        check_git_status()
        time.sleep(5)

if __name__ == '__main__':
    git_thread = threading.Thread(target=git_monitor, daemon=True)
    git_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except OSError as e:
        if "Address already in use" in str(e) or "port 5000 already in use" in str(e).lower():
            print("Port 5000 is already in use. Trying port 5001...")
            try:
                app.run(host='0.0.0.0', port=5001, debug=False)
            except OSError:
                print("Port 5001 also in use. Trying port 5002...")
                app.run(host='0.0.0.0', port=5002, debug=False)
        else:
            raise
