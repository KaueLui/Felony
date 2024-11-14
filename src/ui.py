import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
from generator import NFTGenerator

class NFTGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Felony | Gerador de NFTs")
        self.layer_dirs = []  # Lista que armazenará as camadas e seus caminhos
        self.output_dir = ""
        self.generator = NFTGenerator()
        self.setup_ui()

    def setup_ui(self):
        add_layer_button = tk.Button(self.root, text="Adicionar Camada", command=self.add_layer)
        add_layer_button.pack(pady=10)

        self.layer_list = tk.Listbox(self.root, width=50, selectmode=tk.MULTIPLE)
        self.layer_list.pack(pady=10)

        remove_layer_button = tk.Button(self.root, text="Remover Camada Selecionada", command=self.remove_layer)
        remove_layer_button.pack(pady=10)

        output_button = tk.Button(self.root, text="Selecionar Pasta de Saída", command=self.select_output_dir)
        output_button.pack(pady=10)

        self.output_label = tk.Label(self.root, text="Pasta de Saída: Não selecionada")
        self.output_label.pack(pady=10)

        tk.Label(self.root, text="Quantidade Máxima de NFTs:").pack(pady=5)
        self.max_nfts_entry = tk.Entry(self.root)
        self.max_nfts_entry.pack(pady=5)

        generate_button = tk.Button(self.root, text="Gerar NFTs", command=self.start_generation_thread)
        generate_button.pack(pady=20)

        self.preview_label = tk.Label(self.root, text="Pré-visualização da Última NFT Gerada:")
        self.preview_label.pack(pady=5)
        self.preview_canvas = tk.Label(self.root)
        self.preview_canvas.pack(pady=10)

        save_config_button = tk.Button(self.root, text="Salvar Configurações", command=self.save_config)
        save_config_button.pack(pady=5)

        load_config_button = tk.Button(self.root, text="Carregar Configurações", command=self.load_config)
        load_config_button.pack(pady=5)

    def add_layer(self):
        layer_path = filedialog.askdirectory(title="Selecionar Pasta da Camada")
        if layer_path:
            layer_name = os.path.basename(layer_path)
            layer_items = self.load_items_from_directory(layer_path)
            self.layer_dirs.append({"name": layer_name, "path": layer_path, "items": layer_items})
            self.layer_list.insert(tk.END, f"Camada: {layer_name} - Pasta: {layer_path}")

    def load_items_from_directory(self, directory):
        items = []
        for filename in os.listdir(directory):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                rarity = "Exotic" if "exotic" in filename.lower() else "Common"
                items.append({"filename": filename, "rarity": rarity})
        return items

    def remove_layer(self):
        selected_indices = self.layer_list.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.layer_dirs.pop(index)
                self.layer_list.delete(index)
        else:
            messagebox.showwarning("Aviso", "Selecione uma camada para remover.")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Selecionar Pasta de Saída")
        if self.output_dir:
            self.output_label.config(text=f"Pasta de Saída: {self.output_dir}")

    def start_generation_thread(self):
        thread = threading.Thread(target=self.generate_nfts)
        thread.start()

    def generate_nfts(self):
        if not self.output_dir:
            messagebox.showerror("Erro", "Selecione a pasta de saída!")
            return

        max_nfts = self.max_nfts_entry.get()
        if max_nfts.isdigit():
            max_nfts = int(max_nfts)
        else:
            messagebox.showerror("Erro", "Insira um número válido para a quantidade máxima de NFTs!")
            return

        if not self.layer_dirs:
            messagebox.showerror("Erro", "Nenhuma camada foi selecionada!")
            return

        self.generator = NFTGenerator()
        try:
            self.generator.generate(self.layer_dirs, self.output_dir, max_nfts=max_nfts, callback=self.update_preview)
            messagebox.showinfo("Sucesso", "NFTs geradas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar NFTs: {e}")

    def update_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)
            self.preview_canvas.config(image=image_tk)
            self.preview_canvas.image = image_tk
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def save_config(self):
        config = {
            "layers": [{"name": layer["name"], "path": layer["path"]} for layer in self.layer_dirs],
            "output_dir": self.output_dir,
            "max_nfts": self.max_nfts_entry.get(),
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(config, f)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    config = json.load(f)

                self.layer_dirs = [
                    {"name": layer["name"], "path": layer["path"], "items": self.load_items_from_directory(layer["path"])}
                    for layer in config.get("layers", [])
                ]
                self.layer_list.delete(0, tk.END)
                for layer in self.layer_dirs:
                    self.layer_list.insert(tk.END, f"Camada: {layer['name']} - Pasta: {layer['path']}")

                self.output_dir = config.get("output_dir", "")
                self.output_label.config(text=f"Pasta de Saída: {self.output_dir}")

                self.max_nfts_entry.delete(0, tk.END)
                self.max_nfts_entry.insert(0, config.get("max_nfts", ""))

                messagebox.showinfo("Sucesso", "Configurações carregadas com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")
