import re
import logging
import threading
from collections import defaultdict
from util import Message, InputError

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')

class Datastore(object):
    def __init__(self, dependency_map = {}, dependents_count = defaultdict(int)):
        # TODO: achieve better performance via a reader-writer lock. any number of concurrent reads could be allowed, if no concurrent write is occurring.
        self.lock = threading.Lock()
        self.dependency_map = dependency_map
        self.dependents_count = dependents_count

    def parse_message(self, message):
        logging.debug('parse_message called with message ' + message)
        # TODO: improve regex to filter out non syntactially correct dependency lists
        match = re.match('(INDEX|REMOVE|QUERY)\|([+\w-]+)\|([,+\w-]*)\\n$', message)
        if not match:
            raise InputError(message)
        command, package, dependency_list = match.group(1), match.group(2), match.group(3).split(',')
        if dependency_list == ['']:
            dependency_list = []
        logging.debug('command: ' + command + ', package: ' + package + ', dependency_list: ' + str(dependency_list))
        # test for unnecessary existence of dependency_list
        if command in ['REMOVE', 'QUERY'] and dependency_list:
            raise InputError(message)
        # test for illegal comma syntax in dependency_list
        if command == 'INDEX' and dependency_list and '' in dependency_list:
            raise InputError(message)      
        return command, package, dependency_list

    def process_message(self, message):
        logging.debug('processing message ' + message)
        logging.debug('self.dependency_map' + str(self.dependency_map))
        logging.debug('self.dependents_count ' + str(self.dependents_count))
        try:
            command, package, dependency_list = self.parse_message(message)
        except InputError:
            return str(Message.Error)
        if 'INDEX' == command:
            return self.index_package(package, dependency_list)
        if 'REMOVE' == command:
            return self.remove_package(package, dependency_list)
        return self.query_package(package)

    def index_package(self, package, dependency_list):
        with self.lock:
            if package in self.dependency_map:
                return str(Message.OK)
            for dependency in dependency_list:
                if dependency not in self.dependency_map:
                    return str(Message.Fail)
            self.dependency_map[package] = dependency_list
            for dependency in dependency_list:
                self.dependents_count[dependency] += 1
            return str(Message.OK)

    def remove_package(self, package, dependency_list):
        with self.lock:
            if package not in self.dependency_map:
                return str(Message.OK)
            if package in self.dependents_count:
                return str(Message.Fail)
            for dependency in self.dependency_map[package]:
                if self.dependents_count[dependency] == 1:
                    del self.dependents_count[dependency]
                else:
                    self.dependents_count[dependency] -= 1
            del self.dependency_map[package]
            return str(Message.OK)

    def query_package(self, package):
        with self.lock:
            if package in self.dependency_map:
                return str(Message.OK)
            return str(Message.Fail)
