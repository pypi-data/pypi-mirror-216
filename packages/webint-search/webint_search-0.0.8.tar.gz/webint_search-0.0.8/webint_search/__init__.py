"""Search your website."""

import collections

import eng_to_ipa
import pronouncing
import typesense
import web
import webagt
import wn
import youtube_search

app = web.application(__name__, prefix="search")
client = typesense.Client(
    {
        "nodes": [
            {
                "host": "localhost",
                "port": "8108",
                "protocol": "http",
            }
        ],
        "api_key": "hpAnnsIdJse2NejW8RFKKRZ8z2lfhRjWCNtWWvwNFWXTyB1Y",
        "connection_timeout_seconds": 2,
    }
)
books_schema = {
    "name": "books",
    "fields": [
        {"name": "title", "type": "string"},
        {"name": "authors", "type": "string[]", "facet": True},
        {"name": "publication_year", "type": "int32", "facet": True},
        {"name": "ratings_count", "type": "int32"},
        {"name": "average_rating", "type": "float"},
    ],
    "default_sorting_field": "ratings_count",
}
# client.collections.create(books_schema)
# with open("/tmp/books.jsonl") as jsonl_file:
#     client.collections["books"].documents.import_(jsonl_file.read().encode("utf-8"))


@app.wrap
def linkify_head(handler, main_app):
    """Ensure OpenSearch document is referenced from homepage."""
    yield
    if web.tx.request.uri.path == "":
        web.add_rel_links(
            search=(
                "/search/opensearch.xml",
                {
                    "type": "application/opensearchdescription+xml",
                    "title": "Angelo Gladding",
                },
            )
        )


@app.control("")
class Search:
    """Search everything."""

    def get(self):
        """Return an index of data sources."""
        try:
            query = web.form("q").q
        except web.BadRequest:
            return app.view.index()

        if query.startswith("!yt"):
            results = youtube_search.YoutubeSearch(query, max_results=10).to_dict()
            return app.view.youtube_results(query.partition(" ")[2], results)

        ipa_pronunciation = None
        cmu_pronunciation = None
        definition = None
        rhymes = []
        try:
            en = wn.Wordnet("oewn:2022")
        except wn.Error:
            pass  # TODO download Open English WordNet `python -m wn download oewn:2022`
        else:
            try:
                ss = en.synsets(query)[0]
            except IndexError:
                pass
            else:
                ipa_pronunciation = eng_to_ipa.convert(query)
                try:
                    cmu_pronunciation = pronouncing.phones_for_word(query)[0]
                except IndexError:
                    pass
                definition = ss.definition()
                rhymes = pronouncing.rhymes(query)

        web_results = webagt.get(
            f"https://html.duckduckgo.com/html?q={query}"
        ).dom.select(".result__a")

        code_projects = collections.Counter()
        code_files = collections.defaultdict(list)
        for code_project, code_file in web.application("webint_code").model.search(
            query
        ):
            code_projects[code_project] += 1
            code_files[code_project].append(code_file)

        # books = client.collections["books"].documents.search(
        #     {
        #         "q": query,
        #         "query_by": "authors,title",
        #         "sort_by": "ratings_count:desc",
        #     }
        # )
        books = {}

        return app.view.results(
            query,
            ipa_pronunciation,
            cmu_pronunciation,
            definition,
            rhymes,
            web_results,
            code_projects,
            code_files,
            books,
        )


@app.control("opensearch.xml")
class OpenSearch:
    """"""

    def get(self):
        web.header("Content-Type", "application/xml; charset=utf-8")
        return bytes(str(app.view.opensearch()), "utf-8")


@app.control("collections")
class Collections:
    """"""

    def get(self):
        return app.view.collections(client.collections.retrieve())
