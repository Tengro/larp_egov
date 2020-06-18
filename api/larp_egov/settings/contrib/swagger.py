from ..environment import env


SWAGGER_SETTINGS = {
    "DEFAULT_API_URL": env.str("LARP_EGOV_BASE_API_URL", default="https://atom-egov.xyz"),
}
