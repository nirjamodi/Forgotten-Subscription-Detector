from flask import Flask, render_template, request, send_file, url_for
import os
from detector import run_detector
from pdf_parser import pdf_to_dataframe

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure upload folder exists and is a directory
upload_path = app.config['UPLOAD_FOLDER']
if os.path.exists(upload_path) and not os.path.isdir(upload_path):
    os.remove(upload_path)
os.makedirs(upload_path, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    table = None
    download_link = False

    if request.method == 'POST':
        file = request.files['file']

        if file and (file.filename.endswith('.csv') or file.filename.endswith('.pdf')):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                if filepath.endswith('.csv'):
                    df = run_detector(filepath)
                elif filepath.endswith('.pdf'):
                    extracted_df = pdf_to_dataframe(filepath)
                    df = run_detector(extracted_df)

                # Save output for download
                output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'subscriptions_output.csv')
                df.to_csv(output_file, index=False)

                table = df.to_html(classes='table table-striped', index=False)
                download_link = True

            except Exception as e:
                error = f"⚠️ Error: {str(e)}"

        else:
            error = "Unsupported file format. Please upload a .csv or .pdf file."

    return render_template('index.html', table=table, error=error, download_link=download_link)

@app.route('/download')
def download_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'subscriptions_output.csv')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)