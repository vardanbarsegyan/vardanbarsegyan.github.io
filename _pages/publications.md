---
permalink: /_pages/publications
title: "Publications"
excerpt: "Publications"
author_profile: true
redirect_from: 
  - /_pages/publications/
  - /publications.md
---



{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
