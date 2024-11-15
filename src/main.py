import tkinter as tk
from ui import NFTGeneratorApp
import requests
import zipfile
import os
import shutil
import sys
import json

UPDATE_URL = "https://raw.githubusercontent.com/KaueLui/Felony/main/json/version.json"  # URL do JSON de versão no GitHub

def check_for_updates():
    """
    Verifica no repositório remoto se há uma nova versão disponível.
    """
    try:
        print("Verificando atualizações...")
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        remote_data = response.json()
        remote_version = remote_data.get("version")
        download_url = remote_data.get("download_url")

        if not remote_version or not download_url:
            print("Informações de versão ou URL de download ausentes no arquivo remoto.")
            return

        # Versão atual do programa
        current_version = "1.0.0"  # Atualize para a versão atual do programa
        if remote_version > current_version:
            user_response = input(f"Nova versão {remote_version} disponível! Deseja atualizar? (s/n): ")
            if user_response.lower() == 's':
                download_and_install_update(download_url)
            else:
                print("Atualização ignorada pelo usuário.")
        else:
            print("Você já está usando a versão mais recente.")
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")

def download_and_install_update(download_url):
    """
    Faz o download da nova versão e instala os arquivos atualizados.
    """
    try:
        print("Baixando atualização...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Salvar o arquivo ZIP de atualização
        with open("update.zip", "wb") as update_file:
            for chunk in response.iter_content(chunk_size=1024):
                update_file.write(chunk)

        # Extrair os arquivos para um diretório temporário
        print("Instalando atualização...")
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall("update_temp")

        # Substituir os arquivos da aplicação
        for item in os.listdir("update_temp"):
            src_path = os.path.join("update_temp", item)
            dest_path = os.path.join(os.getcwd(), item)

            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.move(src_path, dest_path)
            else:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                shutil.move(src_path, dest_path)

        # Remover arquivos temporários
        os.remove("update.zip")
        shutil.rmtree("update_temp")

        print("Atualização concluída. Reiniciando o programa...")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Erro ao instalar atualização: {e}")

if __name__ == "__main__":
    # Verifica atualizações antes de iniciar a aplicação
    check_for_updates()

    # Inicia a interface principal
    root = tk.Tk()
    app = NFTGeneratorApp(root)
    root.mainloop()
