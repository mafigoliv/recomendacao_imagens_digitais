import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Função para localizar todas as imagens .png no diretório especificado
def get_star_image_paths(directory):
    return {os.path.splitext(f)[0]: os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')}

# Diretório das imagens das estrelas
star_image_directory = "D:/Git/recomendacao_imagens_digitais/estrelas"

# Função para localizar todas as imagens .jpg no diretório especificado
def get_image_paths(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]

# Diretório das imagens dos produtos
image_directory = "D:/Git/recomendacao_imagens_digitais/canecas"

# Função com os IDs, nomes, notas e imagens dos produtos
product_ids = [1, 2, 3, 4]
product_names = ["Caneca C++", "Caneca C#", "Caneca Java", "Caneca Python"]
ratings = [4.8, 5.0, 4.3, 5.0]
image_paths = get_image_paths(image_directory)

# Criar um dicionário para mapear o nome do produto ao caminho da imagem
image_dict = {os.path.splitext(os.path.basename(path))[0]: path for path in image_paths}

# Obter os caminhos das imagens correspondentes aos nomes dos produtos diretamente
ordered_image_paths = [image_dict[name.lower().replace(' ', '_')] for name in ["caneca_cpp", "caneca_csharp", "caneca_java", "caneca_python"]]

# Função para exibir as estrelas amarelas, a nota, os nomes dos produtos e as imagens das canecas
def display_all_products_ratings_stars_and_images(product_ids, ratings, product_names, image_paths, star_image_paths):
    # Dimensões da imagem (largura x altura)
    img_width, img_height = 1280, 720  # Ajustar para 1280x720 HD

    # Criar uma imagem em branco para exibir os títulos, as notas, as estrelas e as imagens
    img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255  # Imagem branca

    # Adicionar título no topo
    title = "Recomendacao de Imagens Digitais"
    cv2.putText(img, title, (int(img_width / 2) - 450, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)

    # Carregar e redimensionar as imagens das estrelas
    estrela_cheia = cv2.imread(star_image_paths["estrela_cheia"], cv2.IMREAD_UNCHANGED)
    estrela_meia = cv2.imread(star_image_paths["estrela_meia"], cv2.IMREAD_UNCHANGED)
    estrela_vazia = cv2.imread(star_image_paths["estrela_vazia"], cv2.IMREAD_UNCHANGED)
    if estrela_cheia is None or estrela_meia is None or estrela_vazia is None:
        print("Erro ao carregar as imagens das estrelas.")
        return
    estrela_cheia = cv2.resize(estrela_cheia, (32, 32))  # Redimensionar para 32x32 pixels
    estrela_meia = cv2.resize(estrela_meia, (32, 32))  # Redimensionar para 32x32 pixels
    estrela_vazia = cv2.resize(estrela_vazia, (32, 32))  # Redimensionar para 32x32 pixels

    y_offset = 200  # Ajuste da posição y inicial para os textos

    for i, (pid, rating, product_name, image_path) in enumerate(zip(product_ids, ratings, product_names, image_paths)):
        x_offset = 20 + i * 310  # Ajuste da posição x para cada produto, aumentando o espaçamento horizontal

        # Adicionar título do produto
        y_text_offset = y_offset
        cv2.putText(img, product_name, (x_offset, y_text_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        # Adicionar nota e estrelas
        y_rating_offset = y_text_offset + 50
        cv2.putText(img, f"{rating:.1f}", (x_offset, y_rating_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2, cv2.LINE_AA)

        x_star_offset = x_offset + 70
        y_star_offset = y_rating_offset - 30

        # Sobrepor a imagem das estrelas na imagem em branco com transparência
        full_stars = int(rating)
        half_star = (rating - full_stars) >= 0.5
        for j in range(5):  # Assumindo que a escala é de 5 estrelas
            if j < full_stars:
                star_to_use = estrela_cheia
            elif j == full_stars and half_star:
                star_to_use = estrela_meia
            else:
                star_to_use = estrela_vazia

            alpha_s = star_to_use[:, :, 3] / 255.0  # Canal alpha da imagem da estrela
            alpha_l = 1.0 - alpha_s  # Inverso do canal alpha

            for c in range(0, 3):  # Para os canais RGB
                if x_star_offset + star_to_use.shape[1] <= img_width and y_star_offset + star_to_use.shape[0] <= img_height:
                    img[y_star_offset:y_star_offset+star_to_use.shape[0], x_star_offset:x_star_offset+star_to_use.shape[1], c] = (
                        alpha_s * star_to_use[:, :, c] + alpha_l * img[y_star_offset:y_star_offset+star_to_use.shape[0], x_star_offset:x_star_offset+star_to_use.shape[1], c]
                    )
            x_star_offset += 32  # Ajuste do espaçamento horizontal entre as estrelas

        # Carregar e redimensionar a imagem da caneca
        product_img = cv2.imread(image_path)
        if product_img is None:
            print(f"Erro ao carregar a imagem do produto: {image_path}")
            continue
        product_img = cv2.resize(product_img, (300, 300))  # Ajustar a imagem da caneca para 300x300 pixels

        # Calcular a posição da imagem da caneca
        y_image_offset = y_rating_offset + 50
        x_image_offset = x_offset

        # Garantir que a posição da imagem está dentro dos limites
        if y_image_offset + product_img.shape[0] <= img_height and x_image_offset + product_img.shape[1] <= img_width:
            # Colocar a imagem da caneca na imagem em branco
            img[y_image_offset:y_image_offset+product_img.shape[0], x_image_offset:x_image_offset+product_img.shape[1]] = product_img

    # Verificar e criar a pasta de saída se não existir
    output_directory = "D:/Git/recomendacao_imagens_digitais/output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Gerar um nome de arquivo único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_directory, f"recomendacao_imagens{timestamp}.jpg")

    # Salvar a imagem na pasta de saída
    cv2.imwrite(output_path, img)
    print(f"Imagem salva como: {output_path}")

    # Exibir a imagem com os títulos, as estrelas, as notas e as imagens das canecas
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    print("Exibindo todos os produtos com suas respectivas notas, estrelas e imagens no centro da tela.")

# Obter os caminhos das imagens das estrelas
star_image_paths = get_star_image_paths(star_image_directory)

# Exibir todos os produtos com IDs, avaliações e imagens
display_all_products_ratings_stars_and_images(product_ids, ratings, product_names, ordered_image_paths, star_image_paths)
