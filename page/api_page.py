import requests
#import allure


class ApiPage:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    @allure.step("Поиск продукта по фразе: {phrase}")
    def search_product(self, phrase, customer_city_id=54):
        params = {
            "customerCityId": customer_city_id,
            "phrase": phrase
        }
        response = requests.get(self.base_url, headers=self._get_headers(),
                                params=params)
        allure.attach(response.text, "Ответ API")
        return response

    @allure.step("Извлечение названий книг из ответа")
    def extract_book_titles(self, response_json):
        titles = [book['attributes']['title'] for book in response_json.get(
            'included', []) if book['type'] == 'product']
        allure.attach(str(titles), "Названия книг")
        return titles

    @allure.step("Извлечение авторов книг из ответа")
    def extract_book_authors(self, response_json):
        book_authors = []
        for book in response_json.get('included', []):
            if book['type'] == 'product':
                authors = book['attributes'].get('authors', [])
                for author in authors:
                    full_name = f"{author.get('firstName', '')} {author.get('lastName', '')}".strip()
                    book_authors.append(full_name)
        allure.attach(str(book_authors), "Авторы книг")
        return book_authors