from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>",

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return "You are using POST\n"
    elif request.method=='GET':
        return "You are using GET"
    else:
        return "You are using neither GET nor POST"

@app.route('/hey')
def hey():
    #return "Hey, there!",200 #defauli 'ok'
    return "Hey, there!",201 # 'CREATED'
    #return "Hey, there!",202 # 'ACCEPTED'
    #return "Hey, there!",404 # 'NOT FOUND'
    #return "Hey, there!",500 # 'INTERNAL SERVER ERROR'

@app.route('/custom')
def custom():
    response = make_response('hello, its custom')
    response.status_code = 202
    response.headers['Content-Type'] = 'application/octet-stream'
    return response

@app.route('/greet/<name>')
def greet(name):
    return f"<h2>Hello, {name}!</h2>"

@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    return f'{number1} + {number2} = {number1 + number2}'

@app.route('/handle_url_params')
def handle_url_params():
    if 'greeting' not in request.args or 'name' not in request.args:
        return 'Missing URL params'
    greeting = request.args.get('greeting')
    name = request.args.get('name')
    return f'<h1>{greeting}, {name}!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

