import tkinter as tk
from ui import NFTGeneratorApp
import requests
import zipfile
import os
import shutil
import sys

UPDATE_URL = "https://github.com/KaueLui/Felony/blob/main/json/version.json"  # Substitua pelo link do arquivo remoto

def check_for_updates():
    try:
        print("Verificando atualizações...")
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        remote_data = response.json()
        remote_version = remote_data.get("version")
        download_url = remote_data.get("download_url")

        # Verificar a versão atual
        current_version = "1.0.0"  # Atualize com a versão do seu programa
        if remote_version > current_version:
            user_response = input(f"Nova versão encontrada: {remote_version}. Deseja atualizar? (s/n): ")
            if user_response.lower() == 's':
                download_and_install_update(download_url)
            else:
                print("Atualização ignorada.")
        else:
            print("Você já está na versão mais recente.")
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")

def download_and_install_update(download_url):
    try:
        print("Baixando atualização...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Salvar arquivo ZIP temporariamente
        with open("update.zip", "wb") as update_file:
            for chunk in response.iter_content(chunk_size=1024):
                update_file.write(chunk)

        # Extrair os arquivos
        print("Instalando atualização...")
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall("update_temp")

        # Substituir os arquivos do programa
        for item in os.listdir("update_temp"):
            src_path = os.path.join("update_temp", item)
            dest_path = os.path.join(os.getcwd(), item)
            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.move(src_path, dest_path)
            else:
                shutil.move(src_path, dest_path)

        # Limpar arquivos temporários
        os.remove("update.zip")
        shutil.rmtree("update_temp")

        print("Atualização concluída. Reiniciando o programa...")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Erro ao instalar atualização: {e}")

if __name__ == "__main__":
    # Verificar atualizações antes de iniciar o programa
    check_for_updates()

    # Iniciar a aplicação
    root = tk.Tk()
    app = NFTGeneratorApp(root)
    root.mainloop()
