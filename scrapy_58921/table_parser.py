from scrapy.selector import Selector
from scrapy.http import HtmlResponse


year = 1996
target_url = "http://58921.com/alltime/{year}".format(year=year)
# response = HtmlResponse(target_url)

table_css_pattern = ".movie_box_office_stats_table"

header = response.css(table_css_pattern).css("thead").css("tr th").extract()
