from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.init_driver()

    def init_driver(self):
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            print("ChromeDriver iniciado com sucesso.")
        except Exception as e:
            print(f"Erro ao iniciar o WebDriver: {e}")
            exit()

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        print("Página de login carregada.")

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
            print("Campo de nome de usuário encontrado.")
            
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'nav')))
            print("Login bem-sucedido")
        except TimeoutException:
            print("Erro: Login falhou ou a página não carregou corretamente.")
            self.driver.quit()
            exit()

    def get_followers(self):
        # Clicar no ícone do perfil para acessar o próprio perfil
        try:
            profile_link = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Perfil']"))
            )
            profile_link.click()
            print("Perfil acessado.")
        except TimeoutException:
            print("Erro: Ícone do perfil não encontrado.")
            self.quit()
            return []

        # Aguardar o carregamento da página do perfil
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'seguidores'))
        )
        
        try:
            followers_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'seguidores')
            followers_link.click()
            print("Acessando seguidores.")
        except TimeoutException:
            print("Erro: Link de seguidores não encontrado.")
            self.quit()
            return []

        # Esperar o modal de seguidores ser carregado
        try:
            followers_popup = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
            )
            print("Modal de seguidores carregado.")
        except TimeoutException:
            print("Erro: Popup de seguidores não carregado.")
            self.quit()
            return []

        last_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_popup)
        followers_names = []

        while True:
            # Scroll para baixo
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
            time.sleep(2)  # Tempo para a página carregar novos seguidores

            try:
                # Atualizar a referência ao modal de seguidores
                followers_popup = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
                )
                print("Modal de seguidores atualizado.")

                new_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_popup)

                # Buscar seguidores usando o XPath fornecido
                followers = followers_popup.find_elements(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
                if not followers:
                    print("Nenhum seguidor encontrado na página.")
                for follower in followers:
                    try:
                        user_name = follower.text

                        if user_name:
                            if user_name not in followers_names:
                                followers_names.append(user_name)
                    except NoSuchElementException:
                        print("Erro: Elemento de seguidor não encontrado.")
                    except Exception as e:
                        print(f"Erro ao processar um seguidor: {e}")

                if new_height == last_height:
                    print("Rolagem concluída. Todos os seguidores foram carregados.")
                    break
                last_height = new_height
            except TimeoutException:
                print("Erro: Popup de seguidores não carregado após scroll.")
                break

        # Retornar os nomes dos seguidores
        print(f"Total de seguidores encontrados: {len(followers_names)}")
        return followers_names

    def quit(self):
        if self.driver:
            self.driver.quit()
            print("ChromeDriver encerrado.")

def save_followers_to_json(data, filename='data/followers.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
