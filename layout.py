import tkinter as tk
import subprocess
import os

def rodar_coletar_rosto():
    # Caminho absoluto para o script coletar_rostos.py
    caminho_coletar_rosto = "C:/Users/tinvi/Downloads/RECONHECIMENTO_FACIAL_COMPLETO/coletar_rostos.py"
    if os.path.exists(caminho_coletar_rosto):
        subprocess.run(["python", caminho_coletar_rosto])
    else:
        print("Arquivo coletar_rostos.py não encontrado.")

def rodar_verificar_acesso():
    caminho_verificar_acesso = "C:/Users/tinvi/Downloads/RECONHECIMENTO_FACIAL_COMPLETO/verificar_acesso.py"
    if os.path.exists(caminho_verificar_acesso):
        subprocess.run(["python", caminho_verificar_acesso])
    else:
        print("Arquivo verificar_acesso.py não encontrado.")

def rodar_gerenciar_pessoas():
    # Caminho absoluto para o script gerenciar_pessoas.py
    caminho_gerenciar_pessoas = "C:/Users/tinvi/Downloads/RECONHECIMENTO_FACIAL_COMPLETO/gerenciar_pessoas.py"
    if os.path.exists(caminho_gerenciar_pessoas):
        subprocess.run(["python", caminho_gerenciar_pessoas])
    else:
        print("Arquivo gerenciar_pessoas.py não encontrado.")

def sair():
    root.destroy()  # Fecha a janela principal

root = tk.Tk()
root.title("Reconhecimento Facial")
root.geometry("400x250")

tk.Label(root, text="Sistema de Reconhecimento Facial", font=("Helvetica", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

btn_cadastrar = tk.Button(frame, text="Cadastrar Rosto", command=rodar_coletar_rosto, width=25, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12))
btn_cadastrar.grid(row=0, column=0, padx=10, pady=5)

btn_verificar = tk.Button(frame, text="Verificar Acesso", command=rodar_verificar_acesso, width=25, height=2, bg="#FF5722", fg="white", font=("Helvetica", 12))
btn_verificar.grid(row=1, column=0, padx=10, pady=5)


btn_sair = tk.Button(frame, text="Sair", command=sair, width=25, height=2, bg="#F44336", fg="white", font=("Helvetica", 12))
btn_sair.grid(row=3, column=0, padx=10, pady=20)

root.mainloop()
