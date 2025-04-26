from flask import Flask, request, make_response, render_template, redirect, url_for, send_from_directory, jsonify
import fitz
import pandas as pd
import os
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

@app.route('/')
def index():
    myvalue = "askmyevent"
    myresult = 10+20
    mylist = [12,33,65,76]
    return render_template('index.html', value=myvalue, result=myresult, list=mylist)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if name == "sutapa" and password == "1234":
            return "Welcome, sutapa"
        else:
            return "Invalid credentials" 


@app.route('/convert_csv')
def convert_csv():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    if file.content_type == 'text/csv':
        content = file.read().decode('utf-8')
        return f"<h3>CSV File Content:</h3><pre>{content}</pre>"

    else:
        return "Unsupported file type", 400

@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']

    if not file:
        return "No file uploaded", 400

    if file.content_type == 'text/plain':
        content = file.read().decode('utf-8')
        return f"<h3>Text File Content:</h3><pre>{content}</pre>"

    elif file.content_type == 'application/pdf':
        content = file.read()
        pdf_document = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()

        return f"<h3>PDF File Content:</h3><pre>{text}</pre>"

    else:
        return "Unsupported file type", 400
    
@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
    file = request.files['file']

    df = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads', filename), index=False)

    return render_template('download.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')

@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']

    with open('greeting.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'Greeting received'})

@app.route('/other')
def other():
    return render_template('otherpage.html')

@app.route('/filter')
def filter():
    some_text = 'Hello from filter\n'
    return render_template('filter.html', text = some_text)

@app.template_filter('reverse')
def reverse_string(s):
    return s[::-1] # for reverse

@app.template_filter('repeat')
def repeat(s, times=2):
    return s * times # for repeat

@app.template_filter('alternate_case')
def alternate_case(s):
    return ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])

@app.route('/hdjhcidsjhci')
def otherSome():
    return "otherSome!"

@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('other')) #by function name


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

