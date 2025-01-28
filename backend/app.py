from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import os

# Configuração do Flask
app = Flask(__name__)

# Configuração da pasta de uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota para receber uploads de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo inválido"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Extrai o texto do PDF
    text = extract_text_from_pdf(file_path)
    
    return jsonify({
        "message": "Arquivo enviado com sucesso!",
        "file_path": file_path,
        "text": text  # Retorna o texto extraído
    }), 200

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Rota inicial (opcional)
@app.route('/')
def home():
    return "Bem-vindo ao micro SaaS de filtro de questões!"

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)