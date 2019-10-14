import redis
import time
from flask import Flask, render_template


app = Flask(__name__)
cli = redis.Redis(host='www.hzasteam.org', password='sadkfjhuwehufdsnvjkjlehghuleharferaghkjvsldu394872937ryfygeu2783tf')

@app.route('/<team_a>/<team_b>')
def pre(team_a, team_b):
    result = cli.hget('nba_pre', f'{team_a}-{team_b}') 
    if not result:
        if len(team_a) == 3 and len(team_b) == 3:
            cli.hset('nba_pre', f'{team_a}-{team_b}', 'pre')
        else:
            return 'Error'
    start_time = time.time()
    while True:
        result = cli.hget('nba_pre', f'{team_a}-{team_b}') 
        if result and result != b'pre':
            return str(result)
        if time.time() - start_time > 3:
            return 'Error'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
 