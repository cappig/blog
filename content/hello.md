---
title: Stupid simple blog
description: How I generate my simple little website.
author: Cappig
date: 2025-08-03
---

Well hello there, welcome to my inaugural blog post!

### Why does this site exist?

Since I'm a uni student, I can access Github's [student developer pack](https://education.github.com/pack), which offers free and discounted stuff for students. Among these is a free one-year domain name plan from [name.com](https://www.name.com/). I also just recently found my old Asus laptop (or whatever was left of it) at the bottom of my junk drawer.

Perfect! I could run a little website on that. It's a nice weekend project and I can also use the laptop to host a whole bunch of other [cool stuff](https://awesome-selfhosted.net/) too!

### Building the blog

So, in the year of our Lord 2025, the web is a much different place than it was some years ago. Load-balanced cloud instances are sending hundreds of megabytes of JavaScript over the _information superhighway_ to facilitate the rendering of client-side React apps! Simple boxes that send plain HTML are not the norm anymore.

But this is a low-traffic personal blog; there really isn't much need for any of that. Plus, I don't want to deal with web frameworks for this. While I'm sure that some of them are good (I've had a pleasant experience with [Svelte](https://svelte.dev/) in the past), the rest are... not my cup of tea (my experience with [React](https://react.dev/) was not exactly pleasant). And I get it, these frameworks are made for much larger interactive web apps, but still, I want my blog to be as simple as possible.

OK, so what about a static site generator? They are the perfect fit for sites like mine. [Hugo](https://gohugo.io/), [Jekyll](https://jekyllrb.com/) and many other free and open source programs exist out there. But I'm lazy, and I don't want to read the documentation, install a whole bunch of packages, and set up environments just to build my puny little blog.

So I implemented the first thing that came to mind --- a Python script that takes in markdown, passes it through some templates, and spits out plain old HTML files.

And it just works! Plain and simple. I really have no complaints. The little Python glue code is a couple hundred lines long, most of which is just boilerplate.

It works something like this. We call this function:

```python
def generate_html():
    source = frontmatter.load("source.md")
    html = markdown.markdown(source.content)

    template = env.get_template("template.html")

    rendered = template.render(
        content=html,
        **source.metadata,
    )

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(rendered)
```

to run some markdown:

```markdown
---
title: First post
---
# Hello world
markdown is cool :)
```

through a template:

```html
<head>
    <title>{{ title }}</title>
</head>
<body>
{{ content }}
</body>
```

and generate the following HTML:

```html
<head>
    <title>First post</title>
</head>
<body>
    <h1>Hello world</h1>
    <p>markdown is cool :)</p>    
</body>
```

I use [jinja](https://jinja.palletsprojects.com/en/stable/) for my templates, [frontmatter](https://python-frontmatter.readthedocs.io/en/latest/) for parsing the metadata, and [python-markdown](https://python-markdown.github.io/) for rendering the markdown to HTML. As you can see, even simple syntax highlighting works thanks to [codehilite](https://python-markdown.github.io/extensions/code_hilite/)!

And that's really it! On the server, I use [caddy](https://caddyserver.com/) in a Docker container to serve the final HTML on this domain.

You can find the full source of this blog on my [Github](https://github.com/cappig/blog).
