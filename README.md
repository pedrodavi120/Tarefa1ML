Streamlit App: Classificador Binário MNISTEste é um Data App desenvolvido com Streamlit que utiliza um modelo de Machine Learning (SGDClassifier) para realizar uma classificação binária. O objetivo do modelo é identificar se um dígito desenhado à mão é o número 5 ou não.A aplicação utiliza a biblioteca streamlit-drawable-canvas para permitir que o usuário desenhe um dígito em tempo real e obtenha a predição do modelo.Como Executar o ProjetoSiga os passos abaixo para executar a aplicação em seu ambiente local.Pré-requisitosPython 3.8 ou superiorpip (gerenciador de pacotes do Python)PassosClone o repositório:git clone https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git
cd NOME_DO_SEU_REPOSITORIO
Crie um ambiente virtual (recomendado):python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências:Crie um arquivo requirements.txt com o conteúdo abaixo e execute o comando pip:streamlit
streamlit-drawable-canvas
numpy
scikit-learn
pandas
Pillow
```bash
pip install -r requirements.txt
Execute a aplicação Streamlit:No terminal, execute o seguinte comando:streamlit run app.py
A aplicação será aberta automaticamente no seu navegador.Print da Aplicação em FuncionamentoSubstitua a imagem abaixo por um print da sua aplicação rodando.
