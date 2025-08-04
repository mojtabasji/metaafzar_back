from django.urls import path, include, re_path
from django.http import JsonResponse
from django.urls import URLResolver, ResolverMatch


def nothing_to_show(request):
    return JsonResponse({"message": "Nothing to show here. Please check the API documentation."}, status=404)


def endpoints_list(request):
#     get available endpoints from the django app
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





