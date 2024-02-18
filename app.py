from flask import Flask, render_template, request, send_file
import os
import excecution_module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join('uploads', 'excel_file.xlsx')
        uploaded_file.save(file_path)
        # Process the file here (e.g., convert it to Excel)
        # After processing, generate the Excel file
        generated_excel_file = "path/to/generated/excel/file.xlsx"
        return 'File uploaded successfully'
    return "No file uploaded"

@app.route('/form', methods=['POST'])
def process_form():
    data = request.get_json()
    if data['qaInput']:
        # Process Quality analysis for file
        print(data['qaInput'])
        print(data['fullfile'])
        print(data['percentage'])
        print(data['prompt'])
        
    elif data['fullfile']:
        # Process full file
        process_complete_file()
    return 'Form submitted successfully'


def process_complete_file():

    excecution_module.start_excussion()
    return 0


if __name__ == '__main__':
    app.run(debug=True , port=3000)
