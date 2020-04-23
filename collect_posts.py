from web_handlers.reddit_source_handler import RedditSourceHandler
from pandas import DataFrame, concat
import plac
import yaml
from os import path
from os import makedirs
import logging

from web_handlers.twitter_source_handler import TwitterSourceHandler

logger = logging.getLogger('post_collector')
logger.setLevel(logging.INFO)


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
    logger.info('initialising')
    conf = get_conf(conf_loc)
    reddit_source = RedditSourceHandler(conf['REDDIT_CLIENT_ID'],
                                        conf['REDDIT_CLIENT_SECRET'],
                                        conf['REDDIT_USER_AGENT'])
    logger.info(f'Getting Reddit posts involving {company_name}')
    reddit_posts = reddit_source.get_posts(company_name, 10000)
    reddit_frame = DataFrame.from_records([post.as_dict() for post in reddit_posts])
    twitter_source = TwitterSourceHandler()
    logger.info(f'Obtaining posts from Twitter for {company_name}')
    twitter_posts = twitter_source.get_posts(company_name)
    twitter_frame = DataFrame.from_records([post.as_dict() for post in twitter_posts])
    all_posts = concat([twitter_frame, reddit_frame]).sort_values(by=['created_date'], ascending=False)
    makedirs(conf['OUTPUT_LOC'], exist_ok=True)
    for year, frame in all_posts.groupby('created_date'):
        out_path = path.join(conf['OUTPUT_LOC'], f'{year}.csv')
        logger.info(f'Outputting posts for {year} in {out_path.__str__()}')
        frame.to_csv(out_path)


if __name__ == '__main__':
    plac.call(main)
