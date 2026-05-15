# 🧪 Projet d’Automatisation de Tests du site SauceDemo avec Python Selenium

<p align="center">
  <img src="logo.jpg" width="500"/>
</p>

<p align="center">
  📸 Source : <a href="https://www.magnific.com/">Magnific</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Selenium-Automation-43B02A?logo=selenium&logoColor=white" />
  <img src="https://img.shields.io/badge/Allure-Reporting-FF6F00?logo=allure&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/status-WIP-orange" />
</p>

---

## 📌 Présentation du projet

Ce projet est un **framework d’automatisation de tests UI** développé en Python avec Selenium.

Il permet de tester l’application de démonstration :
👉 https://www.saucedemo.com/

L’objectif est de simuler un **framework de test professionnel maintenable et scalable**.

---

## 🚀 Stack technique

- Python 3.11+
- Selenium WebDriver
- Pytest
- Allure

---

## 🧱 Architecture du projet

```bash
saucedemo-test-automation
│
├── config/               # Configuration globale
│   └── settings.py
│
├── core/                 # Composants centraux du framework
│   ├── driver_factory.py # Initialisation du WebDriver
│   ├── logger.py         # Système de logs
│   └── utils.py          # Fonctions utilitaires
│
├── pages/                # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── testdata/             # Données de test
│   ├── credentials.json
│   └── checkout.json
│
├── tests/                # Suites de tests
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── .env                  # Variables d’environnement (non versionné)
├── conftest.py           # Fixtures pytest globales et configuration des tests
├── pyproject.toml        # Dépendances du projet
├── uv.lock               # Lock des dépendances
└── README.md
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/komiadok/saucedemo-test-automation.git
cd saucedemo-test-automation
```

---

### 2. Installer uv (gestionnaire Python)

```bash
pip install uv
```

---

### 3. Installer scoop (Windows)

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

---

### 4. Installer Allure CLI (reporting)

```bash
scoop install allure
```

---


### 5. Installer les dépendances

Avec `uv` :

```bash
uv sync
```

Ou avec pip :

```bash
pip install -e .
```

---

## 🔐 Variables d’environnement

Contenu du fichier `.env` :

```dotenv
# Application
BASE_URL=https://www.saucedemo.com/

# Browser
BROWSER=chrome
HEADLESS=true

# Timeouts
DEFAULT_TIMEOUT=10
```

> Vous pouvez le modifier et l'adapter selon vos besoins.

---

## ▶️ Exécution des tests

### Lancer tous les tests

```bash
uv run pytest
```

---

### Lancer tous les tests, puis générer et visualiser les résultats Allure

```bash
# Lancer les tests avec rapport Allure
uv run pytest --alluredir=reports/allure-results

# Ouvrir le rapport
allure serve reports/allure-results
```

---

### Lancer un fichier spécifique

```bash
uv run pytest tests/test_login.py
```

---

### Lancer un test avec des tags

```bash
uv run pytest -m smoke
uv run pytest -m "login and smoke"
uv run pytest -m "not e2e"
```

---

### Mode verbeux 

```bash
uv run pytest -v
```

> Ce mode sert à avoir plus de détails dans le terminal pendant l'exécution des tests. Exemple : 

```text
test_login.py::test_valid_login PASSED
test_login.py::test_invalid_login PASSED
test_cart.py::test_add_item FAILED
```

---

## 🧪 Couverture des tests

### 🔐 Authentification
- Connexion avec un utilisateur valide
- Connexion avec un utilisateur bloqué
- Connexion avec un mot de passe incorrect
- Connexion avec des champs vides
- Validation des messages d’erreur

### 📦 Inventaire
- Affichage de la liste des produits
- Vérification des informations produit (nom, prix, description)
- Tri des produits (prix croissant/décroissant, nom)

### 🛒 Panier
- Ajout d’un ou plusieurs articles au panier
- Suppression d’un article du panier
- Vérification du nombre d’articles
- Vérification du total du panier

### 💳 Checkout
- Validation du formulaire de commande
- Vérification des messages d’erreur de validation
- Processus de commande complet
- Vérification du récapitulatif de commande

---

## 👤 Auteur

**komiadok**  
QA Automation Engineer & Data Analyst

GitHub : https://github.com/komiadok

---

## 📄 Licence

Ce projet est distribué sous la licence MIT.  

Vous pouvez l’utiliser, le modifier et le redistribuer librement, y compris dans un contexte commercial, à condition de conserver la mention de l’auteur original et la licence.