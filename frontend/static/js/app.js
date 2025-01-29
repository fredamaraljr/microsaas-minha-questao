
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            formData.append('file', document.getElementById('pdfFile').files[0]);
            
            try {
                // Upload do arquivo
                const uploadResponse = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const uploadData = await uploadResponse.json();
                
                // Filtragem das questões
                const filterResponse = await fetch('/filter_questions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: uploadData.text,
                        subject: document.getElementById('subject').value
                    })
                });
                const filterData = await filterResponse.json();
                
                document.getElementById('result').textContent = filterData.filtered_questions;
            } catch (error) {
                console.error('Erro:', error);
                document.getElementById('result').textContent = 'Ocorreu um erro ao processar sua solicitação.';
            }
        });
    