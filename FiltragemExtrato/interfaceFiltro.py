import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from filtro import processar_extratos
from bot import upload_files

def start_upload_thread():
    """Inicia a filtragem e upload em uma thread separada para não bloquear a interface."""
    caminho_extratos = entry_folder_path.get()
    thread = threading.Thread(target=processar_e_upload, args=(caminho_extratos,))
    thread.start()

def processar_e_upload(caminho_extratos):
    """Filtra os arquivos e realiza o upload."""
    arquivos_filtrados = processar_extratos(caminho_extratos)
    if arquivos_filtrados:
        upload_files(arquivos_filtrados)
        messagebox.showinfo("Sucesso", "Todos os arquivos foram enviados com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhum arquivo foi processado.")

def select_folder():
    """Abre uma janela de seleção de pasta e atualiza o campo de entrada."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder_path.delete(0, tk.END)  # Limpa o campo
        entry_folder_path.insert(0, folder_selected)  # Insere o novo caminho

# Configuração da interface gráfica
root = tk.Tk()
root.title("Bot de Upload e Filtragem")

# Rótulo e botão para selecionar a pasta de extratos
label_folder_path = tk.Label(root, text="Selecione a pasta com os extratos:")
label_folder_path.pack(pady=10)

entry_folder_path = tk.Entry(root, width=50)
entry_folder_path.pack(pady=10)

button_select_folder = tk.Button(root, text="Selecionar Pasta", command=select_folder)
button_select_folder.pack(pady=5)

# Botão para iniciar o upload
button_start = tk.Button(root, text="Iniciar Filtragem e Upload", command=start_upload_thread)
button_start.pack(pady=20)

# Iniciar a interface
root.mainloop()
