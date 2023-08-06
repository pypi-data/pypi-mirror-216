from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.providerutils import filter_backends

from qiskit_han.backend import HanBackend
import warnings

class MyProvider(Provider):

    def __init__(self, token=None):
        super().__init__()
        self.token = token
        if token == None:
            raise Exception("Warning: No access token is provided.")
        
        self._backends = [HanBackend()]

    def backends(self):
        return self._backends
    
    def get_backend(self, name=None, **kwargs):
        for backend in self.backends:
            if backend.name == name:
                return backend
              
        raise Exception("Backend not found")
       
