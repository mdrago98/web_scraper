from pandas import DataFrame, concat, to_datetime
import plac
import yaml
from os import path
from os import makedirs
import logging

from crawler.web_handlers import RedditSourceHandler, TwitterSourceHandler


def get_conf(conf_loc: str) -> dict:
    """
    Loads the yaml config
    :param conf_loc: the config location
    :return: a dictionary representing the config
    """
    with open(conf_loc) as conf_file:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        conf = yaml.safe_load(conf_file)
    return conf


def main(company_name, conf_loc='conf.yaml') -> None:
    """
    Runs the post extraction script
    :param company_name: the company name for which the reddit_posts are to be extracted
    :param conf_loc: the api configuration yaml file location
    :return: None
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('initialising')
    conf = get_conf(conf_loc)
    reddit_source = RedditSourceHandler(conf['REDDIT_CLIENT_ID'],
                                        conf['REDDIT_CLIENT_SECRET'],
                                        conf['REDDIT_USER_AGENT'])
    logging.info(f'Getting Reddit posts involving {company_name}')
    reddit_posts = reddit_source.get_posts(company_name, 10000)
    reddit_frame = DataFrame.from_records([post.as_dict() for post in reddit_posts])
    twitter_source = TwitterSourceHandler()
    logging.info(f'Obtaining posts from Twitter for {company_name}')
    twitter_posts = twitter_source.get_posts(company_name)
    twitter_frame = DataFrame.from_records([post.as_dict() for post in twitter_posts])
    all_posts = concat([twitter_frame, reddit_frame]).sort_values(by=['created_date'], ascending=False)
    all_posts['created_date'] = to_datetime(all_posts['created_date'])
    makedirs(conf['OUTPUT_LOC'], exist_ok=True)
    for date, frame in all_posts.groupby(by=all_posts['created_date'].dt.date):
        out_path = path.join(conf['OUTPUT_LOC'], f'{date}.csv')
        logging.info(f'Generating csv file of posts written on {date} as {out_path.__str__()}')
        frame.to_csv(out_path, index=False)


if __name__ == '__main__':
    plac.call(main)
