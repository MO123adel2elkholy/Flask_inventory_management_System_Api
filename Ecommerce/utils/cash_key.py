# categroies Key
from flask import request

from Ecommerce.apps import cache


def categoriess_cache_key():
    return "categories_list"


def categories_cache_keies():
    version = cache.get("categories_version") or 1

    return (
        f"cat:{version}:"
        f"{request.args.get('page', 1)}:"
        f"{request.args.get('per_page', 10)}:"
        f"{request.args.get('search', '')}:"
        f"{request.args.get('sort_by', 'id')}:"
        f"{request.args.get('order', 'asc')}"
    )


def invalidate_categories_cache():
    version = cache.get("categories_version") or 1
    cache.set("categories_version", version + 1)
