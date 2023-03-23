---
layout: archive
title: "Resources"
permalink: /resources/
author_profile: true
---

Data 1
======
{% include base_path %}

{% for post in site.resources reversed %}
  {% include archive-single.html %}
{% endfor %}





Data
======
<ul> {% for post in site.resources %}
   {% include archive-single-cv.html %}
  {% endfor %} </ul>


Publications
======
  <ul>{% for post in site.publications %}
    {% include archive-single-cv.html %} <! --- here is the problem 
  {% endfor %}</ul>
