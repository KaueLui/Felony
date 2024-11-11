import os
import json
import random
import itertools
import argparse
from PIL import Image
from utils import create_metadata, create_nft_image

class NFTGenerator:
    # Definir as probabilidades para cada raridade
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

    def generate(self, layers, output_dir, max_nfts=None):
        # Diretórios de saída para imagens e metadados
        image_output_dir = os.path.join(output_dir, "nfts")
        metadata_output_dir = os.path.join(output_dir, "metadata")
        os.makedirs(image_output_dir, exist_ok=True)
        os.makedirs(metadata_output_dir, exist_ok=True)
        
        # Carregar arquivos das camadas considerando raridade
        layer_files = self.load_layer_files_with_rarity(layers)

        nft_id = 1

        if self.unique_only:
            # Modo de combinações únicas sem aleatoriedade
            combinations = itertools.product(*[layer for layer in layer_files.values()])
            for combination in combinations:
                if nft_id > max_nfts:
                    break
                self.create_nft(nft_id, combination, image_output_dir, metadata_output_dir)
                nft_id += 1

        elif self.exotic_only:
            # Modo exótico: selecionar apenas itens da raridade 'Exotic'
            combinations = [random.choice(layer_files["Exotic"]) for layer in layer_files]
            while nft_id <= max_nfts:
                self.create_nft(nft_id, combinations, image_output_dir, metadata_output_dir)
                nft_id += 1

        else:
            # Modo padrão aleatório, considerando todas as raridades
            while nft_id <= max_nfts:
                combination = [self.select_random_item_with_rarity(layer) for layer in layer_files]
                self.create_nft(nft_id, combination, image_output_dir, metadata_output_dir)
                nft_id += 1

        print("Geração de NFTs concluída.")

    def load_layer_files_with_rarity(self, layers):
        layer_files = []
        for layer in layers:
            rarity_files = {}
            # Para cada raridade, verificar se há uma pasta correspondente e carregar arquivos
            for rarity in self.rarity_probabilities.keys():
                rarity_path = os.path.join(layer["path"], rarity)
                if os.path.isdir(rarity_path):
                    files = [{"name": layer["name"], "rarity": rarity, "file": os.path.join(rarity_path, f)}
                             for f in os.listdir(rarity_path) if f.endswith(".png")]
                    rarity_files[rarity] = files
            layer_files.append(rarity_files)
        return layer_files

    def select_random_item_with_rarity(self, layer_rarity_files):
        # Seleciona a raridade com base nas probabilidades definidas
        rarity = random.choices(
            population=list(self.rarity_probabilities.keys()),
            weights=list(self.rarity_probabilities.values()),
            k=1
        )[0]
        
        # Seleciona um item aleatório da raridade escolhida
        if rarity in layer_rarity_files and layer_rarity_files[rarity]:
            return random.choice(layer_rarity_files[rarity])
        else:
            # Se não houver itens na raridade selecionada, selecionar outra raridade disponível
            available_rarities = [r for r in layer_rarity_files if layer_rarity_files[r]]
            if available_rarities:
                return random.choice(layer_rarity_files[random.choice(available_rarities)])
            else:
                raise ValueError("Nenhum item disponível para essa camada.")

    def create_nft(self, nft_id, combination, image_output_dir, metadata_output_dir):
        # Caminhos de saída para imagem e metadados
        output_path = os.path.join(image_output_dir, f"NFT_{nft_id}.png")
        metadata_path = os.path.join(metadata_output_dir, f"NFT_{nft_id}.json")

        # Log do progresso
        print(f"Gerando NFT {nft_id}...")

        # Criar a imagem e o arquivo de metadados
        create_nft_image(combination, output_path)
        metadata = create_metadata(nft_id, combination)
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Gerador de NFTs com suporte a raridades e exclusividade")
    parser.add_argument("layers", help="Diretório das camadas")
    parser.add_argument("output_dir", help="Diretório de saída para os NFTs gerados")
    parser.add_argument("-u", "--unique", action="store_true", help="Gera apenas combinações únicas, sem aleatoriedade")
    parser.add_argument("-e", "--exotic", action="store_true", help="Gera apenas combinações com itens da raridade 'Exotic'")
    parser.add_argument("-n", "--max_nfts", type=int, default=10, help="Número máximo de NFTs a serem geradas")
    
    args = parser.parse_args()

    # Instancia o gerador com base nas flags
    generator = NFTGenerator(unique_only=args.unique, exotic_only=args.exotic)
    generator.generate(args.layers, args.output_dir, max_nfts=args.max_nfts)

if __name__ == "__main__":
    main()
