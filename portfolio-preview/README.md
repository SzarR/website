# Personal portfolio rebuild

Work in progress for [issue #2](https://github.com/SzarR/website/issues/2). This directory contains the reviewed portfolio prototype and migrated blog. Existing MkDocs production files are unchanged.

## Preview

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory portfolio-preview
```

Open http://127.0.0.1:8080/. No JavaScript build step is required. Google Fonts requires an internet connection; system fallbacks are included.

## Blog

All 36 original published posts are preserved in `content/posts`, including images and YAML metadata. Generated reading pages retain the original `/posts/<slug>/` URLs. The archive supports Aviation, Psychology, and Programming filters, based on the original categories; posts may have multiple tags.

After changing the homepage header/footer or blog Markdown, regenerate the blog:

```sh
python3 -m venv /tmp/rws-blog-env
/tmp/rws-blog-env/bin/pip install -r portfolio-preview/scripts/requirements.txt
/tmp/rws-blog-env/bin/python portfolio-preview/scripts/build_blog.py
```

The generator checks local links and image paths. `blog.js` handles filtering, URL state, and browser back/forward navigation.

## Current design

- Dark theme on first visit; saved light/dark preference persists locally.
- Light background: RGB 240, 237, 226.
- Lowercase rws mark, Contact menu, and Blog navigation.
- Experience, project cards, and one research card using the supplied paper's title-page thumbnail.
- Flighty artwork is an editable SVG in `assets/flighty.svg`.
- Some project details and imagery remain placeholders; the résumé link still points to the existing résumé.
- Footer version v0.1; last updated November 23, 2026.

Nothing in this directory has been deployed. Root-level preview screenshots are intentionally excluded from version control.
