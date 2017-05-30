# Dupin

Dupin is a tool to help discover secrets in Git repositories.

## Installation

## Usage

Dupin creates a directory structure for storing its results as follows.

```
 root
 ├── repository-urls
 ├── repositories
 │   ├── example.git
 │   │   ├── ...etc contents of example repo
 │   │   └── .git
 │   └── example-2.git
 │       ├── ...etc contents of example-2 repo
 │       └── .git
 └── results
     ├── .git
     ├── example-2
     └── example
```

## Config

You can provide a config file to set some parameters for Dupin without
needing to pass them every time. This also lets you keep secrets away
from the git repository.
