import scrapy
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response: Response, **kwargs):
        for book_url in response.css('article.product_pod h3 a::attr(href)').getall():
            yield response.follow(book_url, self.parse_book)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response: Response):
        yield {
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'amount_in_stock': response.css('p.instock.availability::text').re_first('\d+'),
            'rating': response.css('p.star-rating::attr(class)').re_first('star-rating (\w+)'),
            'category': response.css('ul.breadcrumb li a::text')[-2].get(),
            'description': response.css('meta[name="description"]::attr(content)').get().strip(),
            'upc': response.css('table.table-striped tr:nth-child(1) td::text').get(),
        }
