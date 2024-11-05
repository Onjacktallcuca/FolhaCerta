import schedule
import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Caminho para o Google Chrome e o ChromeDriver
chrome_path = "C:/Users/gvmn/AppData/Local/Google/Chrome/Application/chrome.exe"
driver_path = "C:/Program Files/chromedriver-win64/chromedriver.exe"


def iniciar_chrome_com_debug():
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222", "--user-data-dir=C:/chrome_dev_profile"], shell=False)
    time.sleep(5)


def marcar_ponto():
    # Configurar o Chrome para usar a depuração remota
    chrome_options = Options()
    chrome_options.debugger_address = "localhost:9222"

    # Criar o objeto Service com o caminho do ChromeDriver
    service = Service(executable_path=driver_path)

    # Roda o WebDriver com sessão existente
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Acessar o site usando a janela existente
    driver.get("https://portal.folhacerta.com/#/dashboard/minhas-rotinas/web-ponto")

    # Criar o metodo de login após os testes beta...

    # Esperar o carregamento da página
    time.sleep(6)

    # Localizar o botão "MARCAR PONTO" e clicar nele
    try:
        marcar_ponto_button = driver.find_element(By.XPATH, "//button[contains(., 'MARCAR') and contains(., 'PONTO')]")
        marcar_ponto_button.click()
        print("Botão 'MARCAR PONTO' clicado com sucesso!")

        # Aguardar um tempo para que a janela de confirmação apareça
        time.sleep(4)

        # Localizar o botão "Confirmar Marcação" e clicar nele
        confirmar_button = driver.find_element(By.XPATH, "//button[contains(., 'Confirmar Marcação')]")
        confirmar_button.click()
        print("Botão 'Confirmar Marcação' clicado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

    # Fechar o navegador se necessário
    # driver.quit()


# Agenda a execução com o atraso aleatório
def agendar_marcacao():
    atraso = random.randint(0, 5) * 60

    if atraso == 0:
        atraso = 60

    print(f"Aguardando {atraso // 60} minutos para a execução.")

    time.sleep(atraso)  # Aguardar até o intervalo aleatório dentro da janela
    marcar_ponto()


# Agendar as marcações para os intervalos desejados
def main():
    # Iniciar o Chrome com depuração remota antes de começar as marcações
    iniciar_chrome_com_debug()

    # Marcação 1: Entrada
    schedule.every().day.at("08:58").do(lambda: agendar_marcacao())

    # Marcação 2: Saida almoco
    schedule.every().day.at("11:58").do(lambda: agendar_marcacao())

    # Marcação 3: Retorno almoco
    schedule.every().day.at("12:58").do(lambda: agendar_marcacao())

    # Marcação 4: Saida
    schedule.every().day.at("17:58").do(lambda: agendar_marcacao())

    # Manter o script rodando
    while True:
        schedule.run_pending()
        time.sleep(1)

# Executar o agendamento
if __name__ == "__main__":
    main()
