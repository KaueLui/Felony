# FELONY | NFT Generator

This project is an NFT generator with a graphical interface. It allows you to create NFTs using image layers and generates metadata for each NFT.

## Project Structure
- `src/`: Source code of the application
- `assets/`: Example layers for NFT generation

```
├── assets/
│   ├── Background/
│   │   │   ├── Common/
│   │   │   ├── Rare/
│   │   │   ├── Epic/
│   │   │   ├── Legendary/
│   │   │   ├── Mythic/
│   │   │   └── Exotic/
│   │   └── Eyes/
│   │       ├── Common/
│   │       ├── Rare/
│   │       ├── Epic/
│   │       ├── Legendary/
│   │       ├── Mythic/
│   │       └── Exotic/

```

- `output/`: Folder where the NFTs and metadata are saved
- `requirements.txt`: Project dependencies

## How to Use
1. Install the dependencies with `pip install -r requirements.txt`.
2. Run the program: `python src/main.py or py src/main.py`.
3. Add layers, select the output folder, and click "Generate NFTs".

## Flags
1. `python src/generator.py assets -u`
2. `python src/generator.py assets -e`

- `-u`: generates only unique combinations.
- `-e`: generates an exotic combination
 
## Requirements
- Python 3.x
- Pillow
