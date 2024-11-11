import os
from PIL import Image

# Mapeamento de nomes de raridade para valores numéricos
RARITY_VALUES = {
    "Common": 1,
    "Rare": 2,
    "Epic": 3,
    "Legendary": 4,
    "Mythic": 5,
    "Exotic": 6
}

def create_metadata(nft_id, layers):
    metadata = {
        "name": f"NFT #{nft_id}",
        "description": "Uma NFT gerada com camadas personalizadas.",
        "attributes": [],
        "rarity_score": None  # Campo para média de raridade
    }

    total_rarity_value = 0
    valid_rarities_count = 0

    # Iterar sobre as camadas e incluir a raridade
    for layer in layers:
        rarity_name = layer.get("rarity", "Common")  # Usa "Common" como padrão se a raridade estiver ausente
        rarity_value = RARITY_VALUES.get(rarity_name, 1)  # Usa 1 (Common) caso a raridade não seja reconhecida
        
        # Soma o valor de raridade e conta camadas válidas
        total_rarity_value += rarity_value
        valid_rarities_count += 1

        metadata["attributes"].append({
            "trait_type": layer["name"],
            "value": os.path.basename(layer["file"]),  # Nome do arquivo (item)
            "rarity": rarity_name  # Nome da raridade associada ao item
        })

    # Calcula a média dos valores de raridade e determina a raridade geral
    average_rarity_value = total_rarity_value / valid_rarities_count if valid_rarities_count > 0 else 1
    # Encontra a raridade mais próxima baseada na média
    rounded_rarity_value = round(average_rarity_value)
    nft_rarity = [name for name, value in RARITY_VALUES.items() if value == rounded_rarity_value]
    metadata["rarity_score"] = nft_rarity[0] if nft_rarity else "Common"  # Define como "Common" caso não haja valor correspondente

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
