# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import urllib.parse
from calendar import timegm
from datetime import datetime

import jwt
import requests
from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_date

logger = logging.getLogger(__name__)


def update_release_from_github(release, repo_api=None):
    if not repo_api:
        repo_api = release.repo.github_api
    if not release.git_tag:
        logger.info("Cannot update release, no git_tag specified")
        return
    ref = repo_api.ref("tags/{}".format(release.git_tag))
    if not ref:
        logger.info(
            "Cannot update release, ref tags/{} not found in Github".format(
                release.git_tag
            )
        )
        return
    gh_release = repo_api.release_by_tag_name(release.git_tag)
    release.status = "published"
    release.version_name = gh_release.name
    release.version_number = gh_release.name
    release.github_release = gh_release.html_url
    release.release_creation_date = gh_release.created_at
    release.created_from_commit = ref.object.sha
    sandbox_date = re.findall(
        r"^Sandbox orgs: (20[\d][\d]-[\d][\d]-[\d][\d])", gh_release.body
    )
    if sandbox_date:
        release.sandbox_push_date = parse_date(sandbox_date[0], "%Y-%m-%d")

    prod_date = re.findall(
        r"^Production orgs: (20[\d][\d]-[\d][\d]-[\d][\d])", gh_release.body
    )
    if prod_date:
        release.production_push_date = parse_date(prod_date[0], "%Y-%m-%d")

    package_version_id = re.findall(r"(04t[\w]{15,18})", gh_release.body)
    if package_version_id:
        release.package_version_id = package_version_id[0]

    trialforce_id = re.findall(r"^(0TT[\w]{15,18})", gh_release.body)
    if trialforce_id:
        release.trialforce_id = trialforce_id[0]

    return release


def send_release_webhook(project_config, release):
    if release is None or not settings.METACI_RELEASE_WEBHOOK_URL:
        return
    logger.info(
        f"Sending release webhook for {release} to {settings.METACI_RELEASE_WEBHOOK_URL}"
    )
    tag = release.git_tag
    payload = {
        "case_template_id": release.change_case_template.case_template_id,
        "package_name": project_config.project__package__name,
        "version": project_config.get_version_for_tag(tag),
        "release_url": f"{release.repo.url}/releases/tag/{urllib.parse.quote(tag)}",
    }
    token = jwt.encode(
        {
            "iss": settings.METACI_RELEASE_WEBHOOK_ISSUER,
            "exp": timegm(datetime.utcnow().utctimetuple()),
        },
        settings.METACI_RELEASE_WEBHOOK_AUTH_KEY,
        algorithm="HS256",
    )
    response = requests.post(
        settings.METACI_RELEASE_WEBHOOK_URL,
        json=payload,
        headers={"Authorization": f"Bearer {token.decode('latin1')}"},
    )
    result = response.json()
    if result["success"]:
        with transaction.atomic():
            case_id = result["id"]
            case_url = settings.METACI_CHANGE_CASE_URL_TEMPLATE.format(case_id=case_id)
            release.change_case_link = case_url
            release.save()
    else:
        raise Exception("\n".join(err["message"] for err in result["errors"]))
