import yaml


class Config(object):
    github_token = None
    organisation_name = None
    notification_email = None

    def __init__(self, filename = None):
        if filename is not None:
            with open(filename, "r") as f:
                data = yaml.load(f)
                self.github_token = data.get("github_token", None)
                self.organisation_name = data.get("organisation_name", None)
                self.notification_email = data.get("notification_email", None)
