""" Parsers for wikitext (page content) downloaded using Wikipedia's API with the nlpia2_wikipedia package """
import re
import pandas as pd

RE_HEADING = r'^\s*[=]+ [^=]+ [=]+\s*'


def paragraphs_dataframe(page):
    """ Split wikitext into paragraphs and return a dataframe with columns for headings (title, h1, h2, h3, ...)

    TODO: create a method or property within a wikipedia.Page class with this function

    >>> from nlpia2_wikipedia.wikipedia import wikipedia as wiki
    >>> page = wiki.page('Large language model')
    >>> df = paragraphs_dataframe(page)
    >>> df.head(2)

    """
    paragraphs = [p for p in page.content.split('\n\n')]
    headings = [page.title]
    df_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        p_headings = re.findall(RE_HEADING, p)
        # TODO strip headings from front of p
        # TODO use match instead of findall (only need 1)
        while p_headings:
                h = p_headings[0]
                p = p[len(h):].strip()
                h = h.strip()
                level = len([c for c in h if c == '=']) + 1
                h = h.strip('=').strip()
                headings = headings[:level]
                if len(headings) <= level:
                    headings = headings + [''] * (level - len(headings))
                    headings[level - 1] = h
                p_headings = re.findall(RE_HEADING, p)
        if p:
            p_record = dict(text=p, title=page.title)
            p_record.update({f'h{i}': h for (i, h) in enumerate(headings)}) 
            df_paragraphs.append(p_record)
    return pd.DataFrame(df_paragraphs)


