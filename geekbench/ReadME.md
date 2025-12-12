
```bash
scrapy startproject geekbench
```
```bash
cd geekbench
```
```bash
scrapy genspider android_multi browser.geekbench.com
```
```bash
scrapy crawl android_multi -o multicore.json
```
