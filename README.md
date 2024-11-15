# Felony | NFT Generator

This project is an NFT generator with a graphical interface. It allows you to create NFTs using image layers and generates metadata for each NFT.

## Project Structure
- `src/`: Source code of the application
- `assets/`: Example layers for NFT generation
- `output/`: Folder where the NFTs and metadata are saved
- `requirements.txt`: Project dependencies

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

## How to Use
1. Install the dependencies with `pip install -r requirements.txt`.
2. Run the program: `python src/main.py or py src/main.py`.
3. Add layers, select the output folder, and click "Generate NFTs".

## Features
1. You can generate images with the rarities you want
2. Generates a maximum of 10,000 image units
3. You have a preview of the generated images
4. Simple and straightforward interface
5. You can save and load system configurations through a .json file

## Requirements
- Python 3.x
- Pillow
