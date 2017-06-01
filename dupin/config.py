import yaml


class Config(object):
    github_token = None
    organisation_name = None
    notification_email = None

    smtp_host = None
    smtp_username = None
    smtp_password = None
    smtp_from = None

    source_file = None

    def __init__(self, filename = None):
        if filename is not None:
            self.source_file = filename
            with open(filename, "r") as f:
                data = yaml.load(f)
                self.github_token = data.get("github_token", None)
                self.organisation_name = data.get("organisation_name", None)
                self.notification_email = data.get("notification_email", None)

                self.smtp_host = data.get("smtp", {}).get("host", None)
                self.smtp_username = data.get("smtp", {}).get("username", None)
                self.smtp_password = data.get("smtp", {}).get("password", None)
                self.smtp_from = data.get("smtp", {}).get("from", None)

    def smtp_configured(self):
        return self.smtp_host is not None
