import time
import os

import aiohttp_jinja2
from aiohttp import web
import asyncio
from urllib.parse import parse_qs

import database

QUERY_TEMPLATE = "query.html.j2"
DASHBOARD_TEMPLATE = "dashboard.html.j2"
TAGLIST_TEMPLATE = "taglist.html.j2"
TEMPLATE_DIR = os.path.dirname(os.path.realpath(__file__))


class Router:
    def __init__(self, db):
        self._db = db

    @aiohttp_jinja2.template(QUERY_TEMPLATE)
    def get_query(self, request):
        query = parse_qs(request.rel_url.query_string)

        if 'network' in query:
            if len(query['network']) > 0:
                network = query['network'][0]
            else:
                network = ""

            limit = 10
            if 'limit' in query:
                if len(query['limit']) > 0:
                    try:
                        limit = int(query['limit'][0])
                    except BaseException:
                        pass

            print("Query for %s, limit %d" % (network, limit))
            return {
                "data": database.get_query(self._db, network, limit),
                "network": network,
            }

        else:
            return {
                "data": [],
                "network": "Unknown request.",
            }

    @aiohttp_jinja2.template(DASHBOARD_TEMPLATE)
    def get_dashboard(self, request):
        print("Get request received for dashboard...")

        dashboard = database.get_dashboard(self._db, ["bond", "mkt"])

        return dashboard

    @aiohttp_jinja2.template(TAGLIST_TEMPLATE)
    def get_tags(self, request):
        print("Get request received for tags...")

        taglist = database.list_tags(self._db)

        return {"tags": taglist}

    @asyncio.coroutine
    def post_json(self, request):
        print("Received /log...") 
        try:
            data = (yield from request.read()).decode()

            network, tag = database.post_log(self._db, data)

            return web.Response(text="Received message from {} tagged {}".format(network, tag))

        except BaseException:
            print("Failed.")
            return web.Response(text="Bad message received")

    @asyncio.coroutine
    def get_export(self, request):
        print("Received export request...") 
        query = parse_qs(request.rel_url.query_string)

        try:
            tag = query['tag'][0]
        except KeyError:
            print("Export failed because no tag specified")
            return web.Response(text="No tag given.")

        try:
            data = database.export_tag(self._db, tag)
        except BaseException:
            return web.Response(
                text="Could not export data for tag {}".format(tag)
            )

        return web.Response(
            text=data
        )
