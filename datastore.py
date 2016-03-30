import re
from collections import defaultdict
from util import Message, InputError

# self.dependency_map = {}
# self.dependents_count = defaultdict(int)

class Datastore(object):
    def __init__(self, dependency_map = {}, dependents_count = defaultdict(int)):
        self.dependency_map = dependency_map
        self.dependents_count = dependents_count
        print ('datastore __init__ called')

    # def set_self.dependency_map(self.dependency_map):
    #     self.dependency_map = self.dependency_map

    # def set_self.dependents_count(self.dependents_count):
    #     self.dependents_count = self.dependents_count

    def parse_message(self, message):
        print ('parse_message called with message', message)
        match = re.match('(INDEX|REMOVE|QUERY)\|([\w-]+)\|([,\w-]*)\\n$', message)
        if not match:
            raise InputError(message)
        command, package, dependency_list = match.group(1), match.group(2), match.group(3).split(',')
        if dependency_list == ['']:
            dependency_list = []
        # print ('command:', command, 'package:', package, 'dependency_list:', dependency_list)
        # test for unnecessary dependency_list
        if command in ['REMOVE', 'QUERY'] and dependency_list:
            raise InputError(message)
        # test for illegal comma syntax in dependency_list
        if command == 'INDEX' and dependency_list and '' in dependency_list: # TODO: replace with better regex
            raise InputError(message)      
        return command, package, dependency_list

    def process_message(self, message):
        # print ('processing message', message)
        # print ('self.dependency_map', self.dependency_map)
        # print ('self.dependents_count', self.dependents_count)
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
        # print ('dependency_map', self.dependency_map, 'dependents_count', self.dependents_count)
        if package not in self.dependency_map:
            return str(Message.OK)
        if package in self.dependents_count:
            return str(Message.Fail)
        del self.dependency_map[package] # TODO: tackle concurrent access by multiple clients to data store
        return str(Message.OK)

    def query_package(self, package):
        if package in self.dependency_map:
            return str(Message.OK)
        return str(Message.Fail)
