from flask import Flask, request
import notifier
import threading

app = Flask(__name__)

@app.route('/recorder', methods=['GET'])
def recorder():
    text_value = request.args.get('text', 'no message')
    notifier.send_recording(text_value)
    return f"text :{text_value}"




def run():
    app.run(host='0.0.0.0', port=8080, threaded=True)

thread = threading.Thread(target=run)
thread.start()