# -*- coding: utf8 -*-

# (c) 2009 Marcos Dione <mdione@grulic.org.ar>

from lalita import Plugin

class Ping(Plugin):

    def init(self, config):
        self.logger.debug("Init! config: %s", config)
        self.register(self.events.COMMAND, self.ping, ['ping'])

    def ping(self, user, channel, command):
        self.logger.debug("let's play ping pong with %s!" % user)
        self.say(channel, u"%s: pong" % user)

# end
