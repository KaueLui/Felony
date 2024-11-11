import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json  # Importa o módulo JSON
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
        # Interface gráfica: botões, lista de camadas e rótulos
        add_layer_button = tk.Button(self.root, text="Adicionar Camada", command=self.add_layer)
        add_layer_button.pack(pady=10)

        self.layer_list = tk.Listbox(self.root, width=50, selectmode=tk.MULTIPLE)  # Permitir múltiplas seleções
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

        # Checkbox para as opções "unique" e "exotic"
        self.unique_var = tk.BooleanVar()
        self.exotic_var = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Combinações Únicas", variable=self.unique_var).pack(pady=5)
        tk.Checkbutton(self.root, text="Apenas Itens Exóticos", variable=self.exotic_var).pack(pady=5)

        # Botão para gerar NFTs
        generate_button = tk.Button(self.root, text="Gerar NFTs", command=self.start_generation_thread)
        generate_button.pack(pady=20)

        # Campo de visualização da última imagem gerada
        self.preview_label = tk.Label(self.root, text="Pré-visualização da Última NFT Gerada:")
        self.preview_label.pack(pady=5)
        self.preview_canvas = tk.Label(self.root)
        self.preview_canvas.pack(pady=10)

        # Botões para salvar e carregar configurações
        save_config_button = tk.Button(self.root, text="Salvar Configurações", command=self.save_config)
        save_config_button.pack(pady=5)

        load_config_button = tk.Button(self.root, text="Carregar Configurações", command=self.load_config)
        load_config_button.pack(pady=5)

    def add_layer(self):
        # Permite a seleção de múltiplas pastas
        layer_paths = filedialog.askdirectory(title="Selecionar Pasta da Camada")
        if layer_paths:
            if isinstance(layer_paths, str):
                layer_paths = [layer_paths]  # Se for apenas uma pasta, transforma em lista
            for layer_path in layer_paths:
                layer_name = os.path.basename(layer_path)
                self.layer_dirs.append({"name": layer_name, "path": layer_path})
                self.layer_list.insert(tk.END, f"Camada: {layer_name} - Pasta: {layer_path}")

    def remove_layer(self):
        # Remove camadas selecionadas
        selected_indices = self.layer_list.curselection()
        if selected_indices:
            # Remover múltiplas camadas, da última para a primeira
            for index in reversed(selected_indices):
                self.layer_dirs.pop(index)
                self.layer_list.delete(index)
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

        # Passa as flags de 'unique' e 'exotic' para o gerador
        unique_only = self.unique_var.get()
        exotic_only = self.exotic_var.get()

        # Verifica se as camadas estão sendo passadas corretamente
        if not self.layer_dirs:
            messagebox.showerror("Erro", "Nenhuma camada foi selecionada!")
            return

        # Verifica se o gerador de NFTs está sendo corretamente inicializado
        self.generator = NFTGenerator(unique_only=unique_only, exotic_only=exotic_only)
        try:
            self.generator.generate(self.layer_dirs, self.output_dir, max_nfts=max_nfts, callback=self.update_preview)
            messagebox.showinfo("Sucesso", "NFTs geradas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar NFTs: {e}")

    def update_preview(self, image_path):
        # Atualiza a pré-visualização com a nova imagem gerada
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)  # Ajuste o tamanho conforme necessário
            image_tk = ImageTk.PhotoImage(image)

            # Atualiza o canvas de pré-visualização com a nova imagem
            self.preview_canvas.config(image=image_tk)
            self.preview_canvas.image = image_tk

        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def save_config(self):
        """Salvar configurações em um arquivo JSON."""
        config = {
            "layers": [{"name": layer["name"], "path": layer["path"]} for layer in self.layer_dirs],
            "output_dir": self.output_dir,
            "max_nfts": self.max_nfts_entry.get(),
            "unique_only": self.unique_var.get(),
            "exotic_only": self.exotic_var.get()
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

    def load_config(self):
        """Carregar configurações de um arquivo JSON."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                
                # Carregar as camadas
                self.layer_dirs = [{"name": layer["name"], "path": layer["path"]} for layer in config.get("layers", [])]
                self.layer_list.delete(0, tk.END)
                for layer in self.layer_dirs:
                    self.layer_list.insert(tk.END, f"Camada: {layer['name']} - Pasta: {layer['path']}")

                # Carregar o diretório de saída
                self.output_dir = config.get("output_dir", "")
                self.output_label.config(text=f"Pasta de Saída: {self.output_dir}")

                # Carregar a quantidade máxima de NFTs
                self.max_nfts_entry.delete(0, tk.END)
                self.max_nfts_entry.insert(0, config.get("max_nfts", ""))

                # Carregar as opções de filtros
                self.unique_var.set(config.get("unique_only", False))
                self.exotic_var.set(config.get("exotic_only", False))

                messagebox.showinfo("Sucesso", "Configurações carregadas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NFTGeneratorApp(root)
    root.mainloop()
