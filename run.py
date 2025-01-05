from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.text import Text
from rich import print as rprint
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama
init()

# Create Rich console
console = Console()

class WebDriverManager:
    """Manages WebDriver initialization and cleanup"""
    @staticmethod
    def initialize_driver() -> webdriver.Chrome:
        console.print("[yellow]Installing Chrome Driver[/yellow]")
        chromedriver_autoinstaller.install()
        console.print("[green]Chrome Driver Installation Complete ✓[/green]")
        return webdriver.Chrome()

class BasePage:
    """Base class for all pages with common web interactions"""
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.console = Console()

    def find_element(self, by: By, value: str):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by: By, value: str):
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

class AgeGatePage(BasePage):
    """Handles age verification page"""
    def handle_age_verification(self, birth_year: str = "2001"):
        console.print("[yellow]Handling Age Verification...[/yellow]")
        age_input = self.find_element(By.CLASS_NAME, "age-gate__input")
        age_input.send_keys(birth_year)

        check_mark = self.find_element(By.CLASS_NAME, "checkable__mask")
        check_mark.click()

        age_continue = self.find_element(By.CLASS_NAME, "age-gate__enter")
        age_continue.click()
        console.print("[green]Age verification completed ✓[/green]")

class LoginPage(BasePage):
    """Handles login functionality"""
    def login(self, email: str, password: str):
        console.print("[blue]Starting login process...[/blue]")
        self.driver.get("https://clubesagres.cervejasagres.pt/pt/login/")
        
        age_gate = AgeGatePage(self.driver)
        age_gate.handle_age_verification()
        
        console.print("[yellow]Waiting for page load...[/yellow]")
        time.sleep(5)
        
        console.print("[yellow]Entering credentials...[/yellow]")
        email_input = self.find_element(By.ID, "email")
        email_input.send_keys(email)

        password_input = self.find_element(By.ID, "password")
        password_input.send_keys(password)

        login_btn = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/section/div/div[2]/form/div[2]/button'))
        )
        login_btn.click()
        console.print("[green]Login successful ✓[/green]")

class Product:
    """Represents a product in the Sagres store"""
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link

class ProductCatalog(BasePage):
    """Handles product listing and searching"""
    def fetch_all_products(self) -> List[Product]:
        products = []
        current_page = 0
        
        while True:
            current_page += 1
            console.print(f"[cyan]Scanning page {current_page}...[/cyan]")
            
            self.driver.get(f"https://clubesagres.cervejasagres.pt/pt/montra-de-premios-sagres/?page={current_page}")
            self.scroll_to_bottom()

            try:
                prize_cards = self.find_elements(By.CLASS_NAME, 'prize-list__card')
                if not prize_cards:
                    break

                with Progress() as progress:
                    scan_task = progress.add_task(f"[cyan]Processing items on page {current_page}...", total=len(prize_cards))
                    
                    for prize in prize_cards:
                        try:
                            prize_link = prize.get_attribute('href')
                            prize_name = prize.find_element(By.CLASS_NAME, "prize-list__heading").text
                            products.append(Product(prize_name, prize_link))
                        except Exception as e:
                            console.print(f"[red]Error fetching prize details: {e}[/red]")
                        finally:
                            progress.update(scan_task, advance=1)

            except Exception as e:
                console.print(f"[red]Error fetching prize cards: {e}[/red]")
                break

        console.print(Panel(f"[green]Total Products Found: {len(products)}[/green]"))
        return products

class ProductRedeemer(BasePage):
    """Handles product redemption process"""
    def redeem_product(self, product: Product):
        console.print("[green]Attempting to redeem product...[/green]")
        self.driver.get(product.link)
        time.sleep(2)
        self.scroll_to_bottom()

        try:
            missing_point = self.find_element(By.TAG_NAME, 'h2')
            if missing_point:
                console.print(f"[yellow]Points Status: {missing_point.text}[/yellow]")
                return False
        except Exception:
            pass

        check_box = self.find_element(By.CLASS_NAME, "checkable__mask")
        check_box.click()
        submit_btn = self.find_element(By.CLASS_NAME, "prize-detail__submit")
        submit_btn.click()
        time.sleep(10)
        
        console.print("[green]Product redemption successful! ✓[/green]")
        return True

class SagresBot:
    """Main bot class that orchestrates all operations"""
    def __init__(self):
        self.driver = WebDriverManager.initialize_driver()
        self.login_page = LoginPage(self.driver)
        self.product_catalog = ProductCatalog(self.driver)
        self.product_redeemer = ProductRedeemer(self.driver)

    def login(self, email: str, password: str):
        self.login_page.login(email, password)

    def find_and_redeem_product(self, product_name: str, retry_interval: int = 15, max_retries: Optional[int] = None):
        attempts = 0
        
        while True:
            if max_retries is not None and attempts >= max_retries:
                console.print("[red]Maximum retries reached. Product not found.[/red]")
                return False
                
            attempts += 1
            console.print(Panel(f"[blue]Attempt {attempts} to find product: {product_name}[/blue]"))
            
            products = self.product_catalog.fetch_all_products()
            
            for product in products:
                if product.name.lower() == product_name.lower():
                    console.print(f"[green]Found product: {product_name} after {attempts} attempts! ✓[/green]")
                    return self.product_redeemer.redeem_product(product)
            
            console.print(f"[yellow]Waiting {retry_interval} seconds before next attempt...[/yellow]")
            time.sleep(retry_interval)

    def close(self):
        self.driver.quit()

def main():
    console.print(Panel.fit("[cyan]Welcome to Sagres Bot[/cyan]", border_style="blue"))
    
    get_email = console.input("[yellow]Enter Email: [/yellow]")
    get_password = console.input("[yellow]Enter Password: [/yellow]")
    enter_product = console.input("[yellow]Enter Product Name: [/yellow]")
    product_name_capitalize = enter_product.upper()
    
    console.print(Panel(f"[cyan]Searching for: {product_name_capitalize}[/cyan]"))
    
    bot = SagresBot()
    try:
        bot.login(get_email, get_password)
        time.sleep(5)
        console.print("[bold blue]Starting product search...[/bold blue]")
        bot.find_and_redeem_product(product_name_capitalize, retry_interval=20, max_retries=None)
        console.input("[yellow]Press Enter to Exit...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error occurred: {e}[/red]")
    finally:
        bot.close()

if __name__ == "__main__":
    main()