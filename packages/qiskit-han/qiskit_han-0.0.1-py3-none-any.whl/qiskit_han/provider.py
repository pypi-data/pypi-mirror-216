from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.providerutils import filter_backends

from backend import HanBackend

class MyProvider(Provider):

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        self.backends = [HanBackend()]

    def backends(self):
        return self.backends
    
    def get_backend(self, name=None, **kwargs):
        for backend in self.backends:
            if backend.name == name:
                return backend
              
        raise Exception("Backend not found")
       
