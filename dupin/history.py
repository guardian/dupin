import os
import re
import sys
from git import Repo

from emails import send_email_quick, send_email_properly
from pgp import parse_key, encrypt
from utils import printerr


def history(root, message, notify, config):
    results_dir = os.path.join(root, "results")
    repo = Repo(results_dir)
    repo.git.add(A=True)
    contents = repo.git.diff(cached=True)

    if contents:
        printerr("Changes to secrets detected")
        if notify:
            if config.notification_email:
                printerr("Notifying {address} of changes".format(address=config.notification_email))

                if config.pgp_key is None:
                    message = strip_ansi_sequences(contents)
                else:
                    pgp_key = parse_key(config.pgp_key)
                    unencrypted = strip_ansi_sequences(contents)
                    message = "Dupin findings encrypted using key '{identity}'\nFingerprint: {fingerprint}\n\n{data}"\
                        .format(identity=pgp_key.userids[0].name,
                                fingerprint=pgp_key.fingerprint,
                                data=encrypt(unencrypted, pgp_key))

                if config.smtp_configured():
                    send_email_properly(message, config.notification_email, config.smtp_from, config.smtp_host, config.smtp_username, config.smtp_password)
                else:
                    printerr("No SMTP configuration discovered, attempting to send email anyway")
                    send_email_quick(message, config.notification_email)
            else:
                printerr("Error: Missing notification email configuration")
                sys.exit(1)
        else:
            print(contents)
        printerr("Comitting log to repo at {location}".format(location=results_dir))
        repo.index.commit(message)
    else:
        printerr("No new secrets found")
    return

def strip_ansi_sequences(str):
    escape_seqs = re.compile(r'\x1b[^m]*m')
    return escape_seqs.sub('', str)
