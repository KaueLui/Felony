import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import json
from generator import NFTGenerator

class NFTGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Felony | Gerador de NFTs")
        self.layer_dirs = []  
        self.output_dir = ""
        self.generator = NFTGenerator()
        self.generated_nfts_count = 0
        self.selected_rarities = set()
        self.setup_ui()

    def setup_ui(self):
        # Configuração da grid com 3 colunas: 0 (camadas/config), 1 (separador), 2 (preview)
        self.root.columnconfigure(0, weight=1, minsize=300)
        self.root.columnconfigure(1, weight=0, minsize=10)  # Separador
        self.root.columnconfigure(2, weight=2, minsize=500)

        # Frame para Camadas
        layers_frame = ttk.Frame(self.root, padding="10")
        layers_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        add_layer_button = ttk.Button(layers_frame, text="Adicionar Camada", command=self.add_layer)
        add_layer_button.grid(row=0, column=0, padx=5, pady=5)

        self.layer_list = tk.Listbox(layers_frame, width=50, selectmode=tk.MULTIPLE)
        self.layer_list.grid(row=1, column=0, padx=5, pady=5)

        remove_layer_button = ttk.Button(layers_frame, text="Remover Camada Selecionada", command=self.remove_layer)
        remove_layer_button.grid(row=2, column=0, padx=5, pady=5)

        # Frame para Saída
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        output_button = ttk.Button(output_frame, text="Selecionar Pasta de Saída", command=self.select_output_dir)
        output_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_label = ttk.Label(output_frame, text="Pasta de Saída: Não selecionada")
        self.output_label.grid(row=1, column=0, padx=5, pady=5)

        # Quantidade Máxima de NFTs
        max_nfts_frame = ttk.Frame(self.root, padding="10")
        max_nfts_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        ttk.Label(max_nfts_frame, text="Quantidade Máxima de NFTs:").grid(row=0, column=0, padx=5, pady=5)
        self.max_nfts_entry = ttk.Entry(max_nfts_frame)
        self.max_nfts_entry.grid(row=1, column=0, padx=5, pady=5)

        # Raridade
        rarity_frame = ttk.Frame(self.root, padding="10")
        rarity_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

        ttk.Label(rarity_frame, text="Escolha as Raridades:").grid(row=0, column=0, padx=5, pady=5)

        self.rarity_vars = {
            "Common": tk.BooleanVar(),
            "Rare": tk.BooleanVar(),
            "Epic": tk.BooleanVar(),
            "Legendary": tk.BooleanVar(),
            "Mythic": tk.BooleanVar(),
            "Exotic": tk.BooleanVar()
        }

        for idx, (rarity, var) in enumerate(self.rarity_vars.items()):
            chk = ttk.Checkbutton(rarity_frame, text=rarity, variable=var, command=self.update_selected_rarities)
            chk.grid(row=idx+1, column=0, sticky="w", padx=5, pady=5)

        # Formato de Imagem
        image_format_frame = ttk.Frame(self.root, padding="10")
        image_format_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)

        ttk.Label(image_format_frame, text="Formato de Imagem:").grid(row=0, column=0, padx=5, pady=5)
        self.image_format_var = tk.StringVar(value="png")
        image_format_menu = ttk.OptionMenu(image_format_frame, self.image_format_var, "png", "jpg", "jpeg")
        image_format_menu.grid(row=1, column=0, padx=5, pady=5)

        # Botão Gerar NFTs
        generate_button = ttk.Button(self.root, text="Gerar NFTs", command=self.start_generation_thread)
        generate_button.grid(row=5, column=0, padx=10, pady=20)

        # Linha de separação entre as colunas
        separator = ttk.Separator(self.root, orient="vertical")
        separator.grid(row=0, column=1, rowspan=6, sticky="ns", padx=10)

        # Tela de Preview da NFT
        preview_frame = ttk.Frame(self.root, padding="10")
        preview_frame.grid(row=0, column=2, rowspan=6, sticky="nsew", padx=10, pady=5)

        self.preview_label = ttk.Label(preview_frame, text="Pré-visualização da Última NFT Gerada:")
        self.preview_label.grid(row=0, column=0, padx=5, pady=5)

        self.preview_canvas = ttk.Label(preview_frame)
        self.preview_canvas.grid(row=1, column=0, padx=5, pady=10)

        self.generated_nfts_label = ttk.Label(preview_frame, text="NFTs Geradas: 0")
        self.generated_nfts_label.grid(row=2, column=0, padx=5, pady=5)

        # Salvar e Carregar Configurações
        config_frame = ttk.Frame(self.root, padding="10")
        config_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        save_config_button = ttk.Button(config_frame, text="Salvar Configurações", command=self.save_config)
        save_config_button.grid(row=0, column=0, padx=5, pady=5)

        load_config_button = ttk.Button(config_frame, text="Carregar Configurações", command=self.load_config)
        load_config_button.grid(row=0, column=1, padx=5, pady=5)

    def update_selected_rarities(self):
        self.selected_rarities = {rarity for rarity, var in self.rarity_vars.items() if var.get()}

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
            if max_nfts < 1 or max_nfts > 10000:
                messagebox.showerror("Erro", "O número máximo de NFTs deve ser entre 1 e 10.000.")
                return
        else:
            messagebox.showerror("Erro", "Insira um número válido para a quantidade máxima de NFTs!")
            return

        if not self.layer_dirs:
            messagebox.showerror("Erro", "Nenhuma camada foi adicionada!")
            return

        try:
            image_format = self.image_format_var.get()
            selected_rarities = self.selected_rarities

            def update_count(image_path):
                self.generated_nfts_count += 1
                self.update_preview(image_path)
                self.update_generated_count_label()

            self.generator.generate(self.layer_dirs, self.output_dir, max_nfts=max_nfts,
                                    image_format=image_format, rarities=selected_rarities,
                                    callback=update_count)
            messagebox.showinfo("Sucesso", "NFTs geradas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar NFTs: {e}")

    def update_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)
            self.preview_canvas.config(image=image_tk)
            self.preview_canvas.image = image_tk
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def update_generated_count_label(self):
        self.generated_nfts_label.config(text=f"NFTs Geradas: {self.generated_nfts_count}")

    def save_config(self):
        config = {
            "layers": [{"name": layer["name"], "path": layer["path"]} for layer in self.layer_dirs],
            "output_dir": self.output_dir,
            "max_nfts": self.max_nfts_entry.get(),
            "image_format": self.image_format_var.get(),
            "rarities": list(self.selected_rarities)
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

                image_format = config.get("image_format", "png")
                self.image_format_var.set(image_format)

                rarities = config.get("rarities", [])
                for rarity, var in self.rarity_vars.items():
                    var.set(rarity in rarities)
                self.update_selected_rarities()

                messagebox.showinfo("Sucesso", "Configurações carregadas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")
