import search_engine

# examples to setup the search engine and perform search
parser = search_engine.Parser()
searcher = search_engine.Searcher(index_path = './indexdir', parser = parser)
# to search
query = 'hello'
searcher.search(query)
