from flask import Flask, render_template, request
from utils.db import init_db, save_response
from utils.gemini_api import generate_text, generate_image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        output_type = request.form['output_type']
        
        if output_type == 'text':
            response = generate_text(prompt)
        else:
            response = generate_image(prompt)
        
        save_response(prompt, response, output_type)
        return render_template('index.html', result=response, output_type=output_type)
    
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)