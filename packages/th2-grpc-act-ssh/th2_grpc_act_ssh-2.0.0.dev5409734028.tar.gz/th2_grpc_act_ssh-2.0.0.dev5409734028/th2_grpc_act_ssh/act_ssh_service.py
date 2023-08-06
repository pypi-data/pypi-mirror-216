from . import act_ssh_pb2_grpc as importStub

class ActSshService(object):

    def __init__(self, router):
        self.connector = router.get_connection(ActSshService, importStub.ActSshStub)

    def execute(self, request, timeout=None, properties=None):
        return self.connector.create_request('execute', request, timeout, properties)