from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
import os
from openai import OpenAI
from dotenv import load_dotenv
from transformers import AutoTokenizer

# Carrega as variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise EnvironmentError("Variáveis de ambiente API_KEY e BASE_URL não configuradas!")

# Caminho absoluto para o diretório frontend
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Carrrega o tokenizer
tokenizer = AutoTokenizer.from_pretrained("./", trust_remote_code=True)

def contar_tokens(texto):
    return len(tokenizer.encode(texto))
# Configuração do Flask
app = Flask(__name__,
            template_folder=os.path.join(FRONTEND_DIR, 'templates'),
            static_folder=os.path.join(FRONTEND_DIR, 'static'))

# Configuração do OpenAI
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Configuração da pasta de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
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

     # Conta os tokens
    num_tokens = contar_tokens(text)
    
    return jsonify({
        "message": "Arquivo enviado com sucesso!",
        "file_path": file_path,
        "text": text,
        "num_tokens": num_tokens  # Retorna o texto extraído
    }), 200

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/filter_questions', methods=['POST'])
def filter_questions():
  try:
    data = request.json
    text = data.get('text')
    subject = data.get('subject')
    
    if not text or not subject:
        return jsonify({"error": "Texto e assunto são obrigatórios"}), 400
    
    # Limita o texto para 3000 tokens (ajuste conforme necessidade)
    max_tokens = 3000
    truncated_text = text[:max_tokens*4]  # 1 token ≈ 4 caracteres
    
    prompt = f"""Filtre APENAS as questões sobre {subject} no formato exato:
        [QUESTÃO X] <texto completo da questão>
        Formate como lista numerada. Texto para análise:
        {truncated_text}"""

    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um especialista em análise de provas. Sua saída deve conter APENAS as questões no formato solicitado."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=2000,
            stream=False
        )
    # Verificação adicional da resposta
    if not response.choices[0].message.content:
            raise ValueError("Resposta da API vazia")
            
    return jsonify({
            "filtered_questions": response.choices[0].message.content
        }), 200

  except Exception as e:
        app.logger.error(f"Erro na API: {str(e)}")
        return jsonify({
            "error": f"Falha na comunicação com a API: {str(e)}"
        }), 500
    

# Rota inicial (opcional)
@app.route('/')
def home():
    return render_template('index.html')

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)