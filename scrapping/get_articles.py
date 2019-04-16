import json

import newspaper
import click

from newspaper import Config, news_pool

SITES_URLS = [
    'https://www.onet.pl/',
    'http://www.gazeta.pl/0,0.html',
    'https://www.rp.pl/',
    'https://www.se.pl/',
]


@click.command(help='Download some articles')
@click.option("--output-path", type=str, default="./data/scrapping/articles.json")
def get_articles(
        output_path,
):
    config = dict(
        language='pl',
        fetch_images=False,
        MIN_WORD_COUNT=100,
        MIN_SENT_COUNT=5,
        memoize_articles=False,
    )

    papers = {}
    for url in SITES_URLS:
        paper = newspaper.build(url, **config)
        print(f"{url} contains {paper.size()} articles")
        papers[url] = paper

    print("Downloading...")
    news_pool.set(papers.values(), threads_per_source=2)
    news_pool.join()

    print("Parsing...")
    for paper in papers.values():
        for article in paper.articles:
            article.parse()

    articles = [art.text for paper in papers.values() for art in paper.articles]
    articles = [art.replace("\n", "") for art in articles]

    print(f"Scraped {len(articles)} articles")

    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(articles, f)


if __name__ == "__main__":
    get_articles()
