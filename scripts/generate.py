import hashlib
import frontmatter
import markdown
import re
import unidecode
import subprocess
import os
import sys
from datetime import date, datetime, time, timezone
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from pathlib import Path

content_dir = Path("content")
template_dir = Path("templates")
output_dir = Path("site")
site_url = "https://cappig.dev"

env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(["html", "xml"]),
    undefined=StrictUndefined,
)
env.globals["strftime"] = lambda format, dt: dt.strftime(format)

gen_time = datetime.now(timezone.utc)


def absolute_url(path):
    if path.startswith(("http://", "https://")):
        return path

    if not path.startswith("/"):
        path = f"/{path}"

    return f"{site_url}{path}"

def rfc3339(dt):
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    if isinstance(dt, date):
        return (
            datetime.combine(dt, time.min, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

    return str(dt)

def escape_cdata(text):
    return str(text).replace("]]>", "]]]]><![CDATA[>")

env.globals["absolute_url"] = absolute_url
env.globals["rfc3339"] = rfc3339
env.filters["cdata"] = escape_cdata


def slugify(text):
    text = unidecode.unidecode(text).lower()
    text = re.sub(r"[\W_]+", "-", text)
    text = re.sub(r"-+", "-", text)

    return text

def render_markdown(content):
    return markdown.markdown(
        content,
        extensions=["extra", "codehilite", "smarty"],
        extension_configs={"codehilite": {"css_class": "highlight"}},
    )


def get_git_hash():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )

def get_katex_version():
    version_file = Path("static/katex/version.txt")

    if not version_file.exists():
        print("katex sources not found!", file=sys.stderr)
        sys.exit(1)

    return version_file.read_text().strip()

def get_file_hash(path):
    hasher = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()[:8]


def validate_post_metadata(post_info, filepath):
    required_fields = ("title", "description", "author", "date")
    missing = [field for field in required_fields if not post_info.get(field)]

    if missing:
        raise ValueError(f"{filepath}: missing required metadata: {', '.join(missing)}")

    if not isinstance(post_info["date"], date):
        raise ValueError(f"{filepath}: date metadata must be a date")


def write_page(template_name, output_name, context=None):
    template = env.get_template(template_name)

    version = {
        "style_css_hash": get_file_hash("static/css/style.css"),
        "code_css_hash": get_file_hash("static/css/code.css"),
        "font_css_hash": get_file_hash("static/css/font.css"),
        "katex_version": get_katex_version()
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

            validate_post_metadata(post_info, filepath)

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

    metadata = dict(article.metadata)
    metadata.setdefault("image", "/static/img/serpent.webp")

    context = {"content": post["content"], "slug": post["slug"], **metadata}

    write_page("article.html", f"blog/{post['slug']}.html", context)

def generate_blog(posts):
    feed_updated = max((post["date"] for post in posts), default=gen_time)
    context = {"posts": posts, "feed_updated": feed_updated}
    write_page("blog.html", "blog.html", context)
    write_page("feed.xml", "blog/feed.xml", context)

def generate_sitemap(posts):
    pages = [
        {"loc": absolute_url("/"), "lastmod": None},
        {"loc": absolute_url("/about"), "lastmod": None},
        {"loc": absolute_url("/links"), "lastmod": None},
        {"loc": absolute_url("/blog"), "lastmod": None},
    ]

    pages.extend(
        {"loc": absolute_url(f"/blog/{post['slug']}"), "lastmod": post.get("date")}
        for post in posts
    )

    write_page("sitemap.xml", "sitemap.xml", {"pages": pages})


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
    generate_sitemap(posts)
    generate_index(posts)

    print("~ Site generated! ~")


if __name__ == "__main__":
    main()
