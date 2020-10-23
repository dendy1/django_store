from selenium import webdriver
from unittest import TestCase, main


class HomePageTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title)

    def test_register_page(self):
        # Visiting Web Store site
        self.browser.get('http://localhost:8000')

        # Searching for `Register` link in <body></body>
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Register', body.text)

        # Clicking on `Register` link
        register_link = self.browser.find_element_by_link_text('Register')
        register_link.click()

        # Checking for `Registration Page` in <body></body>
        register_body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Registration Page', register_body)

if __name__ == '__main__':
    main()