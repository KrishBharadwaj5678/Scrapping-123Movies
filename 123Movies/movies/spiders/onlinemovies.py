import scrapy
from pymongo import MongoClient
client = MongoClient("mongodb+srv://username:password@cluster0.h6ocrk9.mongodb.net/")

db = client["123Movies"]
movies = db.Movies

class OnlinemoviesSpider(scrapy.Spider):
    name = "onlinemovies"
    allowed_domains = ["ww16.0123movie.net"]
    start_urls = ["https://ww16.0123movie.net"]

    def start_requests(self):
        urls = [
            "https://ww16.0123movie.net/list/movies.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        cards=response.css("div.col")

        def addMovies(link,image,title):
            data = {
                "Title":title,
                "Link": link,
                "Image": image,
            }
            post_id = movies.insert_one(data)

        for card in cards:
            # Movie URL
            link=card.css("a::attr(href)").get()
            # Movie Image
            image=card.css("a picture source::attr(data-srcset)").get().split(" ")[0]
            # Movie Title
            title=card.css("div.card-body h2.card-title::text").get()
            addMovies(link,image,title)

    
