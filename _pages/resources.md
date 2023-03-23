---
layout: archive
title: "Resources"
permalink: /resources/
title: "Resources"
author_profile: true
---


{% include base_path %}


Data
======

<ul> {% for post in site.data %}
  {% include archive-single.html %}
{% endfor %} </ul>


Publications
======
  <ul>{% for post in site.publications %}
    #{% include archive-single-cv.html %}
  {% endfor %}</ul>
