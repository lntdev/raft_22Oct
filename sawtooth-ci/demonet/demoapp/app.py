import argparse
import sys
import yaml

import aiohttp_jinja2
from aiohttp import web
import jinja2

import router
import database


def main(args=sys.argv[1:]):
    args = parse_args(args)

    db = database.create(args.reset)

    routes = router.Router(db)

    app = web.Application()
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader(router.TEMPLATE_DIR))

    app.router.add_get('/', routes.get_dashboard)
    app.router.add_get('/query', routes.get_query)
    app.router.add_post('/log', routes.post_json)
    app.router.add_get('/export', routes.get_export)
    app.router.add_get('/tags', routes.get_tags)

    web.run_app(app, host=args.host, port=args.port)
    
    print("Closing database...", end="")
    db.close()    
    print("closed.")
    

def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("--reset", action="store_true", default=False)
    return parser.parse_args(args)
