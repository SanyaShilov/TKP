import argparse

from aiohttp import web

from app import Application


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8001)
    return parser.parse_args()


def main():
    app = Application()
    args = parse_args()
    web.run_app(app, port=args.port)


if __name__ == '__main__':
    main()
