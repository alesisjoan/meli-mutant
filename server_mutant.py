#!/usr/bin/env python3.6
# pip3 install git+https://github.com/webpy/webpy#egg=web.py
import web
import json
from mutant import DNAExpert
from mutant import helmet_ascii
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
web.config.debug = False

urls = (
    '/mutant', 'Mutant',
)
app = web.application(urls, globals())

dna_expert = DNAExpert()

print(helmet_ascii)


class Mutant:

    def POST(self):
        data = web.data()
        data_json = json.loads(data)
        result = dna_expert.isMutant(data_json['dna'])
        r.set(data, int(result))
        if result == False:
            raise web.Forbidden()
        elif result:
            return web.OK()
        else:
            return web.HTTPError()


class DNAExpertController(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


def run():
    app = DNAExpertController(urls, globals())
    app.run(port=8080)


if __name__ == "__main__":
    run()
