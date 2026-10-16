#!/usr/bin/env python3
"""Save temporary Workshop Studio credentials outside the project."""
import configparser
import getpass
import os
from pathlib import Path


def main():
    values = {}
    for key, label in (
        ("aws_access_key_id", "AWS Access Key ID"),
        ("aws_secret_access_key", "AWS Secret Access Key"),
        ("aws_session_token", "AWS Session Token"),
    ):
        value = getpass.getpass(label + " (hidden): ").strip()
        if not value:
            raise SystemExit("All three credentials are required. Nothing saved.")
        values[key] = value

    directory = Path.home() / ".aws"
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / "credentials"
    config = configparser.RawConfigParser()
    if path.exists():
        config.read(path)
    if not config.has_section("hackathon"):
        config.add_section("hackathon")
    for key, value in values.items():
        config.set("hackathon", key, value)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(descriptor, 0o600)
    with os.fdopen(descriptor, "w") as output:
        config.write(output)
    print("Saved credentials to ~/.aws/credentials under [hackathon].")


if __name__ == "__main__":
    main()
