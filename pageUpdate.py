from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

class BrowserError(Exception):
    pass

class ProductParser:
    def __init__(self):
        self.URL = ""

        print('Starting parser session...')

        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch()
        self.page = self.browser.new_page()
        self.keyword = 'Продукты отсутствуют'

        print('Parser session started!')

    # Checking if a product appears
    def check(self):
        try:
            print('Checking product info...')

            self.page.goto(self.URL)
            self.page.wait_for_selector('table.table-bordered.table-striped.top_30',timeout=60000)

        except Exception:
            raise BrowserError
        
        if self.page.get_by_text('Товары').count():

            if self.page.get_by_text(self.keyword).count():
                return False
            
            return True
        
    # Close browser session
    def close(self):
        self.browser.close()
        print('Parser session closed!')