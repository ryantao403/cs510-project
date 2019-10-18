from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import *
from bs4 import BeautifulSoup as bs4
import os
import glob 
import json

class Parser :
    def __init__(self, indexing_dir = "./papers_to_index/") :
        self.dir = indexing_dir
        self.article_dict = {}

        
    def parse_article(self, article_path) :
        raw = open(article_path, 'r')
        article = dict()
        lines = raw.readlines()
        for idx, line in enumerate(lines) :
            if line.strip() == "<title>" :
                article['title'] = lines[idx+1].strip()
            elif line.strip() == '<abstract>' :
                article['abstract'] = lines[idx+1].strip()
            elif line.strip() == '<introduction>' and 'abstract' not in article :
                article['abstract'] = lines[idx+1].strip() if len(lines) > idx + 1 else ''
            if len(article) == 2 :
                break
        raw.close()
        return article if len(article) == 2 else None


    def parse_xml_article(self, article_path) :
        with open(article_path, 'r') as doc :
            soup = bs4(doc, 'lxml')
            article = dict()
            try :
                article['title'] = soup.title.getText()
                article['abstract'] = soup.abstract.getText()
            except :
                article = None
        return article

    
    def parse_all(self) :
        count_files = 0
        count_abnormal_parses = 0
        for filepath in os.listdir(self.dir) :
            count_files += 1
            path = os.path.join(self.dir, filepath)
            article = self.parse_xml_article(path) 
            if article :
                if article['title'].strip() == '' :
                    count_abnormal_parses += 1
#                     print("### Invalid Article:", filepath)
                    continue
                article['filename'] = filepath
                self.article_dict[filepath] = {'title': article['title'], 'abstract': article['abstract']}
        print("### Parse Completed [%d/%d]" % (count_files - count_abnormal_parses, count_files))
    

    def clean(self) :
        self.article_dict = {}
    

class Searcher:
    def __init__(self, index_path, index_name = "papers", parser = None) :
        self.index_path = index_path
        self.index_name = index_name
        self.schema = Schema(title = TEXT(stored=True), path = ID(stored=True), abstract = TEXT(stored=True))
        if not parser:
            print('No parser input, creating one...')
            self.parser = Parser()
        else: 
            self.parser = parser
        self.create_index()
        
        
    def create_index(self):
        """
        input: index path
        return index
        """
        if not os.path.exists(self.index_path) :
            os.mkdir(self.index_path)

        if not exists_in(self.index_path, indexname=self.index_name) :
            self.parser.parse_all()
            self.idx = create_in(self.index_path, self.schema, indexname=self.index_name)
            self.add_files()
            self.parser.clean()
        else :
            self.idx = open_dir(self.index_path, indexname=self.index_name)

    
    def add_files(self):
        """
        input: file_dict, key, path
        return a index 
        """ 
        writer = self.idx.writer()        
        for path, article in self.parser.article_dict.items():
            writer.add_document(title = article['title'], path = path, abstract = article['abstract'])
        writer.commit()


    def search(self, query):
        """
        input: query string 
        return json as follow 
        {{'title': title, 'abstract': abstract, 'path': doc path}, ...}
        """
        query_results = []
        with self.idx.searcher() as searcher:
            # query title and content using Multifield Parser
            query_parser = MultifieldParser(['title', 'abstract'], self.idx.schema)
            query_parser.add_plugin(FuzzyTermPlugin())
            query_parsed = query_parser.parse(query)
            results = searcher.search(query_parsed, terms=True)
            for r in results:
                query_results.append(dict(r))

        for v in query_results :
            print(v)
        query_results = json.dumps(query_results)
        return query_results


# examples to setup the search engine and perform search
parser = Parser()
searcher = Searcher(index_path = './indexdir', parser = parser)
# to search
query = 'hello'
searcher.search(query)
