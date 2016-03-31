import unittest
from collections import defaultdict
from util import Message
from datastore import Datastore

class TestSingleMessages(unittest.TestCase):
    def test_valid_unusual_package_names(self):
        legal_messages = ['REMOVE|png++|\n', 'REMOVE|libxml++|\n', 'REMOVE|libsigc++|\n', 'REMOVE|mysql-connector-c++|\n']
        for message in legal_messages:
            self.assertEqual(str(Message.OK), Datastore().process_message(message))

    def test_invalid_messages(self):
        legal_messages = ['INDEX|cloog|gmp,isl,pkg-config\n', 'INDEX|ceylon|\n', 'REMOVE|cloog|\n', 'QUERY|cloog|\n']
        for message in legal_messages:
            self.assertEqual(str(Message.Error), Datastore().process_message(' ' + message))
            self.assertEqual(str(Message.Error), Datastore().process_message(message + ' '))
            self.assertEqual(str(Message.Error), Datastore().process_message(message[:-1]))
            print ('message', message[:-1] + ',' + message[-1:])
            self.assertEqual(str(Message.Error), Datastore().process_message(message[:-1] + ',' + message[-1:]))

    def test_index_already_exists(self):
        message = 'INDEX|cloog|gmp,isl,pkg-config\n'
        dependency_map = {'cloog':[], 'ceylon':['cloog']}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_index_with_unindexed_dependency(self):
        message = 'INDEX|cloog|gmp,isl,pkg-config\n'
        dependency_map = {'gmp':[], 'isl':['cmake']}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.Fail), datastore.process_message(message))

    def test_index_with_all_indexed_dependencies(self):
        message = 'INDEX|cloog|gmp,isl,pkg-config\n'
        dependency_map = {'gmp':[], 'isl':['cmake'], 'pkg-config':[]}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_index_with_no_dependencies(self):
        message = 'INDEX|ceylon|\n'
        dependency_map = {}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_remove_already_doesnt_exist(self):
        message = 'REMOVE|cloog|\n'
        dependency_map = {}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_remove_has_dependents(self):
        message = 'REMOVE|cloog|\n'
        dependency_map = {'gmp':['cloog', 'cmake'], 'cloog':[]}
        dependents_count = {'cloog':1, 'cmake':1}
        datastore = Datastore(dependency_map, dependents_count)
        self.assertEqual(str(Message.Fail), datastore.process_message(message))

    def test_remove_exists(self):
        message = 'REMOVE|cloog|\n'
        dependency_map = {'gmp':['cmake'], 'cloog':[]}
        dependents_count = {'cmake':1}
        datastore = Datastore(dependency_map, dependents_count)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_query_exists(self):
        message = 'QUERY|cloog|\n'
        dependency_map = {'gmp':['cmake'], 'cloog':[]}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.OK), datastore.process_message(message))

    def test_query_doesnt_exist(self):
        message = 'QUERY|cloog|\n'
        dependency_map = {'gmp':['cmake']}
        datastore = Datastore(dependency_map)
        self.assertEqual(str(Message.Fail), datastore.process_message(message))

if __name__ == '__main__':
    unittest.main()
