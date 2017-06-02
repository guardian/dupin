# Dupin

> But it is in matters beyond the limits of mere rule that
> the skill of the analyst is evinced. He makes in silence
> a host of observations and inferences....
>
> — Edgar Allan Poe, The Murders in the Rue Morgue

Dupin is a tool to help discover secrets in Git repositories.

It is designed to be used as a tool for regularly scanning an
organisation's public Git repositories, notifying a nominated
email address when it finds anything that looks suspicious.

### Quickstart

Install Dupin from source with `pip install <path-to-dupin>`.
(`virtualenv` is recommended)

For these examples we'll use `~/.dupin` as our root directory,
you can use anything that makes sense for you.

```bash
ROOT=~/.dupin
# sets up a directory for Dupin to store its repositories and results
dupin setup --root $ROOT

# stores a list of your organisation's public repos
dupin update-repos --root $ROOT organisation-name
# if you get rate limit errors you'll need to provide a Github
# token with the --token argument

# scan all repositories in the list for secrets, logs and shows results
dupin auto-scan-all --root $ROOT
# this logs what it finds in the $ROOT/results directory and the
# details to the console
# it's also possible to email reports, more details below and in the
# config section
```

## Installation

Dupin is an installable package Python package, but is not hosted in
public Python repositories. You can clone the source code and then
use `pip` to install Dupin. This will also install its dependencies.

As ever, it's better to install Dupin into a virtual environment.
This prevents Dupin's dependencies from creating problems with other
Python software on your machine.

```bash
git clone git@github.com:guardian/dupin.git

# via a virtualenv, or globally (may require sudo)
pip install dupin
```

You should then be able to run `dupin`.

### AWS

This repository includes a [CloudFormation template](cloudformation/dupin.template.yaml)
which creates an EC2 instance that runs Dupin on a schedule. If you
have an AWS account this is the easiest way to run Dupin.

## Usage

Dupin offers several commands. Check the [program's main file](dupin/dupin.py)
for full info, the main commands are described below.

**Note:** many of these commands interact with Dupin's directory
structure. More information about the layout Dupin uses to store
data is available below, in the [Directory structure](#directory-structure)
section.

### Global arguments

These arguments apply to many/all of Dupin's commands.

#### `--root`

Sets the root directory for Dupin's directory structure.

#### `--config`

By default, this is read from `ROOT/config` if a root is provided.

You may instead provide a custom location. This should point to a
`yaml` file that contains Dupin's config.

### setup

The setup command initialises Dupin's directory structure. If you're
using any of the features Dupin offers that depend on the data it has
stored (likely) you'll need to run this command first.

Examples:

```bash
duping setup --root ~/.dupin
```

### update-repos

This command looks up an organisation's public repositories on Github
and writes them to a file.

Examples:


```bash
# provide args via a config file at ~/.dupin/config
dupin update-repos --root ~/.dupin
```
```bash
# provide args explicitly
dupin update-repos myorg --token abcdef
```
```bash
# save the list of repositories in a provided location
dupin update-repos --file /tmp/organisation-repos.txt
```

#### `--file`

By default it writes to `ROOT/repository-urls` (you'll need to provide
a `--root` argument to take advantage of this). You can specify an
alternative file.

### auto-scan-all

This command scans all the repositories it finds in `ROOT/repository-urls`
for secrets, and saves its findings. It will also generate a diff of
these findings compared to the previous version and display this diff
for the user. This makes it easy to spot when secrets have been
introduced (or [removed](https://rtyley.github.io/bfg-repo-cleaner/)).

If you provide the `--notify` flag, Dupin will read the provided
configuration and email the changes in its findings.

**NOTE:** Emailing secrets is a silly idea so Dupin supports PGP
encryption of its notification emails. To enable this feature simply
provide a PGP Public Key in the configuration (read [the config section](#PGP-key)
for more info)

Examples:

```bash
# scans and prints changes to the console
dupin --root ~/.dupin auto-scan-all
```
```bash
# instruct Dupin to send notification emails (requires config)
dupin --root ~/.dupin auto-scan-all --notify
```

#### --notify

This flag tells Dupin to send notification emails. Doing so will
require additional configuration. Since this configuration is
non-trivial, you should provide it in a config file, rather than as
arguments to Dupin.

More information on configuring Dupin for sending email is available
below, under [Configuration](#Configuration), specifically [SMTP](#SMTP)

## Directory structure

Dupin creates a directory structure for storing its results as follows.

```
 root
 ├── config
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

### config

You may provide a config file that saves passing lots of arguments to
all of Dupin's commands. By default, Dupin looks in `ROOT/config` for
this file.

### repository-urls

This file contains a list of repository URLs, one per line. This is what
Dupin uses to determine what to scan.

You can edit the list yourself, or generate it using Dupin's
`update-repos` command.

### repositories

This is where Dupin stores a local copy of the repositories it scans.
If Dupin finds a new repository while scanning it will clone a copy to
this location. If the repo already exists it will update it before
scanning.

### results

The results directory is a Git repository that contains the history of
Dupin's scans. This is also used to determine changes since when
notifying Dupin emails details of changes.

## Configuration

You can provide a config file to set some parameters for Dupin without
needing to pass them every time. This also lets you keep secrets away
from the git repository.

If you provide a `--root` argument to Dupin it will attempt to read the
config from a file in that root called `config`. Alternatively, you can
specify the config file location with the `--config` argument.

```
 root
 ├── config       <- default location for config
 ├── repository-urls
 ├── repositories
 │   └── ...etc
 └── results
     └── ...etc
```

Here's an example configuration file. The file should be written using
YAML. Look at [config.py](dupin/config.py) for more info about how this
works. 

```yaml
github_token: xxxxxxxx-github-token-xxxxxxxx
organisation_name: your-organisation
notification_email: recipient@example.com
smtp:
  host: smtp-server.example.com
  from: sender@example.com
  username: username
  password: password
pgp_key: |
  -----BEGIN PGP PUBLIC KEY BLOCK-----
  Version: GnuPG v1
  
  abdefghihjklmnopqrstuvwxyz...etc
  ...etc
  ...etc
```

Most of these setting can be provided as arguments to Dupin instead of
as configuration, but it's generally simpler and safer to put them in
a config file. In particular, the `auto-scan-all` reads its arguments
from the configuration for simplicity and the SMTP settings can only be
provided from config.

### Github token

This is used when Dupin fetches the list of organisation repositories.
Dupin searches public repositories so in theory this token isn't
required. In practice, if your organisation has a large number of
repositories you'll hit Github's rate limit while Dupin runs through
the pagination. If this happens you'll need to provide authentication
so you are given a higher rate limit.

### Organisation name

This tells Dupin which organisation to use when it creates its list of
repositories that should be scanned.

### Notification email

Dupin uses this as a "to" address when it emails updates to your
organisation's secrets.

### SMTP

If no SMTP host is provided, Dupin will attempt to send an email using
`localhost`. If your machine does't have a mail server running locally
this will fail. Even if it does, you're probably better off using a real
mailserver. The following settings allow you to configure the way Dupin
sends emails.

#### Host

The hostname of the SMTP server to use.

#### From

Tells Dupin what to use as the "from" address for notification emails.

#### Username & password

These settings are used to authenticate the SMTP connection. You'll get
these when you configure your mailserver.

### PGP key

Sending sensitive secrets over email is a silly idea. To deal with this,
Dupin supports PGP encryption of the email contents.

You should provide a PGP public key as text. YAML supports multi-line
strings using the `|` character like in the example above. Make sure
the key is consistently indented. 

If you are using GnuPG you can obtain the public key in the correct
format using the following command. Other PGP applications will offer
similar functionality for exporting public keys.

```bash
gpg --armor --export <identity/email>
```

If you provide a PGP key in the configuration, PGP encryption will be
automatically enabled.
