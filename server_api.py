#!/usr/bin/env python3.6
# pip3 install git+https://github.com/webpy/webpy#egg=web.py
import web
import json
from mutant import DNAExpert
import redis
import os
from configparser import ConfigParser
config = ConfigParser()

config_file = "stats.conf"
config.read(config_file)

r = redis.Redis(host=os.environ.get("REDIS") or config.get('REDIS', 'ip') or 'localhost', port=6379, db=0)
web.config.debug = False

urls = (
    '/mutant', 'Mutant',
    '/stats', 'Stats',
)
app = web.application(urls, globals())

dna_expert = DNAExpert()


class Mutant:

    def POST(self):
        data = web.data()
        data_json = json.loads(data)
        result = dna_expert.isMutant(data_json['dna'])
        r.set(data, int(0 if result == None else result))
        if result == False:
            raise web.Forbidden()
        elif result:
            return web.OK()
        else:
            return web.HTTPError('400 Bad Request')


class Stats:

    def GET(self):
        count_human_dna = 0
        count_mutant_dna = 0
        ratio = 0
        for key in r.keys():
            result = r.get(key)
            count_human_dna += not int(result)
            count_mutant_dna += int(result)
        if count_mutant_dna and count_human_dna:
           ratio = round(float(count_mutant_dna / count_human_dna), 2)
        return {
            'count_mutant_dna': count_mutant_dna,
            'count_human_dna': count_human_dna,
            'ratio': ratio
        }



class Controller(web.application):
    def run(self, port=8081, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


def run():
    app = Controller(urls, globals())
    port = os.environ.get("PORT")
    app.run(int(port) if port else 8081)


if __name__ == "__main__":
    run()

