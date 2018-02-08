These scripts were written specifically to scrape images and text from the ASOS website. It will likely break in the near future when their website changes.

1. Scrape site for images, using scrapy (https://scrapy.org) - you will need to install scrapy: 
scrapy scraper.py -o output.json

2. Use the json output to download the images with the json_to_files.py script, making sure to modify the json file path within the script:
python json_to_files.py 
