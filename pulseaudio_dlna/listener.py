#!/usr/bin/python

# This file is part of pulseaudio-dlna.

# pulseaudio-dlna is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pulseaudio-dlna is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pulseaudio-dlna.  If not, see <http://www.gnu.org/licenses/>.

import SocketServer
import socket
import struct


class SSDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        packet = self.request[0]
        lines = packet.splitlines()
        if len(lines) > 0 and self._is_notify_method(lines[0]):
            self.server.renderers_holder.process_notify_request(packet)

    def _is_notify_method(self, method_header):
        method = self._get_method(method_header)
        return method == 'NOTIFY'

    def _get_method(self, method_header):
        return method_header.split(' ')[0]


class SSDPListener(SocketServer.UDPServer):
    def __init__(self, renderers_holder):
        SocketServer.UDPServer.__init__(self, ('', 1900), SSDPRequestHandler)
        multicast = struct.pack("=4sl", socket.inet_aton("239.255.255.250"), socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast)
        self.renderers_holder = renderers_holder
