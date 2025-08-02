import frontmatter
import markdown
import re
import unidecode
import subprocess
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
import os

content_dir = "content"
template_dir = "templates"
output_dir = "site"

env = Environment(loader=FileSystemLoader(template_dir))


def slugify(text):
    text = unidecode.unidecode(text).lower()
    text = re.sub(r"[\W_]+", "-", text)
    text = re.sub(r"-+", "-", text)

    return text


def get_git_hash():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )


def collect_posts():
    posts = []

    # all markdown files that don't begin with '_'
    for filename in os.listdir(content_dir):
        if filename.endswith(".md") and not filename.startswith("_"):
            filepath = os.path.join(content_dir, filename)
            post = frontmatter.load(filepath)

            post_info = dict(post.metadata)

            post_info["filepath"] = filepath
            post_info["slug"] = slugify(post_info["title"])

            posts.append(post_info)

    # sort by publication dates
    return sorted(posts, key=lambda p: p.get("date", ""), reverse=True)


def generate_index(posts):
    index_path = os.path.join(content_dir, "_index.md")

    if not os.path.isfile(index_path):
        raise FileNotFoundError("Index page markdown not found")

    index_post = frontmatter.load(index_path)
    index_html = markdown.markdown(index_post.content, extensions=["extra"])

    template = env.get_template("index.html")

    rendered = template.render(
        index_blurb=index_html, latest_posts=posts[:5], **index_post.metadata
    )

    output_path = os.path.join(output_dir, "index.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Generated: {output_path}")


def generate_about():
    about_path = os.path.join(content_dir, "_about.md")

    if not os.path.isfile(about_path):
        raise FileNotFoundError("about page markdown not found")

    about_post = frontmatter.load(about_path)
    about_html = markdown.markdown(about_post.content, extensions=["extra"])

    template = env.get_template("about.html")

    rendered = template.render(
        content=about_html,
        git_hash=get_git_hash(),
        time=datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        **about_post.metadata,
    )

    output_path = os.path.join(output_dir, "about.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Generated: {output_path}")


def generate_404():
    template = env.get_template("404.html")

    rendered = template.render()

    output_path = os.path.join(output_dir, "404.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Generated: {output_path}")


def generate_post(post):
    template = env.get_template("article.html")

    article = frontmatter.load(post["filepath"])
    article_html = markdown.markdown(
        article.content,
        extensions=["extra", "codehilite"],
        extension_configs={"codehilite": {"css_class": "highlight"}},
    )

    output_filename = "blog/" + str(post["slug"]) + ".html"
    output_path = os.path.join(output_dir, output_filename)

    rendered = template.render(content=article_html, **article.metadata)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Generated: {output_path}")


def main():
    # Ensure output dirs exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "blog"), exist_ok=True)

    posts = collect_posts()

    generate_index(posts)
    generate_about()
    generate_404()

    for post in posts:
        generate_post(post)

    print("~ Site generated! ~")


if __name__ == "__main__":
    main()
