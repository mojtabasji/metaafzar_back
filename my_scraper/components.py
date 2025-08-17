from django.urls import path, include, re_path
from django.http import JsonResponse
from django.urls import URLResolver, ResolverMatch
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def nothing_to_show(request):
    return JsonResponse({"message": "Nothing to show here. Please check the API documentation."}, status=404)


def endpoints_list(request):
    # get available endpoints from the django app
    apis_list = []
    for urlconf in [include('my_scraper.urls')]:
        if isinstance(urlconf, URLResolver):
            for pattern in urlconf.url_patterns:
                if isinstance(pattern, URLResolver):
                    for sub_pattern in pattern.url_patterns:
                        if isinstance(sub_pattern, ResolverMatch):
                            apis_list.append({
                                "name": sub_pattern.name,
                                "path": str(sub_pattern.pattern),
                                "methods": sub_pattern.callback.cls.http_method_names if hasattr(sub_pattern.callback, 'cls') else [],
                            })
                elif isinstance(pattern, ResolverMatch):
                    apis_list.append({
                        "name": pattern.name,
                        "path": str(pattern.pattern),
                        "methods": pattern.callback.cls.http_method_names if hasattr(pattern.callback, 'cls') else [],
                    })
    return JsonResponse({"endpoints": apis_list}, status=200)


# instagram business login: Exchange the Code For a Token
def code2token(code, user):
    logger.info(f"Exchanging code for token for user: {user}")
    request_url = "https://api.instagram.com/oauth/access_token "
    payload = {
        'client_id': settings.MY_ENVS.IG_CLIENT_ID,
        'client_secret': settings.MY_ENVS.IG_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.MY_ENVS.IG_REDIRECT_URI,
        'code': code
    }
    logger.debug(f"Payload: {payload}")
    response = requests.post(request_url, data=payload)
    logger.debug(f"Response status: {response.status_code}")
    logger.debug(f"Response data: {response.text}")
    if response.status_code == 200:
        logger.info("Token exchange successful")
        return response.json()
    else:
        logger.error(f"Failed to exchange code for token: {response.text}")
        return {"error": "Failed to exchange code for token", "status_code": response.status_code}


