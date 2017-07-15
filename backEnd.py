import collections
from crawler import crawler
from pagerank import page_rank
from pymongo import MongoClient
import sys

DB_HOST = 'localhost'
DB_PORT = 27017

# Initialize mongodb connection
client = MongoClient(DB_HOST, DB_PORT)
db = client.randomSearch

# Make a new crawler object
crawler = crawler(None, 'urls.txt')

def backEnd_run(dep):
    # Crawl through the URLs provided in urls.txt
    crawler.crawl(depth=int(dep))

    # Retrieve Data needed for populating the SQL Tables
    doc_index = crawler.get_docs_cache()
    inverted_index = crawler.get_inverted_index()
    anchor_db = crawler.get_anchor_db()
    lexicon = crawler.get_lexicon()
    pg_rank = page_rank(crawler.get_links_queue())
    titles_list = crawler.get_title_cache()
    resolved_inverted_index = crawler.get_resovled_inverted_index()
    description = crawler.get_desc_cache()
    images = crawler.get_image_cache()

    return doc_index, titles_list, lexicon, anchor_db, pg_rank, inverted_index, description, images, resolved_inverted_index

def update_db(doc_index, titles_list, lexicon, anchor_db, pg_rank, inverted_index, description, images):
    pg_rank = set_rank_for_no_ourlink_urls(pg_rank, doc_index.values())
    for word, w_id in lexicon.items():
        # Map by words since we are searching
        #  by words on the client side
        outter_doc = {'Word':word, 'Docs':[]}

        for d_id in inverted_index[w_id]:
            doc = {}

            # Add the url
            doc['Url'] = [url for url, doc_id in doc_index.items() if doc_id == d_id][0]

            # Add the titles
            if d_id in titles_list:
                doc['Title'] = titles_list[d_id]
            # Add links
            if d_id in anchor_db:
                doc['Links'] = list(anchor_db[d_id])
            # Add page rank
            if d_id in pg_rank:
                doc['PageRank'] = pg_rank[d_id]
            # Add descriptions for site
            if d_id in description:
                doc['Description'] = description[d_id]

            outter_doc['Docs'].append(doc)

        db.docs.insert_one(outter_doc)

    if len(images) > 0:
        db.img_docs.insert_many([{'Word':key, 'Sources':value} for key,value in images.items()])


def set_rank_for_no_ourlink_urls(pg_rank, doc_ids):
    """Set 0 to page rank for urls with no outgoing links"""
    for id in doc_ids:
        if not id in pg_rank:
            pg_rank[id] = 0

    return pg_rank

def parse_dic_for_db(dic, key_type=int):
    """Parse a dictionary to an array of tuples as shown:
        [(key1, value1),(key1, value2),(key2, value3),(key3, value4)]
    """
    result = []

    for key, value in dic.items():
        if isinstance(value, collections.Iterable):
            for i in value:
                result.append((key_type(key), i))
        else:
            result.append((key_type(key),value))

    return result

if __name__ == '__main__':
    dep = sys.argv[1]
    args = backEnd_run(dep)
    update_db(*args[:-1])
