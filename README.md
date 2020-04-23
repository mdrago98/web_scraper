# Social Media Crawler

The following project implements a very basic web crawler to get posts from a variety of social media sources(Reddit, twitter) relating to a articular company.
The crawler is composed of two source handlers defined under crawler/web_handlers/ to handle each supported social media platform. The reddit handler is written using the praw api whilst the twitter handler parses twitter pages using beautiful soup to get posts. 
The handlers return a list of Post objects.
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The project is built and tested on python 3.7.7 running on Ubuntu 19.10. The Virtual Environment package is also required to set up a development environment


### Installing
First set up a virtual environment and activate it as follows:
```bash
python3 -m venv venv/ && source venv/bin/activate
```
Next install the dependencies listed in the requirements.txt file

```bash
pip install -r requirements.txt
```

Finally the scrip could be run as follows:
```bash
python post_collector.py company_name [config_location]
python post_collector.py google
>  INFO:root:Initialising
>  INFO:root:Getting Reddit posts involving google
>  INFO:root:Obtaining posts from Twitter for google
>  INFO:root:Generating csv file of posts written on 2019-12-18 as output/2019-12-18.csv
>  INFO:root:Generating csv file of posts written on 2019-12-30 as output/2019-12-30.csv

```

## Running the tests

The unit tests are built using the built in unittest package and are located under the tests/ directory. To produce a test report  run:
```bash
coverage run --source=crawler --omit venv -m unittest discover
coverage html -d docs/coverage/
```

## Built With

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - XML/HTML parsing tool
* [Praw](https://github.com/praw-dev/praw) - The python reddit api wrapper
* [Pandas](https://pandas.pydata.org/) - A fast data analysis and manipulation tool.
* [Plac](http://micheles.github.io/plac/) - Commandline argument parser.

## Authors

* **Matthew Drago** - *Initial work* - [Github](https://github.com/mdrago98)
