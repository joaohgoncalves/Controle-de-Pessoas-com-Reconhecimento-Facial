import cv2
import numpy as np
import os

detector_face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.LBPHFaceRecognizer_create()

caminho = "rostos_autorizados"
imagens, ids = [], []

for arquivo in os.listdir(caminho):
    img_path = os.path.join(caminho, arquivo)
    imagem = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    id_pessoa = int(arquivo.split("_")[1])
    faces = detector_face.detectMultiScale(imagem)

    for (x, y, w, h) in faces:
        imagens.append(imagem[y:y+h, x:x+w])
        ids.append(id_pessoa)

reconhecedor.train(imagens, np.array(ids))
reconhecedor.write("modelo.yml")
print("Treinamento concluído com sucesso!")
