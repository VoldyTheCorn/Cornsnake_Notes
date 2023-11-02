# -*- coding: utf-8 -*-
import pathlib
import os
parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

html = open("index_vertical.html", encoding='utf-8').read()  # 这是你的HTML文档
soup = BeautifulSoup(html, 'html.parser')

print("[Adding back-to-top button for vertical page]...",end='\n\n')

button_html = """<button id="top-button" style="position: fixed; bottom: 20px; right: 30px; z-index: 99; outline: none; background-color: white; color: black; cursor: pointer; padding: 15px; border-radius: 4px; width: 30px; height: 30px; background-image: url('images/Scroll_to_Top.png'); background-repeat: no-repeat; background-position: center; background-size: contain; border: none;">
</button>
<script>
//Get the button:
let mybutton = document.getElementById("top-button");

// When the user clicks on the button, scroll to the top of the document
mybutton.onclick = function() 
{  
    var scroll_div = document.getElementById("content-scroll-div");
    if (scroll_div.scrollHeight > scroll_div.clientHeight)
    {
        console.log(scroll_div)
        scroll_div.scrollTop = 0;
    }
    else // for cellphone layout
    {
        console.log(document.getElementsByClassName("gist-data")[0])
        document.getElementsByClassName("gist-data")[0].scrollTop = 0;
    }                       
}

</script>"""

# Find the body tag
body = soup.find('body')

# Insert the html_code at the beginning of the body
body.insert(0, BeautifulSoup(button_html, 'html.parser'))


# 输出修改后的HTML文档
with open('index_vertical.html', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))