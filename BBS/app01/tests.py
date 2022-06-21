from django.test import TestCase

# Create your tests here.
# 模拟网页数据
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc,'lxml')
print(soup.get_text())
print(soup.a)  # 查看单个a标签
print(soup.find('a'))  # 查看单个a标签
print(soup.find_all('a'))  # 查看所有a标签
