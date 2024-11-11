import os
import json
from PIL import Image
import itertools
from utils import create_metadata, create_nft_image

class NFTGenerator:
    def generate(self, layers, output_dir, max_nfts=None):
        # Diretórios de saída para imagens e metadados
        image_output_dir = os.path.join(output_dir, "nfts")
        metadata_output_dir = os.path.join(output_dir, "metadata")
        os.makedirs(image_output_dir, exist_ok=True)
        os.makedirs(metadata_output_dir, exist_ok=True)
        
        # Carregar todos os arquivos das camadas
        layer_files = self.load_layer_files(layers)
        
        # Combinar camadas e gerar NFTs
        nft_id = 1
        for combination in itertools.product(*layer_files):
            if max_nfts is not None and nft_id > max_nfts:
                break  # Para quando atingir o número máximo de NFTs
            
            output_path = os.path.join(image_output_dir, f"NFT_{nft_id}.png")
            metadata_path = os.path.join(metadata_output_dir, f"NFT_{nft_id}.json")
            create_nft_image(combination, output_path)
            metadata = create_metadata(nft_id, combination)
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)
            
            nft_id += 1

    def load_layer_files(self, layers):
        layer_files = []
        for layer in layers:
            files = [{"name": layer["name"], "file": os.path.join(layer["path"], f)} for f in os.listdir(layer["path"]) if f.endswith(".png")]
            layer_files.append(files)
        return layer_files
