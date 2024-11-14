import os
import random
import json
import csv
from PIL import Image
from utils import create_metadata, create_nft_image

class NFTGenerator:
    rarity_probabilities = {
        "Common": 0.50,
        "Rare": 0.25,
        "Epic": 0.15,
        "Legendary": 0.07,
        "Mythic": 0.02,
        "Exotic": 0.01,
    }

    def __init__(self):
        self.generated_combinations = set()  # Armazena combinações únicas

    def generate(self, layers, output_dir, max_nfts=None, image_format="png", callback=None, rarities=None):
        """
        Gera NFTs com base nas camadas, raridades selecionadas e outros parâmetros.

        Args:
            layers (list): Lista de camadas com caminhos e itens.
            output_dir (str): Diretório de saída para imagens e metadados.
            max_nfts (int): Quantidade máxima de NFTs a serem geradas.
            image_format (str): Formato de saída das imagens ("png", "jpg", etc).
            callback (function): Função de callback para cada imagem gerada.
            rarities (set): Conjunto de raridades selecionadas pelo usuário.
        """
        image_output_dir = os.path.join(output_dir, "nfts")
        metadata_output_dir = os.path.join(output_dir, "metadata")
        os.makedirs(image_output_dir, exist_ok=True)
        os.makedirs(metadata_output_dir, exist_ok=True)

        # Carrega os arquivos das camadas com base nas raridades escolhidas
        layer_files = self.load_layer_files_with_rarity(layers, rarities)

        nft_id = 1
        metadata_list = []  # Para coletar todos os metadados para o CSV

        while nft_id <= max_nfts:
            # Garante uma combinação única para cada NFT
            combination = None
            combination_tuple = None
            attempt_count = 0
            while combination_tuple is None or combination_tuple in self.generated_combinations:
                if attempt_count > 100:
                    raise ValueError("Não foi possível gerar uma combinação única após 100 tentativas.")
                combination = [self.select_random_item_with_rarity(layer) for layer in layer_files]
                # Converte a combinação para uma tupla hashável
                combination_tuple = tuple((item["name"], item["rarity"], item["file"]) for item in combination)
                attempt_count += 1

            # Registra a combinação como única
            self.generated_combinations.add(combination_tuple)

            # Define o caminho de saída para a imagem e o metadata
            output_path = os.path.join(image_output_dir, f"NFT_{nft_id}.{image_format}")
            metadata_path = os.path.join(metadata_output_dir, f"NFT_{nft_id}.json")

            # Cria a imagem NFT
            create_nft_image(combination, output_path)

            # Gera metadados no formato ERC-1155 (sem o campo "decimals")
            metadata = self.create_metadata(nft_id, combination)

            # Escreve o JSON do metadata individualmente
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)

            metadata_list.append(metadata)  # Adiciona à lista de metadados para o CSV

            # Log da geração de cada NFT no terminal
            print(f"NFT {nft_id} gerada: {metadata['name']} com atributos: {metadata['attributes']}")

            if callback:
                callback(output_path)

            nft_id += 1

        # Gera o arquivo CSV com todos os metadados
        csv_path = os.path.join(output_dir, "metadata.csv")
        with open(csv_path, "w", newline='') as csvfile:
            fieldnames = ["name", "description", "image", "attributes", "external_url"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for metadata in metadata_list:
                writer.writerow(metadata)

        print("Geração de NFTs concluída.")

    def load_layer_files_with_rarity(self, layers, rarities):
        """
        Carrega arquivos das camadas filtrando pelos diretórios de raridades selecionadas.

        Args:
            layers (list): Lista de camadas com caminhos e itens.
            rarities (set): Conjunto de raridades escolhidas.

        Returns:
            list: Lista de arquivos das camadas filtrados por raridade.
        """
        layer_files = []
        for layer in layers:
            rarity_files = {}
            for rarity in self.rarity_probabilities.keys():
                if rarities and rarity not in rarities:
                    continue  # Ignora raridades não selecionadas
                rarity_path = os.path.join(layer["path"], rarity)
                if os.path.isdir(rarity_path):
                    files = [{"name": layer["name"], "rarity": rarity, "file": os.path.join(rarity_path, f)}
                             for f in os.listdir(rarity_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
                    if files:
                        rarity_files[rarity] = files
            
            if not rarity_files:
                print(f"Aviso: Nenhum item disponível para a camada '{layer['name']}' nas raridades selecionadas.")

            layer_files.append(rarity_files)
        return layer_files

    def select_random_item_with_rarity(self, layer_rarity_files):
        """
        Seleciona um item aleatório de acordo com as probabilidades de raridade.

        Args:
            layer_rarity_files (dict): Arquivos das camadas filtrados por raridade.

        Returns:
            dict: Item selecionado aleatoriamente.
        """
        available_rarities = [r for r in self.rarity_probabilities.keys() if r in layer_rarity_files and layer_rarity_files[r]]
        
        if not available_rarities:
            raise ValueError("Nenhum item disponível para essa camada e raridade.")

        rarity = random.choices(
            population=available_rarities,
            weights=[self.rarity_probabilities[r] for r in available_rarities],
            k=1
        )[0]

        return random.choice(layer_rarity_files[rarity])

    def create_metadata(self, nft_id, combination):
        """
        Cria os metadados para uma NFT.

        Args:
            nft_id (int): ID da NFT.
            combination (list): Lista de itens (camadas) na NFT.

        Returns:
            dict: Metadados da NFT.
        """
        metadata = {
            "name": f"NFT #{nft_id}",
            "description": "Uma NFT única",
            "image": f"https://example.com/image/{nft_id}.png",
            "external_url": f"https://example.com/nft/{nft_id}",
            "attributes": [
                {"trait_type": item["name"], "value": item["rarity"]}
                for item in combination
            ]
        }
        return metadata
