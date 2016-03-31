import re
from collections import defaultdict
from threading import Lock
from message import Message, MessageError

def parse_message(message):
    """Parse an incoming message and throw an MessageError if it is not correctly formatted."""
    # TODO: improve regex to filter out syntactially incorrect dependency lists (misplaced commas)
    match = re.match('(INDEX|REMOVE|QUERY)\|([+\w-]+)\|([,+\w-]*)\\n$', message)
    if not match:
        raise MessageError(message)
    command, package, dependency_list = match.group(1), match.group(2), match.group(3).split(',')
    if dependency_list == ['']:
        dependency_list = []
    # test for unnecessary existence of dependency_list
    if command in ['REMOVE', 'QUERY'] and dependency_list:
        raise MessageError(message)
    # test for illegal comma syntax in dependency_list
    if command == 'INDEX' and dependency_list and '' in dependency_list:
        raise MessageError(message)
    return command, package, dependency_list


class Datastore(object):
    """This class stores all indexed packages and their dependencies.

    Attributes:
        dependency_map      maps an indexed package to its dependencies (packages that need to be indexed before it is)
        dependents_count    maps an indexeded package to the number of packages that have it as a dependency
    """
    def __init__(self, dependency_map={}, dependents_count=defaultdict(int)):
        # TODO: achieve better performance via a reader-writer lock. any number of concurrent reads could be allowed, if no concurrent write is occurring.
        self.lock = Lock()
        self.dependency_map = dependency_map
        self.dependents_count = dependents_count

    def process_message(self, message):
        try:
            command, package, dependency_list = parse_message(message)
        except MessageError:
            return str(Message.Error)
        if command == 'INDEX':
            return self.index_package(package, dependency_list)
        if command == 'REMOVE':
            return self.remove_package(package)
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

    def remove_package(self, package):
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
