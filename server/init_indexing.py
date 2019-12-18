import search_engine

# examples to setup the search engine and perform search
parser = search_engine.Parser()
searcher = search_engine.Searcher(index_path = './indexdir', parser = parser)
# to search
query = 'hello'
searcher.search(query)
# customized add some areas of interest
for search_q in ['data mining', 'information retrieval', 'machine learning'] :
    writer = searcher.idx.writer()
    results = searcher.search(search_q, 500)
    for r in results :
        if r['area'].strip() == '' :
            writer.update_document(path=r['path'], title=r['title'], abstract=r['abstract'], area='information retrieval')
    writer.commit()
