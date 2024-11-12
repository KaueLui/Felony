import os
import random
import itertools
import json
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

    def __init__(self, unique_only=False, exotic_only=False):
        self.unique_only = unique_only
        self.exotic_only = exotic_only

    def generate(self, layers, output_dir, max_nfts=None, callback=None):
        image_output_dir = os.path.join(output_dir, "nfts")
        metadata_output_dir = os.path.join(output_dir, "metadata")
        os.makedirs(image_output_dir, exist_ok=True)
        os.makedirs(metadata_output_dir, exist_ok=True)
        
        layer_files = self.load_layer_files_with_rarity(layers)

        # Exibição simplificada das camadas e raridades carregadas
        print("Camadas e raridades carregadas:")
        for i, layer in enumerate(layer_files):
            raridades_disponiveis = [raridade for raridade in layer.keys() if layer[raridade]]
            print(f"Camada {i + 1}: {raridades_disponiveis}")
        
        nft_id = 1

        if self.unique_only:
            for rarity in self.rarity_probabilities.keys():
                if not all(rarity in layer and layer[rarity] for layer in layer_files):
                    print(f"Erro: Camada com raridade '{rarity}' está vazia em uma ou mais camadas.")
                    continue
                
                combinations = itertools.product(*[layer[rarity] for layer in layer_files])
                for combination in combinations:
                    if nft_id > max_nfts:
                        break
                    self.create_nft(nft_id, combination, image_output_dir, metadata_output_dir, callback)
                    nft_id += 1

        elif self.exotic_only:
            combinations = [random.choice(layer["Exotic"]) for layer in layer_files if "Exotic" in layer and layer["Exotic"]]
            if not combinations:
                raise ValueError("Nenhum item exótico encontrado em alguma das camadas.")
            while nft_id <= max_nfts:
                self.create_nft(nft_id, combinations, image_output_dir, metadata_output_dir, callback)
                nft_id += 1

        else:
            while nft_id <= max_nfts:
                combination = [self.select_random_item_with_rarity(layer) for layer in layer_files]
                print("Combinação gerada:", [(item["name"], item["rarity"]) for item in combination]) # Debug: imprime a combinação para verificação
                self.create_nft(nft_id, combination, image_output_dir, metadata_output_dir, callback)
                nft_id += 1

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

    def create_nft(self, nft_id, combination, image_output_dir, metadata_output_dir, callback):
        output_path = os.path.join(image_output_dir, f"NFT_{nft_id}.png")
        metadata_path = os.path.join(metadata_output_dir, f"NFT_{nft_id}.json")

        print(f"Gerando NFT {nft_id}...")

        create_nft_image(combination, output_path)
        metadata = create_metadata(nft_id, combination)
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        if callback:
            callback(output_path)
