import scrapy


class AndroidMultiSpider(scrapy.Spider):
    name = "android_multi"
    allowed_domains = ["browser.geekbench.com"]
    start_urls = [
        "https://browser.geekbench.com/android-benchmarks/"
    ]

    def parse(self, response):

        # Select the exact table using your XPath
        table = response.xpath("/html/body/div/div/div[1]/div[2]/div/div[2]/div/table")

        # Rows inside table
        rows = table.xpath(".//tr")

        rank = 1
        for row in rows:

            # Device name
            device = row.xpath(".//td[@class='name']/a/text()").get()

            # CPU model (in <div class='description'>)
            cpu = row.xpath(".//td[@class='name']/div[@class='description']/text()").get()

            # Multi-core score (in <td class='score'>)
            score = row.xpath(".//td[@class='score']/text()").get()

            # Skip header/empty rows
            if not device or not score:
                continue

            # DICTIONARY OUTPUT
            yield {
                "Rank": rank,
                "Device": device.strip(),
                "CPU": cpu.strip() if cpu else None,
                "Multi-Core Score": score.strip(),
            }

            rank += 1

        # Follow pagination
        next_page = response.xpath("//a[@rel='next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
