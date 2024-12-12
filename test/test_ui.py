import pytest
from selenium import webdriver
import allure
from page.search_page_ui import SearchPage


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()  # Укажите драйвер
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def search_page(browser):
    page = SearchPage(browser)
    page.open("https://www.chitai-gorod.ru/")
    return page


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск книги по заголовку")
@allure.description(
    "Тест проверяет возможность поиска книги по заголовку 'Садись, пять!'.")
def test_search_book_by_title(search_page):
    with allure.step("Введите запрос на поиск книги"):
        search_page.enter_search_query("Садись, пять!")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert any("Садись, пять!" in title for title in product_titles
               ), "Название книги не найдено в списке продуктов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора")
@allure.description(
    "Тест проверяет возможность поиска автора 'Лев Николаевич Толстой'.")
def test_search_author(search_page):
    with allure.step("Введите запрос на поиск автора"):
        search_page.enter_search_query("Лев Николаевич Толстой")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки авторов"):
        author_titles = search_page.get_author_titles()
    assert len(author_titles) > 0, "Нет результатов поиска для автора"
    assert any("Лев Толстой" in title for title in author_titles
               ), "Имя автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора по части фамилии")
@allure.description(
    "Тест проверяет поиск автора по части фамилии 'Достоевский'.")
def test_search_author_partial_surname(search_page):
    with allure.step("Введите запрос для поиска"):
        search_page.enter_search_query("Достоевский")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки авторов"):
        author_titles = search_page.get_author_titles()
    assert len(author_titles) > 0, "Нет результатов поиска для автора"
    assert any("Достоевский" in title for title in author_titles
               ), "Фамилия автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск автора на английском языке")
@allure.description("Тест проверяет возможность поиска автора 'Dostoevsky'.")
def test_search_author_in_english(search_page):
    with allure.step("Введите запрос для поиска"):
        search_page.enter_search_query("Dostoevsky")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для автора"
    assert any(
        "Dostoevsky" in title for title in product_titles
        ), "Фамилия автора не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск книги с дефисом")
@allure.description("Тест проверяет возможность поиска книги 'Монт-Ориоль'.")
def test_search_book_with_hyphen(search_page):
    with allure.step("Введите запрос для поиска книги"):
        search_page.enter_search_query("Монт-Ориоль")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Получите заголовки продуктов"):
        product_titles = search_page.get_product_titles()
    assert len(product_titles) > 0, "Нет результатов поиска для книги"
    assert any(
        "Монт-Ориоль" in title for title in product_titles
        ), "Книга не отображается на странице результатов"


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
@allure.title("Поиск с использованием только знаков препинания")
@allure.description("Тест проверяет обработку поиска, "
                    "состоящего только из знаков препинания.")
def test_search_punctuation_only(search_page):
    with allure.step("Введите запрос с знаками препинания"):
        search_page.enter_search_query(",,,….!!!")
    with allure.step("Нажмите кнопку поиска"):
        search_page.click_search_button()
    with allure.step("Проверьте сообщение об отсутствии результатов"):
        message_text = search_page.check_no_results_message()
    assert (
        "Похоже, у нас такого нет" in message_text
        ), "Сообщение об отсутствии результатов не отображается."