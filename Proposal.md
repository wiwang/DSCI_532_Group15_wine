# Wine Reviews
## 1: Motivation and Purpose

**Our role**: Online Wine Database
**Target audience**: Wine consumers

For wine lovers, identifying quality wine among the tens of thousands of available options can be a challenge. This can make tracking down good quality wine at a desired price point quite difficult. To help consumers shop smarter and make more informed purchase decisions we are building a consumer friendly dashboard designed to present information from a database of over 130,000 wines + reviews in a simple to use and visually appealing manner. Our dashboard will allow users to apply filters to different features of wine (price, designation, country of origin, etc.) and browse a huge catalogue of different products. It will be able to display a provided review of each beverage and allow users to read detailed summary information about each wine and review (country of origin, vintage year, reviewer name, etc.). This dashboard will allow any consumer to find a wine that satisfies their tastes, and help them make informed purchasing decisions. 


## 2: Data Description

We will be visualizing a dataset of approximately 130,000 wine reviews. Each individual wine + review has 13 associated variables. General information about each wine includes the cost of the wine in USD (`price`), the type of grapes used to grow the wine (`variety`), the country/winery the wine is from (`country`, `province`, `winery`), and the vineyard information describing where the grapes that made the wine are from (`designation`) as well as where they were grown (`region_1`, `region_2`). Information specifically relating to reviews of the wine include the testers who tasted the wine (`tester_name`, `tester_twitter`), a written review of the wine (`description`), a title of the wine review (`title`), and a 1-100 points review score provided by WineEnthusiast (`points`). Using this data we are also considering the derivation of new variables through the use of automated web scraping to retrieve information such as a picture of each wine from a website such as Vivino.

## 3: Research Questions and Usage Scenarios

Camilla is a 37-year-old office lady who fancies herself something of a wine connoisseur. She is interested in purchasing a variety of different wines for a wine tasting party that she will be hosting for her like minded coworkers (she’s been saving for months to prepare this event). In order to build a solid selection of drinks for her guests she hopes to identify an assortment of quality wines to suit everyone’s tastes. She wants the collection of wines at her party to be from multiple different countries, consist of a variety of different blends, and to represent different price ranges. Finally, Camilla wants to only purchase the wines that have positive reviews from tasters to impress her guests as much as possible.
 
By using our dashboard she hopes to be able to identify the collection of wines that she will be purchasing for her party. Upon opening the dashboard she immediately adjusts the WineEnthusiast quality score slider on the dashboard to only include wines with a score of 90 or higher. She first wants to choose a wine that is foreign and expensive to make a strong first impression. She clicks a filter to make sure that no wine from the United States or Canada is included in her search and sets her price range to be $70 or higher and hunts down an exotic Frappato from Italy. Next, she wants to provide something more familiar to her guests, so she inverts her filter and finds a Pinot Gris bottled in the United States within a price range of $30 to $50. Finally, she wants her last wine to have a vintage between 2013 and 2015 so sets the vintage range to those years and reads through the reviews of four different wines before finding a white blend from Portugal. Finally, she can now throw the wine tasting party of her dreams!



