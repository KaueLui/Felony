import os
from PIL import Image

def create_metadata(nft_id, layers):
    metadata = {
        "name": f"NFT #{nft_id}",
        "description": "Uma NFT gerada com camadas personalizadas.",
        "attributes": []
    }

    # Iterar sobre as camadas e incluir a raridade
    for layer in layers:
        rarity = layer["rarity"]  # A raridade será armazenada dentro de cada camada
        metadata["attributes"].append({
            "trait_type": layer["name"],
            "value": os.path.basename(layer["file"]),  # Nome do arquivo (item)
            "rarity": rarity  # A raridade associada ao item
        })

    return metadata

def create_nft_image(layers, output_path):
    # Inicializa a imagem base com a primeira camada
    base_image = Image.open(layers[0]["file"]).convert("RGBA")

    # Itera sobre as camadas restantes e compõe a imagem final
    for layer in layers[1:]:
        overlay = Image.open(layer["file"]).convert("RGBA")
        base_image = Image.alpha_composite(base_image, overlay)

    # Salva a imagem final gerada
    base_image.save(output_path)