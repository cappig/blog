import hashlib
import frontmatter
import markdown
import re
import unidecode
import subprocess
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os

content_dir = Path("content")
template_dir = Path("templates")
output_dir = Path("site")

env = Environment(loader=FileSystemLoader(template_dir))
env.globals["strftime"] = lambda format, dt: dt.strftime(format)

gen_time = datetime.now(timezone.utc)


def slugify(text):
    text = unidecode.unidecode(text).lower()
    text = re.sub(r"[\W_]+", "-", text)
    text = re.sub(r"-+", "-", text)

    return text


def render_markdown(content):
    return markdown.markdown(
        content,
        extensions=["extra", "codehilite", "smarty", "nl2br"],
        extension_configs={"codehilite": {"css_class": "highlight"}},
    )


def get_git_hash():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )


def get_file_hash(path):
    hasher = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()[:8]


def write_page(template_name, output_name, context=None):
    template = env.get_template(template_name)

    version = {
        "css_hash": get_file_hash("static/css/style.css"),
        "code_css_hash": get_file_hash("static/css/code.css"),
        "js_hash": get_file_hash("static/js/theme.js"),
    }

    rendered = template.render(gen_time=gen_time, **version, **(context or {}))

    output_path = output_dir / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Generated: {output_path}")


def collect_posts():
    posts = []

    for filename in os.listdir(content_dir):
        if filename.endswith(".md") and not filename.startswith("_"):
            filepath = os.path.join(content_dir, filename)
            post = frontmatter.load(filepath)

            post_info = dict(post.metadata)

            post_info["filepath"] = filepath
            post_info["slug"] = slugify(post_info["title"])

            posts.append(post_info)

    return sorted(posts, key=lambda p: p.get("date"), reverse=True)


def generate_index(posts):
    index_post = frontmatter.load(f"{content_dir}/_index.md")
    index_html = render_markdown(index_post.content)

    context = {
        "index_blurb": index_html,
        "latest_posts": posts[:5],
        **index_post.metadata,
    }

    write_page("index.html", "index.html", context)


def generate_about():
    about_post = frontmatter.load(f"{content_dir}/_about.md")
    about_html = render_markdown(about_post.content)

    context = {
        "content": about_html,
        "git_hash": get_git_hash(),
        **about_post.metadata,
    }

    write_page("about.html", "about.html", context)


def generate_links():
    links_post = frontmatter.load(f"{content_dir}/_links.md")
    links_html = render_markdown(links_post.content)

    context = {"content": links_html, **links_post.metadata}

    write_page("links.html", "links.html", context)


def generate_404():
    write_page("404.html", "404.html")


def generate_post(post):
    article = frontmatter.load(post["filepath"])
    post["content"] = render_markdown(article.content)

    context = {"content": post["content"], **article.metadata}

    write_page("article.html", f"blog/{post['slug']}.html", context)


def generate_blog(posts):
    context = {"posts": posts}
    write_page("blog.html", "blog.html", context)
    write_page("feed.xml", "blog/feed.xml", context)


def main():
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "blog"), exist_ok=True)

    generate_about()
    generate_links()
    generate_404()

    posts = collect_posts()

    for post in posts:
        generate_post(post)

    generate_blog(posts)
    generate_index(posts)

    print("~ Site generated! ~")


if __name__ == "__main__":
    main()
