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
        pass

    def generate(self, layers, output_dir, max_nfts=None, callback=None):
        image_output_dir = os.path.join(output_dir, "nfts")
        metadata_output_dir = os.path.join(output_dir, "metadata")
        os.makedirs(image_output_dir, exist_ok=True)
        os.makedirs(metadata_output_dir, exist_ok=True)
        
        layer_files = self.load_layer_files_with_rarity(layers)
        
        nft_id = 1
        metadata_list = []  # Para coletar todos os metadados para o CSV

        while nft_id <= max_nfts:
            combination = [self.select_random_item_with_rarity(layer) for layer in layer_files]
            output_path = os.path.join(image_output_dir, f"NFT_{nft_id}.png")
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
            fieldnames = ["name", "description", "image", "attributes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for metadata in metadata_list:
                writer.writerow(metadata)
        
        print("Geração de NFTs concluída.")

    def load_layer_files_with_rarity(self, layers):
        layer_files = []
        for layer in layers:
            rarity_files = {}
            for rarity in self.rarity_probabilities.keys():
                rarity_path = os.path.join(layer["path"], rarity)
                if os.path.isdir(rarity_path):
                    files = [{"name": layer["name"], "rarity": rarity, "file": os.path.join(rarity_path, f)}
                             for f in os.listdir(rarity_path) if f.endswith(".png")]
                    rarity_files[rarity] = files
            layer_files.append(rarity_files)
        return layer_files

    def select_random_item_with_rarity(self, layer_rarity_files):
        rarity = random.choices(
            population=list(self.rarity_probabilities.keys()),
            weights=list(self.rarity_probabilities.values()),
            k=1
        )[0]
        
        if rarity in layer_rarity_files and layer_rarity_files[rarity]:
            return random.choice(layer_rarity_files[rarity])
        else:
            available_rarities = [r for r in layer_rarity_files if layer_rarity_files[r]]
            if available_rarities:
                return random.choice(layer_rarity_files[random.choice(available_rarities)])
            else:
                raise ValueError("Nenhum item disponível para essa camada e raridade.")

    def create_metadata(self, nft_id, combination):
        metadata = {
            "name": f"NFT #{nft_id}",
            "description": "Uma NFT única",
            "image": f"ipfs://NFT_{nft_id}.png",
            "attributes": [
                {"trait_type": item["name"], "value": item["rarity"]}
                for item in combination
            ]
        }
        return metadata
