# MicroSaaS - Filtro de Questões de Concursos

## Descrição do Projeto

Este MicroSaaS é um serviço especializado em filtrar questões de provas de concursos públicos com base em assuntos específicos. Ideal para candidatos que desejam otimizar seus estudos, focando em temas relevantes para sua preparação.

## Funcionalidades

- Upload de arquivos PDF de provas anteriores
- Filtragem de questões por assunto específico
- Cálculo automático de tokens utilizados por requisição
- Integração com a API DeepSeek para processamento inteligente de texto

## Tecnologias Utilizadas

- Python
- Flask
- PyPDF2
- OpenAI (para integração com DeepSeek)
- HTML/CSS/JavaScript (Frontend)

## Como Usar

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r backend/requirements.txt
   ```
3. Configure as variáveis de ambiente no arquivo `.env`
4. Execute o servidor Flask:
   ```
   python backend/app.py
   ```
5. Acesse a interface web através do navegador

## Estrutura do Projeto

```
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── uploads/
├── frontend/
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       └── js/
├── .env
├── README.md
└── .gitignore
```

## Contribuindo

Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

## Contato

Para mais informações, entre em contato através de [fredamaraljr@gmail.com].

