"""Update locales."""
from pathlib import Path

import logging
import re
import requests
import subprocess


logging.basicConfig()
logger = logging.getLogger("i18n")
logger.setLevel(logging.DEBUG)


ISO_CODES_TEAM_REPO = "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main"

PATTERN = r"^[a-z]{2}.*"
domains = "collective.contact_behaviors"
cwd = Path.cwd()
target_path = Path(__file__).parent.parent.resolve()
locale_path = target_path / "locales"

i18ndude = cwd / "bin" / "i18ndude"
if not i18ndude.exists():
    i18ndude = cwd / "i18ndude"

# ignore node_modules files resulting in errors
excludes = '"*.html *json-schema*.xml"'


def _get_languages_folders():
    folders = [path for path in locale_path.glob("*") if path.is_dir()]
    language_folders = sorted(
        [path for path in folders if not path.name.startswith("_")],
        key=lambda item: item.name,
    )
    return language_folders


def _get_content_from_repo(path=""):
    url = f"{ISO_CODES_TEAM_REPO}/{path}"
    response = requests.get(url)
    if not response.status_code == 200:
        raise RuntimeError(f"Not possible to download {url}")
    return response.content


def _sync_iso_codes(domains=None):
    domains = domains if domains else ["iso_3166-1"]
    languages = _get_languages_folders()
    for domain in domains:
        logger.info(f"Synchronize {domain}")
        # Sync POT
        remote_path = f"{domain}/{domain}.pot"
        content = _get_content_from_repo(remote_path)
        local_path = locale_path / f"{domain}.pot"
        local_path.write_bytes(content)
        logger.info(f" - Synchronized {domain} POT")
        for language in languages:
            code = language.name
            remote_path = f"{domain}/{code}.po"
            content = _get_content_from_repo(remote_path)
            local_path = locale_path / code / "LC_MESSAGES" / f"{domain}.po"
            local_path.write_bytes(content)
            logger.info(f" - Synchronized {code} PO")


def locale_folder_setup(domain: str):
    languages = _get_languages_folders()
    for lang_folder in languages:
        lc_messages_path = lang_folder / "LC_MESSAGES"
        lang = lang_folder.name
        if lc_messages_path.exists():
            continue
        elif re.match(PATTERN, lang):
            lc_messages_path.mkdir()
            cmd = (
                f"msginit --locale={lang} "
                f"--input={locale_path}/{domain}.pot "
                f"--output={locale_path}/{lang}/LC_MESSAGES/{domain}.po"
            )
            subprocess.call(
                cmd,
                shell=True,
            )


def _rebuild(domain: str):
    cmd = (
        f"{i18ndude} rebuild-pot --pot {locale_path}/{domain}.pot "
        f"--exclude {excludes} "
        f"--create {domain} {target_path}"
    )
    subprocess.call(
        cmd,
        shell=True,
    )


def _sync(domain: str):
    for path in locale_path.glob("*/LC_MESSAGES/"):
        # Check if domain file exists
        domain_file = path / f"{domain}.po"
        if not domain_file.exists():
            # Create an empty file
            domain_file.write_text("")
    cmd = (
        f"{i18ndude} sync --pot {locale_path}/{domain}.pot "
        f"{locale_path}/*/LC_MESSAGES/{domain}.po"
    )
    subprocess.call(
        cmd,
        shell=True,
    )


def update_locale():
    all_domains = [path.name[:-4] for path in locale_path.glob("*.pot")]
    domains = [domain for domain in all_domains if domain.startswith("collective")]
    iso_domains = [domain for domain in all_domains if domain not in domains]
    if i18ndude.exists():
        for domain in domains:
            logger.info(f"Updating translations for {domain}")
            locale_folder_setup(domain)
            _rebuild(domain)
            _sync(domain)
        _sync_iso_codes(domains=iso_domains)
    else:
        logger.error("Not able to find i18ndude")
