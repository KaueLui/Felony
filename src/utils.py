import os
from PIL import Image

def create_metadata(nft_id, layers):
    metadata = {
        "name": f"NFT #{nft_id}",
        "description": "Uma NFT gerada com camadas personalizadas.",
        "attributes": [{"trait_type": layer["name"], "value": os.path.basename(layer["file"])} for layer in layers]
    }
    return metadata

def create_nft_image(layers, output_path):
    base_image = Image.open(layers[0]["file"]).convert("RGBA")
    for layer in layers[1:]:
        overlay = Image.open(layer["file"]).convert("RGBA")
        base_image = Image.alpha_composite(base_image, overlay)
    base_image.save(output_path)
