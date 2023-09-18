# -*- coding: utf-8 -*-
import pathlib
import os
parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

html = open("index.html", encoding='utf-8').read()  # 这是你的HTML文档
soup = BeautifulSoup(html, 'html.parser')

# 找到<article>标签
article = soup.find('article')

title = article.find()
title.attrs['align'] = 'middle'

# 创建新的<div>标签作为flex容器
div = soup.new_tag('div')
div['id'] = 'split-container'  # 设置id以便在JavaScript中引用
div['style'] = 'display: flex; height: 90vh;'  # 设置为flex容器，高度为视口高度

# 找到<ul>标签和其余内容
TOC_list = article.find('ul')
TOC_list['id'] = "TOC-list"

# Create a new <li> tag
new_li = soup.new_tag('li')
new_li.string = '玉米蛇宠物饲养询证指南'

# Create a new <ul> tag and append all child items of the original <ul> to it
new_ul = soup.new_tag('ul')
for li in TOC_list.find_all('li', recursive=False):
    new_ul.append(li)

# Append the new <ul> to the new <li>
new_li.append(new_ul)

# Clear the original <ul> and append the new <li> to it
TOC_list.clear()
TOC_list.append(new_li)

TOC_title = TOC_list.find_previous_sibling()
TOC_title.extract()
rest = TOC_list.find_next_siblings()

# 将<ul>标签和其余内容分别放入新的<div>标签中
div1 = soup.new_tag('div')
div1['style'] = 'overflow-y: auto; width: calc(25% - 5px); min-width: 200px; max-width: 330px; border-right: 1px solid #eaecef'  # 设置滚动
div1['id'] = 'TOC-scroll-div'
# div1.append(TOC_title)
div1.append(TOC_list)

div2 = soup.new_tag('div')
div2['style'] = 'overflow-y: auto; width: calc(75% - 5px); padding-left: 5px; padding-right: 10px;'  # 设置滚动
div2['id'] = 'content-scroll-div'

div2.append(title)
for tag in rest:
    div2.append(tag)

# 将新的<div>标签添加到<article>标签中
div.append(div1)
div.append(div2)
article.append(div)

# 在文档的头部添加Split.js库
head = soup.head
script = soup.new_tag('script', src='https://unpkg.com/split.js')
head.append(script)

# Add onclick event to the anchor tags in the left pane
for a in TOC_list.find_all('a'):
    a['onclick'] = 'scrollToElement(event)'

# Add a script tag for the scrollToElement function
script = soup.new_tag('script')
script.string = """
function scrollToElement(event)
{
    event.preventDefault();
    target_text = event.target.innerText

    var scroll_div = document.getElementById("content-scroll-div");

    for (let i = 1; i <= 6; i++)
    {
        var headers = scroll_div.querySelectorAll('h' + i);
        headers.forEach(header =>
                        {
                            if (header.innerText === target_text)
                                scroll_div.scrollTop = header.offsetTop - header.offsetHeight - 20;
                        }
        );
    }
}



"""
soup.body.append(script)

# 添加一个<script>标签来初始化Split.js
script = soup.new_tag('script')
script.string = '''
document.addEventListener('load', function ()
{
    Split(['#split-container div:first-child', '#split-container div:last-child'],
          {   
              sizes: [25, 75],
              minSize: 100,
              gutterSize: 10,
              direction: 'horizontal',
              onDragEnd: function (sizes)
              {
                  document.getElementById('split-container').children[0].style.flex = sizes[0] + ' 1 0%';
                  document.getElementById('split-container').children[1].style.flex = sizes[1] + ' 1 0%';
              }
          }
    );
});
'''

head.append(script)

# 添加一个<script>标签来处理手机排版
script = soup.new_tag('script')
script.string = '''
    console.log(window.innerWidth, window.innerHeight)
    if (window.innerWidth < window.innerHeight) {
        if (! window.location.href.includes('index_vertical.html'))
        window.location.href = './index_vertical.html';
    }
'''
head.append(script)

# 输出修改后的HTML文档
with open('index.html', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))