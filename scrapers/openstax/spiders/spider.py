import os
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import argparse
import logging
import hashlib


class WikiSpider(CrawlSpider):
    name = "openstax"
    allowed_domains = ["openstax.org"]

    start_urls = [
        "https://openstax.org/books/business-ethics/pages/preface",
        "https://openstax.org/books/business-law-i-essentials/pages/preface",
        "https://openstax.org/books/entrepreneurship/pages/preface",
        "https://openstax.org/books/introduction-business/pages/preface",
        "https://openstax.org/books/introduction-intellectual-property/pages/preface",
        "https://openstax.org/books/introductory-business-statistics/pages/preface",
        "https://openstax.org/books/mikroekonomia-podstawy/pages/preface",
        "https://openstax.org/books/organizational-behavior/pages/preface",
        "https://openstax.org/books/principles-economics-3e/pages/preface",
        "https://openstax.org/books/principles-finance/pages/preface",
        "https://openstax.org/books/principles-financial-accounting/pages/preface",
        "https://openstax.org/books/principles-macroeconomics-3e/pages/preface",
        "https://openstax.org/books/principles-management/pages/preface",
        "https://openstax.org/books/principles-managerial-accounting/pages/preface",
        "https://openstax.org/books/principles-marketing/pages/preface",
        "https://openstax.org/books/principles-microeconomics-3e/pages/preface",
        "https://openstax.org/books/college-success/pages/preface",
        "https://openstax.org/books/college-success-concise/pages/preface",
        "https://openstax.org/books/preparing-for-college-success/pages/preface",
        "https://openstax.org/books/business-law-i-essentials/pages/preface",
        "https://openstax.org/books/introduction-philosophy/pages/preface",
        "https://openstax.org/books/us-history/pages/preface",
        "https://openstax.org/books/world-history-volume-1/pages/preface",
        "https://openstax.org/books/world-history-volume-2/pages/preface",
        "https://openstax.org/books/writing-guide/pages/preface",
        "https://openstax.org/books/biology-ap-courses/pages/preface",
        "https://openstax.org/books/college-physics-ap-courses-2e/pages/preface",
        "https://openstax.org/books/elementary-algebra-2e/pages/preface",
        "https://openstax.org/books/intermediate-algebra-2e/pages/preface",
        "https://openstax.org/books/physics/pages/preface",
        "https://openstax.org/books/prealgebra-2e/pages/preface",
        "https://openstax.org/books/precalculus-2e/pages/preface",
        "https://openstax.org/books/principles-economics-3e/pages/preface",
        "https://openstax.org/books/principles-macroeconomics-3e/pages/preface",
        "https://openstax.org/books/principles-microeconomics-3e/pages/preface",
        "https://openstax.org/books/statistics/pages/preface",
        "https://openstax.org/books/algebra-and-trigonometry-2e/pages/preface",
        "https://openstax.org/books/calculus-volume-1/pages/preface",
        "https://openstax.org/books/calculus-volume-2/pages/preface",
        "https://openstax.org/books/calculus-volume-3/pages/preface",
        "https://openstax.org/books/college-algebra-2e/pages/preface",
        "https://openstax.org/books/college-algebra-corequisite-support-2e/pages/preface",
        "https://openstax.org/books/contemporary-mathematics/pages/preface",
        "https://openstax.org/books/elementary-algebra-2e/pages/preface",
        "https://openstax.org/books/intermediate-algebra-2e/pages/preface",
        "https://openstax.org/books/introductory-business-statistics/pages/preface",
        "https://openstax.org/books/introductory-statistics/pages/preface",
        "https://openstax.org/books/prealgebra-2e/pages/preface",
        "https://openstax.org/books/precalculus-2e/pages/preface",
        "https://openstax.org/books/statistics/pages/preface",
        "https://openstax.org/books/anatomy-and-physiology-2e/pages/preface",
        "https://openstax.org/books/astronomy-2e/pages/preface",
        "https://openstax.org/books/biology-2e/pages/preface",
        "https://openstax.org/books/biology-ap-courses/pages/preface",
        "https://openstax.org/books/chemistry-2e/pages/preface",
        "https://openstax.org/books/chemistry-atoms-first-2e/pages/preface",
        "https://openstax.org/books/college-physics-2e/pages/preface",
        "https://openstax.org/books/college-physics-ap-courses-2e/pages/preface",
        "https://openstax.org/books/concepts-biology/pages/preface",
        "https://openstax.org/books/microbiology/pages/preface",
        "https://openstax.org/books/organic-chemistry/pages/preface",
        "https://openstax.org/books/physics/pages/preface",
        "https://openstax.org/books/university-physics-volume-1/pages/preface",
        "https://openstax.org/books/university-physics-volume-2/pages/preface",
        "https://openstax.org/books/university-physics-volume-3/pages/preface",
        "https://openstax.org/books/american-government-3e/pages/preface",
        "https://openstax.org/books/introduction-anthropology/pages/preface",
        "https://openstax.org/books/introduction-political-science/pages/preface",
        "https://openstax.org/books/introduction-sociology-3e/pages/preface",
        "https://openstax.org/books/mikroekonomia-podstawy/pages/preface",
        "https://openstax.org/books/principles-economics-3e/pages/preface",
        "https://openstax.org/books/principles-macroeconomics-3e/pages/preface",
        "https://openstax.org/books/principles-microeconomics-3e/pages/preface",
        "https://openstax.org/books/psychologia-polska/pages/preface",
        "https://openstax.org/books/psychology-2e/pages/preface",
    ]

    rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

    def parse_item(self, response):
        # log downloaded files
        if not os.path.exists("manifest.log"):
            with open("manifest.log", "w") as fp:
                fp.write("hash\turl\n")
        data_root = "data/"
        if not os.path.exists(data_root):
            os.mkdir(data_root)

        hash_value = hashlib.sha256(bytes(response.url, "utf-8")).hexdigest()
        with open("manifest.log", "a") as fp:
            fp.write(f"{hash_value}\t{response.url}\n")

        filename = f"{data_root}/{hash_value}.html"
        with open(filename, "wb") as fp:
            fp.write(response.body)
