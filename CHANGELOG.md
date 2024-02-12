# Changelog

All notable changes to this project will be documented in this file.

## 2024-02-12
- Moved website to Mkdocs Material + Cloudflare Pages (from Hugo + Netlify - old repository is [here](https://github.com/nathancatania/website-2020))
- Converted all posts leveraging Hugo-specific features to the equivalent Mkdocs Material feature:
    - Callouts -> Admonitions
    - Figure formatting
    - Front-matter tags
- Organized the posts directory by year to make it a little less chaotic.
- Moved all images to be served from a single 'assets' folder within directory corresponding to the post year.
- Updated Obsidian config to automatically manage attachments for the new directory structure using the Attachment Management plugin.