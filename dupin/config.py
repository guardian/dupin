import yaml


class Config(object):
    github_token = None
    organisation_name = None
    notification_email = None
    repo_exclusions = None
    include_forks = None

    smtp_host = None
    smtp_username = None
    smtp_password = None
    smtp_from = None

    pgp_key = None

    source_file = None

    def __init__(self, filename = None):
        if filename is not None:
            self.source_file = filename
            with open(filename, "r") as f:
                data = yaml.load(f)
                self.github_token = data.get("github_token", None)
                self.organisation_name = data.get("organisation_name", None)
                self.notification_email = data.get("notification_email", None)
                self.repo_exclusions = data.get("repo_exclusions", None)
                self.include_forks = data.get("include_forks", None)

                self.smtp_host = data.get("smtp", {}).get("host", None)
                self.smtp_username = data.get("smtp", {}).get("username", None)
                self.smtp_password = data.get("smtp", {}).get("password", None)
                self.smtp_from = data.get("smtp", {}).get("from", None)

                self.pgp_key = data.get("pgp_key", None)

    def smtp_configured(self):
        return self.smtp_host is not None
