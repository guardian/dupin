# Dupin

Dupin is a tool to help discover secrets in Git repositories.

## Installation

## Usage

Dupin creates a directory structure for storing its results as follows.

```bash
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
     ├── example-2.git
     └── example.git
```
