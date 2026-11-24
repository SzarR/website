"""Rebuild the blog from the original Markdown posts (pip install markdown pyyaml beautifulsoup4)."""
from pathlib import Path
from datetime import date, datetime
from html import escape
from urllib.parse import urlsplit
import shutil
import markdown
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/posts'
base = (ROOT / 'index.html').read_text()
if '<a href="blog/">Blog</a>' not in base:
    base = base.replace('<nav aria-label="Main navigation">', '<nav aria-label="Main navigation"><a href="blog/">Blog</a>')
    (ROOT / 'index.html').write_text(base)


def page(title, description, content, prefix):
    head, tail = base.split('<main>', 1)
    _, tail = tail.split('</main>', 1)
    soup = BeautifulSoup(head + '<main>' + content + '</main>' + tail, 'html.parser')
    soup.title.string = title + ' — Robert W. Szarek'
    soup.find('meta', attrs={'name': 'description'})['content'] = description
    soup.find('link', rel='stylesheet')['href'] = prefix + 'styles.css'
    soup.select_one('nav > a')['href'] = prefix + 'blog/'
    soup.select_one('nav > a')['aria-current'] = 'page'
    home = soup.new_tag('a', href=prefix)
    home.string = 'Home'
    soup.select_one('nav').insert(0, home)
    return str(soup)

posts = []
for path in sorted(SOURCE.glob('*.md')):
    text = path.read_text()
    _, front, body = text.split('---', 2)
    meta = yaml.safe_load(front)
    if meta.get('draft'):
        continue
    when = meta['date']
    if isinstance(when, dict):
        when = when.get('created')
    if isinstance(when, str):
        when = date.fromisoformat(when[:10])
    if isinstance(when, datetime):
        when = when.date()
    markup = markdown.markdown(body.replace('<!-- more -->', ''), extensions=['extra', 'sane_lists', 'toc'])
    soup = BeautifulSoup(markup, 'html.parser')
    for image in soup.find_all('img'):
        src = image.get('src', '')
        if src.startswith('images/'):
            image['src'] = '../' + src
        image['loading'] = 'lazy'
        image['decoding'] = 'async'
    # Preserve internal links between original Markdown posts.
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not urlsplit(href).scheme and href.endswith('.md'):
            link['href'] = '../' + Path(href).stem + '/'
    categories = {str(c).lower() for c in meta.get('tags', meta.get('categories', []))}
    tags = []
    if categories & {'flying', 'aviation', 'flight simulator', 'kdpa', 'gear'}:
        tags.append('aviation')
    if categories & {'psychology', 'iopsychology', 'i/o psychology'}:
        tags.append('psychology')
    if categories & {'programming', 'ai/llm'}:
        tags.append('programming')
    posts.append(dict(slug=path.stem, title=meta['title'], date=when, tags=tags,
                      description=meta.get('description', ''), body=str(soup)))
posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
(ROOT / 'blog').mkdir(exist_ok=True)
(ROOT / 'posts').mkdir(exist_ok=True)
shutil.copytree(SOURCE / 'images', ROOT / 'posts/images', dirs_exist_ok=True)
for index, post in enumerate(posts):
    title = escape(post['title'])
    stamp = f'<time datetime="{post["date"].isoformat()}">{post["date"].strftime("%B %d, %Y").replace(" 0", " ")}</time>'
    adjacent = []
    if index + 1 < len(posts):
        older = posts[index + 1]
        adjacent.append(f'<a href="../{older["slug"]}/"><span>Older post</span>{escape(older["title"])}</a>')
    if index:
        newer = posts[index - 1]
        adjacent.append(f'<a href="../{newer["slug"]}/"><span>Newer post</span>{escape(newer["title"])}</a>')
    tags = ''.join(f'<a class="post-tag" href="../../blog/?tag={tag}">{tag.title()}</a>' for tag in post['tags'])
    content = f'<article class="blog-article"><header class="article-heading"><a class="back-link" href="../../blog/">All posts</a><h1>{title}</h1>{stamp}<div class="post-tags">{tags}</div></header><div class="article-body">{post["body"]}</div><nav class="post-pagination" aria-label="More posts">{"".join(adjacent)}</nav></article>'
    target = ROOT / 'posts' / post['slug']
    target.mkdir(exist_ok=True)
    (target / 'index.html').write_text(page(post['title'], post['description'], content, '../../'))
filters = ''.join(f'<button type="button" data-filter="{tag}" aria-pressed="{str(tag == "all").lower()}">{tag.title()} <span>{sum(tag == "all" or tag in p["tags"] for p in posts)}</span></button>' for tag in ['all', 'aviation', 'psychology', 'programming'])
rows = [f'<section class="blog-index" aria-labelledby="blog-title"><div class="blog-heading"><h1 id="blog-title">Blog</h1><p>Writing on aviation, psychology, and data.</p><div class="blog-filters" role="group" aria-label="Filter posts by topic">{filters}</div><p class="filter-status" role="status" aria-live="polite">{len(posts)} posts</p></div>']
year = None
for post in posts:
    if post['date'].year != year:
        if year is not None:
            rows.append('</div></section>')
        year = post['date'].year
        rows.append(f'<section class="blog-year"><h2>{year}</h2><div>')
    tags = ''.join(f'<a class="post-tag" href="?tag={tag}" data-tag="{tag}">{tag.title()}</a>' for tag in post['tags'])
    rows.append(f'<article class="blog-entry" data-tags="{" ".join(post["tags"])}"><a href="../posts/{post["slug"]}/"><h3>{escape(post["title"])}</h3><p>{escape(post["description"])}</p></a><div class="post-tags">{tags}</div><time datetime="{post["date"].isoformat()}">{post["date"].strftime("%b %d").replace(" 0", " ")}</time></article>')
rows.append('</div></section></section>')
archive = page('Blog', 'Writing by Robert W. Szarek on aviation, psychology, and data.', ''.join(rows), '../')
archive = archive.replace('</body>', '<script src="../blog.js"></script></body>')
(ROOT / 'blog/index.html').write_text(archive)
# Check every migrated local image and same-site link.
missing = []
for path in [ROOT / 'blog/index.html', *(ROOT / 'posts').glob('*/index.html')]:
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    for tag in soup.find_all(['img', 'a', 'link']):
        url = tag.get('src') or tag.get('href', '')
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (path.parent / parts.path).resolve()
        if not target.exists():
            missing.append(f'{path.relative_to(ROOT)}: {url}')
if missing:
    raise RuntimeError('\n'.join(missing))
print(f'Migrated {len(posts)} posts ({posts[-1]["date"].year}–{posts[0]["date"].year}); verified all local images and links.')
