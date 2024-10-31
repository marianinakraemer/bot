import logging
import pyautogui
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import openpyxl

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para fazer login no sistema
def perform_login(driver, usuario, senha):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="trid-auth"]/form/label[1]/span[2]/input'))
        )
        usuario_field = driver.find_element(By.XPATH, '//*[@id="trid-auth"]/form/label[1]/span[2]/input')
        usuario_field.send_keys(usuario)
        password_field = driver.find_element(By.XPATH, '//*[@id="trid-auth"]/form/label[2]/span[2]/input')
        password_field.send_keys(senha)
        login_button = driver.find_element(By.XPATH, '//*[@id="enterButton"]')
        login_button.click()
        time.sleep(5)
    except Exception as e:
        driver.save_screenshot('login_error.png')
        logger.error(f"Erro ao fazer login: {e}")
        raise

# Função para fazer upload de um arquivo
def upload_file(driver, caminho_arquivo):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="uploadButton"]'))
        )
        upload_button = driver.find_element(By.XPATH, '//*[@id="uploadButton"]')
        upload_button.click()
        time.sleep(2)
        pyautogui.write(caminho_arquivo)
        pyautogui.press('enter')
        logger.info(f"Arquivo {caminho_arquivo} enviado para upload.")
    except Exception as e:
        logger.error(f"Erro ao fazer upload do arquivo: {e}")
        raise

# Função para processar o upload dos arquivos filtrados
def upload_files(arquivos_filtrados):
    # Carregar credenciais do Excel
    workbook = openpyxl.load_workbook('dados.xlsx')
    sheet = workbook.active
    usuario = sheet['A2'].value
    senha = sheet['B2'].value

    logger.info(f"Usuário: {usuario}")
    logger.info(f"Senha: {senha}")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.dominioweb.com.br')

    perform_login(driver, usuario, senha)

    for caminho_arquivo in arquivos_filtrados:
        upload_file(driver, caminho_arquivo)

    time.sleep(30)  # Manter o navegador aberto para visualização
    driver.quit()
