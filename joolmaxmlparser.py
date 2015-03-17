# -*- coding: utf-8 -*-

from lxml import etree
import os


class HtmlArticle():
    def __init__(self, a_id, a_state, a_created, a_modified, a_category, a_language, a_title, a_alias, a_metakey, a_introtext, a_fulltext):
        self.a_id = a_id
        self.a_state = a_state
        self.a_created = a_created
        self.a_modified = a_modified
        self.a_category = a_category
        self.a_language = a_language
        self.a_title = a_title
        self.a_alias = a_alias
        self.a_metakey = a_metakey
        self.a_introtext = a_introtext
        self.a_fulltext = a_fulltext

        # Special case to get the category right
        self.a_category_special = ''
        categoryarray = str.split(a_category, '/')
        if len(categoryarray) > 1:
            self.a_category_special = categoryarray[1]
        if len(categoryarray) is 1:
            self.a_category_special = a_category

        # Special case to replace empty metadata with something meaningful
        if self.a_metakey is None:
            self.a_metakey = self.a_category_special

        self.article_header = '''<html>
        <head>
            <title>{header_title}</title>
            <meta name="slug" content="{header_alias}" />
            <meta name="tags" content="{header_metakey}" />
            <meta name="date" content="{header_created}" />
            <meta name="modified" content="{header_modified}" />
            <meta name="category" content="{header_category}" />
            <!--<meta name="lang" content="{header_language}" />-->
            <meta name="authors" content="Author name" />
            <meta name="summary" content="{header_introtext}" />
        </head>'''.format(header_created=self.a_created, header_modified=self.a_modified, header_category=self.a_category_special, header_language=self.a_language, header_title=self.a_title, header_alias=self.a_alias, header_metakey=self.a_metakey, header_introtext=self.a_introtext)

        self.article_body = '''
            <body>
                {html_body}
            </body>'''.format(html_body=self.a_fulltext)

        self.article_footer = '''
            </html>'''

    def __repr__(self):
        encodedString = self.article_header + self.article_body + self.article_footer
        return self.unescape(encodedString)

    def __str__(self):
        encodedString = self.article_header + self.article_body + self.article_footer
        return self.unescape(encodedString)

    def get_id(self):
        return self.a_id

    def get_state(self):
        return self.a_state

    def get_created(self):
        return self.a_created

    def get_alias(self):
        return self.a_alias

    def get_category(self):
        return self.a_category

    def unescape(self, s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&nbsp;", " ")

        s = s.replace("&amp;", "&")
        return s


def parse():
    # Configure the parser
    #parser = etree.XMLParser(ns_clean=True)

    # Parse the file into an ElementTree instance
    et = etree.parse("sitename")

    # Get the root of the tree
    et_root = et.getroot()

    article_collection = []

    for content in et_root:
        a_id = a_state = a_created = a_modified = a_category = a_language = a_title = a_alias = a_metakey = a_introtext = a_fulltext = ""
        for element in content:
            if element.tag == 'id':
                a_id = element.text
            if element.tag == 'state':
                a_state = element.text
            if element.tag == 'created':
                a_created = element.text
            if element.tag == 'modified':
                a_modified = element.text
            if element.tag == 'catid':
                a_category = element.text
            if element.tag == 'language':
                language = element.text
                if language is not "*":
                    a_language = language
            if element.tag == 'title':
                a_title = element.text
            if element.tag == 'alias':
                a_alias = element.text
            if element.tag == 'metakey':
                a_metakey = element.text
            if element.tag == 'introtext':
                a_introtext = element.text
            if element.tag == 'fulltext':
                a_fulltext = element.text

        a_article = HtmlArticle(a_id, a_state, a_created, a_modified, a_category, a_language, a_title, a_alias, a_metakey, a_introtext, a_fulltext)
        if a_state == '1':
            article_collection.append(a_article)
        else:
            #print "Not Published"
            pass

    for article in article_collection:
        # Retriece the information we need to create the savepath
        a_alias = article.get_alias()
        a_category = article.get_category()

        filename = '/Users/username/Utvikling/spyder/ssg/www.sitename.no/content/imported/' + a_category + "/" + a_alias + ".html"
        # Create folders on the path if needed (mkdir -p)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        # Write our html file to the correct path
        f = open(filename, 'w')
        f.write(str(article))
        f.close()

    return "Done parsing"

if __name__ == '__main__':
    parse()
