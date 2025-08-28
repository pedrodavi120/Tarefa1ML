import streamlit as st
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Define o título da aplicação
st.title("MNIST - Classificador Binário para o Dígito 5")
st.markdown("Desenhe um dígito abaixo e clique em 'Prever' para ver se o modelo o identifica como '5'.")

# --- Carregamento e Treinamento do Modelo ---
# Usamos o cache do Streamlit para carregar os dados e treinar o modelo apenas uma vez.
@st.cache_resource
def load_and_train_model():
    """
    Carrega o dataset MNIST, prepara os dados e treina um classificador SGD
    para a tarefa binária de identificar o dígito 5.
    """
    # Busca o dataset MNIST
    mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
    X, y = mnist["data"], mnist["target"]

    # Converte os rótulos para inteiros
    y = y.astype(np.uint8)

    # Divide os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]

    # Cria os rótulos para a classificação binária (5 ou não-5)
    y_train_5 = (y_train == 5)
    y_test_5 = (y_test == 5)

    # Normaliza os dados para melhorar o desempenho do SGD
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))

    # Cria e treina o classificador SGD (Stochastic Gradient Descent)
    sgd_clf = SGDClassifier(random_state=42)
    sgd_clf.fit(X_train_scaled, y_train_5)

    # Retorna o modelo treinado e o scaler
    return sgd_clf, scaler

# Exibe uma mensagem enquanto o modelo está sendo preparado
with st.spinner("Carregando dados e treinando o modelo... Por favor, aguarde."):
    model, scaler = load_and_train_model()

st.success("Modelo pronto para uso!")

# --- Interface do Canvas para Desenho ---
st.header("Desenhe o dígito aqui")

# Configurações do canvas
CANVAS_SIZE = 280
STROKE_WIDTH = 20
STROKE_COLOR = "#FFFFFF"  # Cor branca
BG_COLOR = "#000000"      # Cor preta

# Cria o canvas onde o usuário pode desenhar
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Cor de preenchimento (não usada no modo de desenho)
    stroke_width=STROKE_WIDTH,
    stroke_color=STROKE_COLOR,
    background_color=BG_COLOR,
    width=CANVAS_SIZE,
    height=CANVAS_SIZE,
    drawing_mode="freedraw",
    key="canvas",
)

# --- Lógica de Predição ---
if st.button("Prever"):
    if canvas_result.image_data is not None:
        # Pega a imagem desenhada do canvas
        img_data = canvas_result.image_data

        # Converte para uma imagem do Pillow em escala de cinza
        img = Image.fromarray(img_data.astype('uint8'), 'RGBA').convert('L')

        # Redimensiona a imagem para 28x28 pixels, o formato esperado pelo MNIST
        img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)

        # Converte a imagem para um array numpy e achata para um vetor de 784 posições
        img_array = np.array(img_resized).flatten().reshape(1, -1)

        # Normaliza os dados da imagem usando o mesmo scaler do treinamento
        img_scaled = scaler.transform(img_array)

        # Faz a predição com o modelo treinado
        prediction = model.predict(img_scaled)

        # Exibe o resultado
        st.subheader("Resultado da Predição:")
        if prediction[0]:
            st.success("O modelo previu que este dígito **É o número 5**.")
        else:
            st.error("O modelo previu que este dígito **NÃO é o número 5**.")

        # Opcional: Exibe a imagem processada para depuração
        st.write("Imagem processada (28x28):")
        st.image(img_resized, width=150)
    else:
        st.warning("Por favor, desenhe um dígito no canvas antes de prever.")
