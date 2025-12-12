

scrapy startproject geekbench
cd geekbench
scrapy genspider android_multi browser.geekbench.com
scrapy crawl android_multi -o multicore.json
