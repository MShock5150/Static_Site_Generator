# Static Site Generator in Python

**Live Site:** [https://mshock5150.github.io/Static_Site_Generator/](https://mshock5150.github.io/Static_Site_Generator/)

## Project Overview

This project is a fully functional Static Site Generator (SSG) built from scratch in Python. The program takes a directory of content written in Markdown, combines it with HTML templates, and generates a complete, static website ready for deployment.

The primary goal of this project was to develop a deep, foundational understanding of data structures, algorithms, and software design principles by building a real-world application without relying on external libraries for the core logic. Every component, from the markdown parser to the recursive file handlers, was implemented manually.

## Key Features

* **Markdown to HTML Conversion:** A robust engine that parses block-level and inline Markdown syntax and converts it to semantic HTML.
    * **Block-Level Parsing:** Correctly identifies and converts headings, paragraphs, code blocks, blockquotes, and both ordered and unordered lists.
    * **Inline Parsing:** Handles bold, italic, code, links, and images within text blocks.
* **Recursive File Processing:** Implements recursive algorithms to intelligently process nested file structures.
    * Recursively copies all static assets (CSS, images) from a source directory to the output directory.
    * Recursively discovers all content files in a source directory and generates a corresponding HTML file structure.
* **Templating System:** Utilizes a simple yet effective templating system to inject generated content and page titles into a master HTML template, ensuring a consistent site layout.
* **Configurable Build Process:** The build script accepts a `basepath` argument, allowing all generated URLs to be correctly prefixed for deployment to subdirectories, such as on GitHub Pages.
* **Comprehensive Unit Testing:** The project is supported by a thorough suite of unit tests created with Python's `unittest` framework, ensuring the reliability and correctness of each component.

## How It Works

The generation process is orchestrated by the main script and follows these steps:

1.  The destination `docs/` directory is cleaned to ensure a fresh build.
2.  All static assets from the `static/` directory are recursively copied to `docs/`.
3.  The `content/` directory is recursively scanned for `.md` files.
4.  For each Markdown file found:
    * The `h1` title is extracted.
    * The Markdown content is parsed into an abstract syntax tree of custom `HTMLNode` objects.
    * This node tree is rendered into a final HTML string.
5.  The generated title and HTML content are injected into `template.html`.
6.  The final HTML page is written to the corresponding path in the `docs/` directory.

## How to Run

### For Local Development

This will build the site with a root base path (`/`) and start a local server.

```bash
./main.sh
```

The site will be available at `http://localhost:8888`.

### For Production Build (GitHub Pages)

This will build the site with the correct base path for deployment.

```bash
./build.sh
```

This generates the final site in the `docs/` directory, which can then be committed and pushed to GitHub.

## Using as a Template for a New Site

This repository can be used as a template to generate new static websites. The process involves cloning the project, cleaning out the old content, and then connecting it to a new GitHub repository for the new site.

### 1. Create the New Project Locally

Clone this repository into a new folder for your new project.

```bash
git clone [https://github.com/MShock5150/Static_Site_Generator.git](https://github.com/MShock5150/Static_Site_Generator.git) new-project-name
cd new-project-name
```

### 2. Clean the Project Directories

Remove the old content and static files to prepare the project for your new site. The build script will automatically handle the output directory (`docs/`).

```bash
rm -rf content/*
rm -rf static/*
```

### 3. Connect to a New GitHub Repository

First, create a new, empty repository on GitHub for your new project (e.g., `new-site-repo`).

Next, remove the old remote link and connect your local project to the new repository.

```bash
# Remove the link to the original SSG repository
git remote remove origin

# Add the link to your new repository
git remote add origin [https://github.com/YOUR_USERNAME/new-site-repo.git](https://github.com/YOUR_USERNAME/new-site-repo.git)
```

### 4. Commit and Push

Finally, commit the clean project structure and push it to your new repository to establish the connection.

```bash
git add .
git commit -m "Initial commit: Set up SSG for new site"
git push -u origin main
```

You now have an independent project for your new website, powered by this static site generator.

---

*This site was generated with a custom-built static site generator from the course on [Boot.dev](https://www.boot.dev).*

