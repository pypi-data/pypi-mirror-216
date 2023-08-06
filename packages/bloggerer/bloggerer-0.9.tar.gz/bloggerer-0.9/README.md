# Bloggerer: Markdown (and other things, probably) sprucer upperer

`bloggerer` is a very thin wrapper around a panflute-based Pandoc filter script
that does some preprocessing magic for publishing things as (generally) HTML.
I have mainly used it for generating better-looking and more functional HTML
than WordPress' own Markdown handling, but also for some other quality-of-life
features.

## Usage

```
$ bloggerer path/to/post.md
```

The resulting HTML will be located in `path/to/post.md.html` and can be copied
into a WordPress "Custom HTML" block.

## Features

* Handles footnotes properly
* Proper code-block formatting and syntax highlighting
    * Handled by [`highlight`](<https://gitlab.com/saalen/highlight>)
* Support for inline images
    * WordPress incorrectly considers `data:` URIs to be dangerous in `<img>`
      and CSS `url()`s, `bloggerer` gets around that. (Working in prod for 3+
      years. Caveat emptor, this causes the HTML to blow up and you may run
      into WordPress' or other blogging systems' character limits.)

## Installation

### Prerequisites

```
$ sudo apt-get install pandoc highlight
```

***Note:*** If your distro has an older version of pandoc (e.g. 2.9.x), get it from <https://github.com/jgm/pandoc/releases/>.

```
$ wget https://github.com/jgm/pandoc/releases/download/<ver>/pandoc-<...>.deb
$ sudo dpkg -i ./pandoc-*.deb
```

### Install

```
$ pip3 install --user bloggerer
```

### From Source

```
$ git clone https://github.com/ChaosData/bloggerer && cd bloggerer
$ python3 -m pip install --user --upgrade pip setuptools
$ python3 -m pip install --user .
```

### Packaging

```
$ python3 -m pip install --user wheel build
$ python3 -m build --sdist --wheel .
$ python3 -m pip install --user dist/bloggerer-*.whl
```

### Cleaning

```
$ rm -rf ./build ./dist ./src/bloggerer.egg-info ./src/bloggerer/__pycache__
```

## FAQ

> Why is the first top level heading removed from the HTML?

The first top-level heading is typically the title, which handled by
WordPress or other blogging things.
