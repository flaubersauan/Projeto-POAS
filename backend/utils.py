import requests
import os

def get_data(url, params = None, headers = None):
    request = requests.get(url, params, headers=headers)

    try:
        data = request.json()
    except Exception as e:
        print(e)

    return data

def gerar_env():
    if not os.path.exists(".env"):
        vars = {
            "TMDB_API_KEY": "insira_a_chave_da_api"
        }
        
        lines = []
        for key, value in vars.items():
            lines.append(f"{key}={value}\n")

        with open(".env", "w") as file:
            file.writelines(lines)
        print("="*45)
        print("\nINSIRA A CHAVE DA API TMDB NO .env\n")
        print("="*45)