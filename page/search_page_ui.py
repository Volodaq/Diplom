from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class SearchPage:
    def __init__(self, driver):
        """Инициализация класса SearchPage с драйвером и временем ожидания.

        Args:
            driver (WebDriver): Драйвер Selenium для управления браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открытие URL")
    def open(self, url):
        """Открыть указанную URL-адрес в браузере.

        Args:
            url (str): URL-адрес для открытия.
        """
        self.driver.get(url)

    @allure.step("Ввод поискового запроса '{query}'")
    def enter_search_query(self, query):
        """Вводить текстовое сообщение в поле поиска.

        Args:
            query (str): Запрос для поиска.
        """
        search_input = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".header-search__input")))
        search_input.send_keys(query)

    @allure.step("Нажатие кнопки поиска")
    def click_search_button(self):
        """Нажать на кнопку поиска."""
        search_button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".header-search__button")))
        search_button.click()

    @allure.step("Получение названий продуктов")
    def get_product_titles(self):
        """Получить названия всех продуктов на странице результатов поиска.

        Returns:
            list: Список названий продуктов.
        """
        self.wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, ".product-title__head")))
        product_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                     ".product-title__head")
        return [product.text.strip() for product in product_elements]

    @allure.step("Получение названий авторов")
    def get_author_titles(self):
        """Получить имена всех авторов на странице результатов поиска.

        Returns:
            list: Список имен авторов.
        """
        self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".product-title__author")))
        author_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                    ".product-title__author")
        return [author.text for author in author_elements]

    @allure.step("Проверка сообщения об отсутствии результатов")
    def check_no_results_message(self):
        """Проверить и вернуть сообщение об отсутствии результатов поиска.

        Returns:
            str: Сообщение об отсутствии результатов.
        """
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".catalog-empty-result__description")))
        no_results_message = self.driver.find_element(
            By.CSS_SELECTOR, ".catalog-empty-result__description")
        return no_results_message.text