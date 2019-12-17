from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import *
from bs4 import BeautifulSoup as bs4
from rake_nltk import Rake
import os
import json
import pyltr
import tempfile
import shelve


class Parser :
    def __init__(self, indexing_dir = "./papers_to_index/") :
        self.dir = indexing_dir
        self.article_dict = {}
        self.selected_keywords = ['machine translation', 'statistical machine translation', 'computational linguistics', 'sentiment analysis', 'natural language processing', 'dependency parsing', 'named entity recognition', 'question answering', 'speech tagging', 'neural machine translation', 'coreference resolution', 'information extraction', 'document summarization', 'domain adaptation', 'social media']
        self.rake_extractor = Rake(min_length = 2, max_length = 3) # Uses stopwords for english from NLTK, and all puntuation characters.


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
                self.rake_extractor.extract_keywords_from_text(article['title'])
                area = [keyword for keyword in self.rake_extractor.get_ranked_phrases() if keyword in self.selected_keywords]
                if area:
                    area = area[0] # only maintain one area
                else:
                    area = ""
                self.article_dict[filepath] = {'title': article['title'], 'abstract': article['abstract'], 'area': area}
        print("### Parse Completed [%d/%d]" % (count_files - count_abnormal_parses, count_files))


    def clean(self) :
        self.article_dict = {}


class Searcher:
    def __init__(self, index_path, index_name = "papers", parser = None) :
        self.index_path = index_path
        self.index_name = index_name
        self.schema = Schema(title = TEXT(stored=True), path = ID(stored=True), abstract = TEXT(stored=True), area = TEXT(stored=True))
        if not parser:
            print('No parser input, creating one...')
            self.parser = Parser()
        else:
            self.parser = parser
        self.create_index()
        self.init_env()

    def init_env(self) :
        from whoosh import qparser, query, scoring
        from whoosh.analysis import RegexTokenizer
        from whoosh.lang.morph_en import variations

        self.freq_searcher = self.idx.searcher(weighting=scoring.Frequency())
        self.tfidf_searcher = self.idx.searcher(weighting=scoring.TF_IDF())
        self.bm25_searcher = self.idx.searcher(weighting=scoring.BM25F(B=0.74, K1=1.52))
        self.query_parser = QueryParser('abstract', self.idx.schema)
        self.query_parser.add_plugin(FuzzyTermPlugin())
        self.title_parser = QueryParser('title', self.idx.schema)
        self.title_parser.add_plugin(FuzzyTermPlugin())
        self.tokenizer = RegexTokenizer()

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
            writer.add_document(title = article['title'], path = path, abstract = article['abstract'], area = article['area'])
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
            query_parser = MultifieldParser(['title', 'abstract', 'area'], self.idx.schema)
            query_parser.add_plugin(FuzzyTermPlugin())
            query_parsed = query_parser.parse(query)
            results = searcher.search(query_parsed, terms=True, limit=100)
            for r in results:
                query_results.append(dict(r))

        for v in query_results :
            print(v)
        return query_results


    def suggest(self, query) :
        """
        input: query string
        return json as follow 
        {str, str, ...}
        """
        # to make correct search suggestions
        word_candidates = []
        s = self.idx.reader()
        corrector = s.corrector('abstract')
        with self.idx.reader() as r :
            for word in query.split(" ") :
                word_candidates.append([x[1].decode('utf-8') for x in r.most_distinctive_terms('title', number=2, prefix=word)])
                if len(word_candidates[-1]) == 0 :
                    word_candidates[-1] = [x for x in corrector.suggest(word, limit = 2)]
                if len(word_candidates[-1]) == 0 :
                    word_candidates[-1] = [word]
            # print(word_candidates)

        res = [""]
        for word_list in word_candidates :
            new = []
            for prefix in res :
                for word in word_list :
                    new.append((prefix + " " + word).strip())
            res = new
        print(res)
        return [{'value':x} for x in res]

    def genearte_LETOR_data(self, qid, cur_query, docid, content, title, rel) :
        terms = cur_query.split(' ')
        q = self.query_parser.parse("path:\'"+docid+"\' "+" OR ".join(terms))
        q_2 = self.title_parser.parse("path:\'"+docid+"\' "+" OR ".join(terms))
        results = self.freq_searcher.search(q, limit=None)
        tf_a = 0.0
        if len(results):
    #         print("Abstract TF feature", results[0].score)
            tf_a = results[0].score
        
        results = self.freq_searcher.search(q_2, limit=None)
        tf_t = 0.0
        if len(results):
    #         print("Title TF feature", results[0].score)
            tf_t = results[0].score

        idf_a = sum(self.freq_searcher.idf("abstract", x) for x in terms)
    #     print("Abstract IDF feature", idf_a)
        idf_t = sum(self.freq_searcher.idf("title", x) for x in terms)
    #     print("Title IDF feature", idf_t)

        results = self.tfidf_searcher.search(q, limit=None)
        tfidf_a = 0.0
        if len(results):
    #         print("Abstract TF-IDF feature", results[0].score)
            tfidf_a = results[0].score
        
        results = self.tfidf_searcher.search(q_2, limit=None)
        tfidf_t = 0.0
        if len(results):
    #         print("Title TF-IDF feature", results[0].score)
            tfidf_t = results[0].score

        results = self.bm25_searcher.search(q, limit=None)
        bm25_a = 0.0
        if len(results):
    #         print("Abstract BM25 feature", results[0].score)
            bm25_a = results[0].score
        
        results = self.bm25_searcher.search(q_2, limit=None)
        bm25_t = 0.0
        if len(results):
    #         print("Title BM25 feature", results[0].score)
            bm25_t = results[0].score

        dl = len(list(x for x in self.tokenizer(content)))
    #     print("DL feature", dl)
        
        tl = len(list(x for x in self.tokenizer(title)))
    #     print("TL feature", tl)
        
        return rel + " qid:%s 1:%f 2:%f 3:%f 4:%f 5:%f 6:%f 7:%f 8:%f 9:%f 10:%f #docid = %s\n" % (qid, tf_a, tf_t, idf_a, idf_t, tfidf_a, tfidf_t, bm25_a, bm25_t, dl, tl, docid)

    def ltr_search(self, query) :
        from whoosh.query import Variations
        query_results = []
        with open('ltr_model.pickle', 'rb') as f:
            model = pickle.load(f)
        searcher = self.idx.searcher()
        rels = shelve.open("user_qrels")
        # query title and content using Multifield Parser
        query_parser = MultifieldParser(['title', 'abstract', 'area'], self.idx.schema, termclass=Variations)
        query_parser.add_plugin(FuzzyTermPlugin())
        query_parsed = query_parser.parse(query)
        results = searcher.search(query_parsed, terms=True, limit=100)

        max_rels = 1
        for r in results[:] :
            pair = r['path'] + '##' + query
            if pair in rels :
                max_rels = max(max_rels, abs(rels[pair][0] - rels[pair][1]))
            #if rels[pair][1] - rels[pair][0] > 0 :
            #    results.remove(r)

        wr = tempfile.TemporaryFile('w+')
        for r in results:
            wr.write(self.genearte_LETOR_data('1', query, r['path'], r['abstract'], r['title'], '1'))
        wr.seek(0)
        features, _, qids, docs = pyltr.data.letor.read_dataset(wr)
        p = model.predict(features)
        wr.close()

        results = []
        for j in range(len(qids)) :
            d = searcher.document(path=docs[j][8:].strip())
            pair = d['path'] + '##' + query
            rel_score = ((rels[pair][0] - rels[pair][1]) / max_rels) if pair in rels else 0
            results.append((p[j] * 0.8 + rel_score * 0.2, d, 1 if rel_score > 0 else 0))
        rels.close()

        results.sort(key = lambda x:x[0], reverse = True)
        for r in results:
            new_dict = dict(r[1])
            new_dict['rel'] = r[2]
            query_results.append(new_dict)

        return query_results

    def recommend(self, doc_path, top = 20) :
        recommend_results = []
        docnum = self.bm25_searcher.document_number(path=doc_path)
        doc = self.bm25_searcher.document(path=doc_path)
        if not docnum :
            return recommend_results
        for r in self.bm25_searcher.more_like(docnum, u'abstract', top=top) :
            recommend_results.append(dict(r))
        return {'recommendation':recommend_results, 'paper':dict(doc)}

    def log_relevance(self, doc_path, query, rel) :
        rels = shelve.open("user_qrels")
        pair = doc_path + '##' + query
        if pair not in rels :
            rels[pair] = [0, 0]
        else :
            counter = rels[pair]
            if rel :
                counter[0] += 1
            else :
                counter[1] += 1
            rels[pair] = counter
        rels.close()

        return {'error': None}


