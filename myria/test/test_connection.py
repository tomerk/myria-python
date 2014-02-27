from httmock import urlmatch, HTTMock
import json
import unittest
from myria import MyriaConnection


@urlmatch(netloc=r'localhost:8753', path="/workers")
def worker_mock(url, request):
    return json.dumps({'1': 'localhost:9001', '2': 'localhost:9002'})


class TestDeployment(unittest.TestCase):
    def test_no_deployment(self):
        assert MyriaConnection._parse_deployment(None) is None

    def test_deployment_file(self):
        with open('myria/test/deployment.cfg.local') as deploy_file:
            hostname, port = MyriaConnection._parse_deployment(deploy_file)
            self.assertEqual(hostname, 'localhost')
            self.assertEqual(port, 8753)

    def test_deploy_local(self):
        with HTTMock(worker_mock):
            with open('myria/test/deployment.cfg.local') as deploy_file:
                connection = MyriaConnection(deploy_file)
            assert connection is not None

            self.assertEquals(connection.workers(),
                              {'1': 'localhost:9001', '2': 'localhost:9002'})
