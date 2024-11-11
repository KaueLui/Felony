import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Import necessário para manipulação da imagem
from generator import NFTGenerator

class NFTGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Felony | Gerador de NFTs")
        self.layer_dirs = []
        self.output_dir = ""
        self.generator = NFTGenerator()
        self.setup_ui()

    def setup_ui(self):
        # Interface gráfica: botões, lista de camadas e rótulos
        add_layer_button = tk.Button(self.root, text="Adicionar Camada", command=self.add_layer)
        add_layer_button.pack(pady=10)
        
        self.layer_list = tk.Listbox(self.root, width=50)
        self.layer_list.pack(pady=10)
        
        remove_layer_button = tk.Button(self.root, text="Remover Camada Selecionada", command=self.remove_layer)
        remove_layer_button.pack(pady=10)
        
        output_button = tk.Button(self.root, text="Selecionar Pasta de Saída", command=self.select_output_dir)
        output_button.pack(pady=10)
        
        self.output_label = tk.Label(self.root, text="Pasta de Saída: Não selecionada")
        self.output_label.pack(pady=10)
        
        # Entrada para quantidade máxima de NFTs
        tk.Label(self.root, text="Quantidade Máxima de NFTs:").pack(pady=5)
        self.max_nfts_entry = tk.Entry(self.root)
        self.max_nfts_entry.pack(pady=5)
        
        generate_button = tk.Button(self.root, text="Gerar NFTs", command=self.start_generation_thread)
        generate_button.pack(pady=20)

        # Campo de visualização da última imagem gerada
        self.preview_label = tk.Label(self.root, text="Pré-visualização da Última NFT Gerada:")
        self.preview_label.pack(pady=5)
        self.preview_canvas = tk.Label(self.root)
        self.preview_canvas.pack(pady=10)

    def add_layer(self):
        # Seleciona a pasta de uma camada
        layer_path = filedialog.askdirectory(title="Selecionar Pasta da Camada")
        if layer_path:
            layer_name = os.path.basename(layer_path)
            self.layer_dirs.append({"name": layer_name, "path": layer_path})
            self.layer_list.insert(tk.END, f"Camada: {layer_name} - Pasta: {layer_path}")

    def remove_layer(self):
        # Remove camada selecionada
        selected_index = self.layer_list.curselection()
        if selected_index:
            self.layer_dirs.pop(selected_index[0])
            self.layer_list.delete(selected_index)
        else:
            messagebox.showwarning("Aviso", "Selecione uma camada para remover.")

    def select_output_dir(self):
        # Seleciona a pasta de saída para as NFTs e os metadados
        self.output_dir = filedialog.askdirectory(title="Selecionar Pasta de Saída")
        if self.output_dir:
            self.output_label.config(text=f"Pasta de Saída: {self.output_dir}")

    def start_generation_thread(self):
        # Iniciar o processo de geração em uma nova thread para não congelar a interface
        thread = threading.Thread(target=self.generate_nfts)
        thread.start()

    def generate_nfts(self):
        if not self.output_dir:
            messagebox.showerror("Erro", "Selecione a pasta de saída!")
            return
        
        # Pega o valor de max_nfts e valida
        max_nfts = self.max_nfts_entry.get()
        if max_nfts.isdigit():
            max_nfts = int(max_nfts)
        else:
            messagebox.showerror("Erro", "Insira um número válido para a quantidade máxima de NFTs!")
            return

        # Chama o gerador de NFTs com o limite especificado
        self.generator.generate(self.layer_dirs, self.output_dir, max_nfts=max_nfts)
        messagebox.showinfo("Sucesso", "NFTs geradas com sucesso!")

        # Atualiza a pré-visualização com a última NFT gerada
        self.show_last_generated_image()

    def show_last_generated_image(self):
        # Encontra o último arquivo de imagem gerado no diretório de saída
        try:
            nfts_dir = os.path.join(self.output_dir, "nfts")
            images = [f for f in os.listdir(nfts_dir) if f.endswith(".png")]
            if not images:
                return

            last_image_path = os.path.join(nfts_dir, sorted(images)[-1])
            
            # Carrega e redimensiona a imagem para caber no canvas
            image = Image.open(last_image_path)
            image = image.resize((200, 200), Image.LANCZOS)  # Ajuste o tamanho conforme necessário
            image_tk = ImageTk.PhotoImage(image)

            # Atualiza o canvas de pré-visualização com a nova imagem
            self.preview_canvas.config(image=image_tk)
            self.preview_canvas.image = image_tk

        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFTGeneratorApp(root)
    root.mainloop()
