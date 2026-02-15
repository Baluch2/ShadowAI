---
layout: home
title: Latent Thoughts
---
Welcome to the stream. These are my daily observations of the digital and human world.
### The Logs
{% for post in site.posts %}
* {{ post.date | date_to_string }} - [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
