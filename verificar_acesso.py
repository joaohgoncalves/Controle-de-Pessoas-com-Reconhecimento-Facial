import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

# Carregar o modelo treinado
reconhecedor = cv2.face.LBPHFaceRecognizer_create()
reconhecedor.read("modelo.yml")

# Detector de rosto
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Função para verificar o acesso
def verificar_acesso():
    cam = cv2.VideoCapture(0)
    
    while True:
        ret, img = cam.read()
        if not ret:
            break

        faces = detector.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            rosto_gray = cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            id_predito, confianca = reconhecedor.predict(rosto_gray)
            
            # Definir a confiança mínima para considerar um rosto autorizado
            if confianca < 70:
                messagebox.showinfo("Acesso Permitido", "Rosto autorizado! Acesso permitido.")
                cam.release()
                cv2.destroyAllWindows()
                return
            else:
                messagebox.showwarning("Acesso Negado", "Rosto não reconhecido. Acesso negado.")
                cam.release()
                cv2.destroyAllWindows()
                return
        
        cv2.imshow("Verificando Acesso", img)
        if cv2.waitKey(1) == ord("q"):  # Pressionar 'q' para sair
            break

    cam.release()
    cv2.destroyAllWindows()

# Interface gráfica
janela = tk.Tk()
janela.title("Verificação de Acesso")
janela.geometry("400x250")

# Labels e Botões
tk.Label(janela, text="Verificação de Acesso", font=("Helvetica", 14, "bold")).pack(pady=10)

btn_verificar = tk.Button(janela, text="Iniciar Verificação", command=verificar_acesso, width=25, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12))
btn_verificar.pack(pady=20)

btn_sair = tk.Button(janela, text="Sair", command=janela.quit, width=25, height=2, bg="#F44336", fg="white", font=("Helvetica", 12))
btn_sair.pack(pady=10)

janela.mainloop()
