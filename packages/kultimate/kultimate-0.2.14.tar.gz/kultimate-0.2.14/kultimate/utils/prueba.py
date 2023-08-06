#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs

html = """
<h2>primer columna</h2>
<ul>
<li>primer tarea</li>
<li>segunda tarea</li>
<li>segunda tarea</li>
</ul>
<h2>segunda columna</h2>
<ul>
<li>primer tarea</li>
<li>segunda tarea</li>
<li>segunda tarea</li>
</ul>
<h2>tercer columna</h2>



<h2>cuarta columna</h2>



"""

la_sopa = bs(html, features="html.parser")
print(la_sopa)

h2s = la_sopa.find_all("h2")


for h2 in h2s:
    print(h2.text)
    next_sibling = h2.find_next_sibling()
    if next_sibling != None and next_sibling.name == "h2":
        print("\tsin tareas")
        continue
    elif next_sibling != None and next_sibling.name == "ul":
        print("\ttiene tareas")
    else:
        print("\tsin tareas")
