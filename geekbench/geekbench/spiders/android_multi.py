import scrapy

class AndroidMultiSpider(scrapy.Spider):
    name = "android_multi"
    allowed_domains = ["browser.geekbench.com"]
    start_urls = [
        "https://browser.geekbench.com/android-benchmarks/"
    ]

    def parse(self, response):
        # CSS SELECTOR STRATEGY:
        # 1. Find the div with id="multi-core" (specific to the tab you want)
        # 2. Select the 'table' inside it
        table = response.css("div#multi-core table")

        # Select all rows (tr) inside that table
        rows = table.css("tr")

        rank = 1
        for row in rows:
            # Device name: 
            # Looks for <td class="name"> -> <a> -> text
            device = row.css("td.name a::text").get()

            # CPU model:
            # Looks for <td class="name"> -> <div class="description"> -> text
            cpu = row.css("td.name div.description::text").get()

            # Multi-core score:
            # Looks for <td class="score"> -> text
            score = row.css("td.score::text").get()

            # Skip header/empty rows
            if not device or not score:
                continue

            yield {
                "Rank": rank,
                "Device": device.strip(),
                "CPU": cpu.strip() if cpu else None,
                "Multi-Core Score": score.strip(),
            }

            rank += 1

        # Follow pagination
        # specific attribute selection uses ::attr(attributename)
        next_page = response.css("a[rel='next']::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)