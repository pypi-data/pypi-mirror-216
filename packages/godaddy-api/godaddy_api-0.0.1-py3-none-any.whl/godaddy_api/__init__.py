# SPDX-FileCopyrightText: 2023-present Filip Strajnar <filip.strajnar@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

import os
from typing import Union


def get_api_key() -> Union[str, None]:
    return os.getenv("GODADDY_API_KEY")


def get_api_secret() -> Union[str, None]:
    return os.getenv("GODADDY_API_SECRET")


def get_api_url() -> str:
    url_env = os.getenv("GODADDY_API_URL")
    if url_env == None:
        return "https://api.godaddy.com/"

    assert url_env.startswith("https")

    return url_env if url_env.endswith("/") else f"{url_env}/"
