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

## Contribution and Deployment

This project is licensed under the MIT License, which means you are free to:

- Use the code for any purpose.
- Modify and improve the project.
- Deploy the project in your own environments.

### How to contribute
1. Fork this repository.
2. Clone your fork to your local environment:
   ```bash
   git clone https://github.com/KaueLui/Felony.git
3. Create a new branch to work on your changes: 
     ```bash
   git checkout -b my-new-feature
4. After making your changes, submit them:
    ```bash
    git add .
    git commit -m "Description of the change"
    git push origin my-new-feature
5. Open a Pull Request in the original repository

