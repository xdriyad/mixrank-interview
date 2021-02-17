##### requirement: 
- install nix
- use `nix-shell`
##### Solution 1
- built using scrapy package
- use `scrapy runspider py/logocrawler/main.py`
- It will produce result.csv and summery.txt 
- `result.csv` has all the crawled logo links and favicon links
- `summery.txt` has details about precision and recall

##### Solution 2

- built using requests and beautifulsoup4 packages
- use `python py/logocrawler/solution2.py`
- It will produce result.csv and summery.txt 
- `result2.csv` has all the crawled logo links and favicon links
- `summery2.txt` has details about precision and recall
