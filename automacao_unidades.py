from flask import Flask, render_template_string, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
import threading
import time

app = Flask(__name__)

SITESGAMEBOX = {
    "Riomar": "https://gamebox-riomar.sistemaxcard.com.br/GameCardWEB",
    "Mangabeira": "https://gamebox-mangabeira.sistemaxcard.com.br/GameCardWEB",
    "Manaira": "https://gamebox-manaira.sistemaxcard.com.br/GameCardWEB",
    "Tacaruna": "https://gamebox-tacaruna.sistemaxcard.com.br/GameCardWEB",
    "Recife": "https://gamebox-recife.sistemaxcard.com.br/GameCardWEB",
    
}

SITESGAMESTATION = {
    "AzeGames Butanta": "https://azegames-butanta.sistemaxcard.com.br/GameCardWEB/",
    "Parks Campolimpo": "https://parks-campolimpo.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Franca": "https://azegames-franca.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Grande Rio": "https://azegames-granderio.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Granja": "https://azegames-granja.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Jacarei": "https://azegames-jacarei.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Largo 13": "https://azegames-largo13.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Metropolitano": "https://azegames-metropolitano.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Mogi das Cruzes": "https://azegames-mogidascruzes.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames North Shopping": "https://azegames-northshopping.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Nova Iguacu": "https://azegames-novaiguacu.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Osasco": "https://azegames-osasco.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Parangaba": "https://azegames-parangaba.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Parque das Bandeiras": "https://azegames-parquedasbandeiras.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Plaza Sul": "https://azegames-plazasul.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Porto Alegre Total": "https://azegames-portoalegre-total.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Santana": "https://azegames-santana.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Sorocaba": "https://azegames-sorocaba.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Tambore": "https://azegames-tambore.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames West Plaza": "https://azegames-westplaza.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Bangu": "https://gamestation-bangu.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Bela Vista": "https://gamestation-belavista.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Boa Vista": "https://gamestation-shoppingboavista.sistemaxcard.com.br/GameCardWEB/",
    "Bolix ABC Plaza": "https://bolix-abcplaza.sistemaxcard.com.br/GameCardWEB/",
    "Bolix Internacional": "https://bolix-internacional.sistemaxcard.com.br/GameCardWEB/",
    "Bolix Interlagos": "https://bolix-interlagos.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Raposo": "https://azegames-raposo.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Camara Shopping": "https://gamestation-camarashopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Caruaru Shopping": "https://gamestation-caruarushopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Costa Dourada": "https://gamestation-costadourada.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Guararapes": "https://gamestation-guararapes.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Iguatemi Fortaleza": "https://gamestation-iguatemifortaleza.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Jardins Aracaju": "https://gamestation-jardinsaracaju.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Loja Teste": "https://gamestation-lojateste.sistemaxcard.com.br/GameCardWEB/",
    "AzeGames Maceio": "https://azegames-maceio.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Manaira Shopping": "https://gamestation-manairashopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Mangabeiras": "https://gamestation-mangabeiras.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Midway": "https://gamestation-midway.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Paralela": "https://gamestation-paralela.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Partage Campina": "https://gamestation-shoppingpartagecampina.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Partage Norte Shop Natal": "https://gamestation-partagenorteshopnatal.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Patio Maceio": "https://gamestation-patiomaceio.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Patio Paulista": "https://gamestation-patiopaulista.sistemaxcard.com.br/GameCardWEB/",
    "Parks Olinda": "https://parks-olinda.sistemaxcard.com.br/GameCardWEB/",
    "Parks Paulista North Way Shopping": "https://parks-paulista-northwayshopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Plaza Casa Forte": "https://gamestation-plazacasaforte.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Riomar Aracaju": "https://gamestation-riomararacaju.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Riomar Fortaleza": "https://gamestation-riomarfortaleza.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Riomar Recife": "https://gamestation-riomarrecife.sistemaxcard.com.br/GameCardWEB/",
    "GameStation River Shopping": "https://gamestation-rivershopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Salvador Norte Shopping": "https://gamestation-salvadornorteshopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Boa Vista SP": "https://gamestation-boavista-sp.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Difusora": "https://gamestation-shoppingdifusora.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Natal": "https://gamestation-shoppingnatal.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Recife": "https://gamestation-shoppingrecife.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Salvador Shopping": "https://gamestation-salvadorshopping.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Shopping Taboao": "https://gamestation-shoppingtaboao.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Tacaruna": "https://gamestation-tacaruna.sistemaxcard.com.br/GameCardWEB/",
    "GameStation Tucuruvi": "https://gamestation-tucuruvi.sistemaxcard.com.br/GameCardWEB/",
}

# Combinar todos os sites em um único dicionário para facilitar a iteração
ALL_SITES = {**SITESGAMEBOX, **SITESGAMESTATION}

# Template HTML atualizado para receber usuário, senha e seleção de lojas
HTML_TEMPLATE = """
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <title>Automação de Usuários</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background: #f4f6f9;
      }
      .form-section {
        margin-bottom: 1.5rem;
      }
      .checkbox-group h6 {
        margin-top: 1rem;
        font-weight: 600;
        color: #343a40;
      }
      pre {
        white-space: pre-wrap;
        word-wrap: break-word;
      }
    </style>
  </head>
  <body>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-md-9">
          <div class="card shadow-sm">
            <div class="card-body">
              <h1 class="card-title mb-4 text-primary">Gerenciamento de Usuários SPIX</h1>
              <form method="post" action="/">
                <div class="form-section">
                  <label for="username" class="form-label fw-semibold">Usuário Spix</label>
                  <input type="text" class="form-control" id="username" name="username" placeholder="Digite seu usuário" required>
                </div>
                <div class="form-section">
                  <label for="password" class="form-label fw-semibold">Senha Spix</label>
                  <input type="password" class="form-control" id="password" name="password" placeholder="Digite sua senha" required>
                </div>
                <div class="form-section">
                  <label for="nome_usuario" class="form-label fw-semibold">Nome do Usuário a Desabilitar</label>
                  <input type="text" class="form-control" id="nome_usuario" name="nome_usuario" placeholder="Nome do usuário a gerenciar" required>
                </div>
                <div class="form-section">
                  <label class="form-label fw-semibold">Ação</label>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="action" id="action_disable" value="disable" checked>
                    <label class="form-check-label" for="action_disable">
                      Desabilitar Usuário
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="action" id="action_enable" value="enable">
                    <label class="form-check-label" for="action_enable">
                      Habilitar Usuário
                    </label>
                  </div>
                </div>
                <div class="form-section checkbox-group">
                  <label class="form-label fw-semibold">Selecione a(s) Loja(s)</label>
                  <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" value="all" id="loja_all" name="lojas" checked>
                    <label class="form-check-label" for="loja_all">
                      Todas as Lojas
                    </label>
                  </div>
                  <hr>
                  <h6>GameBox Lojas:</h6>
                  {% for loja_nome, loja_url in sites_gamebox.items() %}
                  <div class="form-check">
                    <input class="form-check-input loja-checkbox" type="checkbox" value="{{ loja_nome }}" id="loja_{{ loja_nome | replace(' ', '_') }}" name="lojas">
                    <label class="form-check-label" for="loja_{{ loja_nome | replace(' ', '_') }}">
                      {{ loja_nome }}
                    </label>
                  </div>
                  {% endfor %}
                  <hr>
                  <h6>GameStation Lojas:</h6>
                  {% for loja_nome, loja_url in sites_gamestation.items() %}
                  <div class="form-check">
                    <input class="form-check-input loja-checkbox" type="checkbox" value="{{ loja_nome }}" id="loja_{{ loja_nome | replace(' ', '_') }}" name="lojas">
                    <label class="form-check-label" for="loja_{{ loja_nome | replace(' ', '_') }}">
                      {{ loja_nome }}
                    </label>
                  </div>
                  {% endfor %}
                </div>
                <div class="d-grid mt-4">
                  <button type="submit" class="btn btn-primary btn-lg">Executar Ação</button>
                </div>
              </form>
              {% if output %}
              <div class="mt-5">
                <h3 class="text-success mb-3">Resultado:</h3>
                <pre class="p-3 bg-light border rounded shadow-sm">{{ output }}</pre>
              </div>
              {% endif %}
            </div>
          </div>
        </div>
      </div>
    </div>

    <script>
      // Script para controlar seleção "Todas" e desmarcar outras se "Todas" estiver marcada
      const lojaAll = document.getElementById('loja_all');
      const checkboxes = document.querySelectorAll('.loja-checkbox');

      lojaAll.addEventListener('change', function() {
        if(this.checked) {
          checkboxes.forEach(cb => cb.checked = false);
        }
      });

      checkboxes.forEach(cb => {
        cb.addEventListener('change', function() {
          if(this.checked) {
            lojaAll.checked = false;
          }
          // Se nenhum checkbox individual estiver marcado, marcar "Todas"
          if (![...checkboxes].some(cb => cb.checked)) {
            lojaAll.checked = true;
          }
        });
      });
    </script>
  </body>
</html>

"""

def aceitar_cookies(driver, wait):
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "close-warning"))
        )
        cookie_button.click()
        print("Botão 'Permitir Todos os Cookies' clicado.")
        time.sleep(1)
    except:
        print("Botão de cookies não apareceu ou já foi aceito.")

def login(driver, wait, site_url, username, password):
    driver.get(site_url + "/usuarios")
    aceitar_cookies(driver, wait)
    wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "j_password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "confirmar"))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn-index.admin")))
    print(f"Login realizado com sucesso em {site_url}")

def acessar_administracao(driver, wait):
    try:
        admin_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-index.admin")))
        driver.execute_script("arguments[0].click();", admin_link)
        print("Clique no link Administração realizado via JavaScript.")
        wait.until(EC.url_contains("/loja/index.jsp"))
        print("Página Administração carregada.")
    except Exception as e:
        print(f"Erro ao acessar Administração: {e}")

def acessar_usuarios(driver, wait):
    try:
        container = wait.until(EC.presence_of_element_located((By.ID, "container")))
        usuarios_link = container.find_element(By.XPATH, ".//a[contains(text(), 'Usuários')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", usuarios_link)
        time.sleep(0.5)
        usuarios_link.click()
        print("Link 'Usuários' clicado.")
        wait.until(EC.url_contains("/usuarios"))
        print("Página Usuários carregada.")
    except Exception as e:
        print(f"Erro ao acessar Usuários: {e}")

def desabilitar_usuario(driver, wait, nome_usuario):
    try:
        time.sleep(2)
        usuario_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tr[.//text()[contains(., '{nome_usuario}')]]")
            )
        )
        botao_desabilitar = usuario_element.find_element(By.XPATH, ".//input[@id='desabilitar' and @type='submit']")
        botao_desabilitar.click()
        print(f"Botão 'Desabilitar' clicado para o usuário {nome_usuario}.")

        try:
            alert = wait.until(EC.alert_is_present())
            alert.accept()
            print("Popup de confirmação aceito.")
        except NoAlertPresentException:
            print("Nenhum popup de confirmação apareceu.")

        time.sleep(2)
        return True
    except Exception as e:
        print(f"Erro ao desabilitar o usuário {nome_usuario}: {e}")
        return False

def habilitar_usuario(driver, wait, nome_usuario):
    try:
        time.sleep(2)
        # Clicar em "Exibir Desabilitados"
        exibir_desabilitados_button = wait.until(
            EC.element_to_be_clickable((By.ID, "exibirDesabilitados"))
        )
        exibir_desabilitados_button.click()
        print("Botão 'Exibir Desabilitados' clicado.")
        time.sleep(2) # Esperar a página carregar os usuários desabilitados

        # Localizar o usuário e o botão "Habilitar"
        usuario_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tr[.//text()[contains(., '{nome_usuario}')]]")
            )
        )
        botao_habilitar = usuario_element.find_element(By.XPATH, ".//input[@id='habilitar' and @type='submit']")
        botao_habilitar.click()
        print(f"Botão 'Habilitar' clicado para o usuário {nome_usuario}.")

        try:
            alert = wait.until(EC.alert_is_present())
            alert.accept()
            print("Popup de confirmação aceito.")
        except NoAlertPresentException:
            print("Nenhum popup de confirmação apareceu.")

        time.sleep(2)
        return True
    except Exception as e:
        print(f"Erro ao habilitar o usuário {nome_usuario}: {e}")
        return False

def executar_automacao(username, password, nome_usuario, lojas_selecionadas, action):
    output = []
    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 20)

        sites_para_processar = {}
        if "all" in lojas_selecionadas:
            sites_para_processar = ALL_SITES
        else:
            for loja_nome in lojas_selecionadas:
                if loja_nome in ALL_SITES:
                    sites_para_processar[loja_nome] = ALL_SITES[loja_nome]

        if not sites_para_processar:
            output.append("Nenhuma loja selecionada para processar.")
            return "\n".join(output)

        for loja_nome, site_url in sites_para_processar.items():
            output.append(f"Processando site: {site_url} ({loja_nome})")
            try:
                login(driver, wait, site_url, username, password)
                time.sleep(2)
                acessar_administracao(driver, wait)
                time.sleep(2)
                acessar_usuarios(driver, wait)
                time.sleep(2)

                if action == "disable":
                    if desabilitar_usuario(driver, wait, nome_usuario):
                        output.append(f"Usuário '{nome_usuario}' desabilitado com sucesso em {loja_nome}.")
                    else:
                        output.append(f"Falha ao desabilitar usuário '{nome_usuario}' em {loja_nome}.")
                elif action == "enable":
                    if habilitar_usuario(driver, wait, nome_usuario):
                        output.append(f"Usuário '{nome_usuario}' habilitado com sucesso em {loja_nome}.")
                    else:
                        output.append(f"Falha ao habilitar usuário '{nome_usuario}' em {loja_nome}.")
                
                output.append(f"Processo concluído para {site_url}\n{'-'*40}")
            except Exception as e:
                output.append(f"Erro no site {site_url}: {e}")
    except Exception as e:
        output.append(f"Erro geral: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass
    return "\n".join(output)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        nome_usuario = request.form.get("nome_usuario", "").strip()
        lojas_selecionadas = request.form.getlist("lojas")
        action = request.form.get("action") # 'disable' or 'enable'

        if username and password and nome_usuario and lojas_selecionadas and action:
            output = executar_automacao(username, password, nome_usuario, lojas_selecionadas, action)
    return render_template_string(HTML_TEMPLATE, output=output, sites_gamebox=SITESGAMEBOX, sites_gamestation=SITESGAMESTATION)

if __name__ == "__main__":
    app.run(debug=True)
