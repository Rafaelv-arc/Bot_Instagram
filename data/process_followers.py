import json
import os

def load_followers_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_followers_to_json(data, filename='followers_processed.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def process_followers(followers):
    processed_followers = []
    for follower in followers:
        # Separar cada linha de nome de usuário
        follower_lines = follower.split("\n")
        for line in follower_lines:
            # Remover "Seguir" e "Remover" e conteúdos indesejados
            line = line.strip()
            if "·" in line:
                line = line.split('·')[0].strip()
            if " " in line:
                line = line.split()[0].strip()

            # Checar se a string não está vazia e se é um nome de usuário válido
            if line and not line.startswith("Seguir") and not line.startswith("Remover"):
                url = f"https://www.instagram.com/{line}/"
                processed_followers.append(url)
                
    return processed_followers

# Exemplo de uso
if __name__ == "__main__":
    original_filename = 'data/followers.json'
    processed_filename = 'data/followers_processed.json'

    if not os.path.exists(original_filename):
        raise FileNotFoundError(f"Arquivo não encontrado: {original_filename}")

    followers_data = load_followers_from_json(original_filename)
    processed_data = process_followers(followers_data)
    save_followers_to_json(processed_data, processed_filename)

    print("Processamento concluído. URLs salvos em 'followers_processed.json'.")
