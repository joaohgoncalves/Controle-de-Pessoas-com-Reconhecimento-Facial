import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

# Pasta onde os rostos serão armazenados
caminho = "rostos_autorizados"
if not os.path.exists(caminho):
    os.makedirs(caminho)

# Detector e reconhecedor
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.LBPHFaceRecognizer_create()

# Função para gerar um novo ID automaticamente
def gerar_novo_id():
    ids = []
    for arquivo in os.listdir(caminho):
        try:
            id_ = int(arquivo.split("_")[1])
            ids.append(id_)
        except:
            continue
    return max(ids, default=0) + 1

# Função para verificar se o rosto já foi cadastrado
def verificar_rosto_existente(rosto):
    # Converter a imagem para escala de cinza
    rosto_gray = cv2.cvtColor(rosto, cv2.COLOR_BGR2GRAY)
    
    reconhecedor.read("modelo.yml")  # Carregar o modelo treinado
    id_predito, confianca = reconhecedor.predict(rosto_gray)
    
    if confianca < 70:  # Se a confiança for alta, significa que já existe o rosto
        return True
    return False

# Função para cadastrar rosto
def cadastrar_rosto():
    if not entry_nome.get() or not entry_telefone.get():
        messagebox.showwarning("Aviso", "Por favor, preencha o nome e o telefone.")
        return
    
    id_pessoa = gerar_novo_id()
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    amostras = 0
    cam = cv2.VideoCapture(0)
    
    # Exibir mensagem de progresso
    status_label.config(text="Capturando rosto, por favor, aguarde...")
    
    while True:
        ret, img = cam.read()
        if not ret:
            break

        faces = detector.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            amostras += 1
            rosto = cv2.resize(img[y:y+h, x:x+w], (220, 220))

            # Verificar se o rosto já foi cadastrado
            if verificar_rosto_existente(rosto):
                messagebox.showwarning("Aviso", "Este rosto já está cadastrado.")
                cam.release()
                cv2.destroyAllWindows()
                return  # Impede o cadastro do rosto

            cv2.imwrite(f"{caminho}/pessoa_{id_pessoa}_{amostras}.jpg", rosto)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Coletando rostos", img)
        if cv2.waitKey(1) == ord("q") or amostras >= 25:
            break

    cam.release()
    cv2.destroyAllWindows()
    
    # Mensagem de sucesso
    messagebox.showinfo("Cadastro", f"Rosto cadastrado com sucesso!\nNome: {nome}\nTelefone: {telefone}")
    status_label.config(text="Cadastro concluído com sucesso!")
    
    # Desabilitar os campos de entrada para nome e telefone
    entry_nome.config(state="disabled")
    entry_telefone.config(state="disabled")
    btn_cadastrar.config(state="disabled")  # Desabilitar o botão de cadastro

# Função para treinar o modelo
def treinar_modelo():
    imagens, ids = [], []

    for arquivo in os.listdir(caminho):
        img_path = os.path.join(caminho, arquivo)
        imagem = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        id_pessoa = int(arquivo.split("_")[1])
        faces = detector.detectMultiScale(imagem)

        for (x, y, w, h) in faces:
            imagens.append(imagem[y:y+h, x:x+w])
            ids.append(id_pessoa)

    if imagens:
        reconhecedor.train(imagens, np.array(ids))
        reconhecedor.write("modelo.yml")

# Função para reiniciar a tela principal
def reiniciar_tela():
    entry_nome.config(state="normal")
    entry_telefone.config(state="normal")
    entry_nome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    btn_cadastrar.config(state="disabled")

    # Limpar o status
    status_label.config(text="Preencha os dados para cadastrar um novo usuário.")
    btn_cadastrar.config(state="disabled")  # Reabilitar o botão apenas quando os campos estiverem preenchidos

# Função para verificar os campos de nome e telefone
def verificar_campos():
    if entry_nome.get() and entry_telefone.get():
        btn_cadastrar.config(state="normal")  # Ativar o botão
    else:
        btn_cadastrar.config(state="disabled")  # Desativar o botão

# Interface gráfica
janela = tk.Tk()
janela.title("Cadastro e Verificação de Rosto")
janela.geometry("400x350")
janela.resizable(False, False)

# Labels e Entradas para nome e telefone
label_nome = tk.Label(janela, text="Nome", font=("Arial", 12))
label_nome.pack(pady=5)

entry_nome = tk.Entry(janela, font=("Arial", 12))
entry_nome.pack(pady=5)

label_telefone = tk.Label(janela, text="Telefone", font=("Arial", 12))
label_telefone.pack(pady=5)

entry_telefone = tk.Entry(janela, font=("Arial", 12))
entry_telefone.pack(pady=5)

# Status de progresso
status_label = tk.Label(janela, text="Preencha os dados para cadastrar um novo usuário.", font=("Arial", 10), fg="gray")
status_label.pack(pady=10)

# Botões
btn_cadastrar = tk.Button(janela, text="Cadastrar Usuário", font=("Arial", 12), command=lambda: [cadastrar_rosto(), treinar_modelo()])
btn_cadastrar.pack(pady=10)
btn_cadastrar.config(state="disabled")  # Iniciar desabilitado

btn_sair = tk.Button(janela, text="Sair", font=("Arial", 12), command=janela.quit)
btn_sair.pack(pady=10)

# Monitorar a mudança nos campos de nome e telefone
entry_nome.bind("<KeyRelease>", lambda event: verificar_campos())
entry_telefone.bind("<KeyRelease>", lambda event: verificar_campos())

janela.mainloop()
