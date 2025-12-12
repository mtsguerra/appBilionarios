import os
import sys
import subprocess

def find_and_run():
    target_file = 'server.py'
    required_db = 'b.db'

    print(f"Procurando por {target_file} nas subpastas...")

    # Percorre todas as pastas a partir de onde o script está
    for root, dirs, files in os.walk('.'):
        if target_file in files:
            # Encontrou o arquivo!
            print(f"--> Encontrado em: {root}")

            # Verifica se o banco de dados também está lá (segurança extra)
            if required_db not in files:
                print(f"AVISO: {required_db} não está na mesma pasta que {target_file}. O banco pode falhar.")

            # Muda o diretório de trabalho para a pasta do arquivo
            os.chdir(root)

            # Adiciona o diretório atual ao path do Python para importar módulos locais
            sys.path.append(os.getcwd())

            print("Iniciando a aplicação Flask...\n")
            print("-" * 40)

            # Executa o servidor usando o mesmo interpretador Python atual
            try:
                subprocess.call([sys.executable, target_file])
            except KeyboardInterrupt:
                print("\nServidor parado pelo usuário.")
            return

    print(f"ERRO: Não foi possível encontrar o arquivo {target_file} neste projeto.")

if __name__ == "__main__":
    find_and_run()