from qiskit.providers import BackendV2
from qiskit.transpiler import Target
from qiskit.providers import Options
from qiskit.circuit import Parameter, Measure
from qiskit.circuit.library import PhaseGate, SXGate, UGate, CXGate, IGate
from qiskit import assemble
from qiskit_aer import AerSimulator
from qiskit_han.job import MyJob
import warnings
import json


class HanBackend(BackendV2):

    def __init__(self):
        super().__init__()
        
        self.name = "HanBackend"
        # Create Target
        self._target = Target("Target for My Backend")
        # Instead of None for this and below instructions you can define
        # a qiskit.transpiler.InstructionProperties object to define properties
        # for an instruction.
        lam = Parameter("λ")
        p_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(PhaseGate(lam), p_props)
        sx_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(SXGate(), sx_props)
        phi = Parameter("φ")
        theta = Parameter("ϴ")
        u_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(UGate(theta, phi, lam), u_props)
        cx_props = {edge: None for edge in [(0, 1), (1, 2), (2, 3), (3, 4)]}
        self._target.add_instruction(CXGate(), cx_props)
        meas_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(Measure(), meas_props)
        id_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(IGate(), id_props)

        # Set option validators
        self.options.set_validator("shots", (1, 4096))
        self.options.set_validator("memory", bool)

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return 1024

    @classmethod
    def _default_options(cls):
        return Options(shots=1024, memory=False)

    def run(self, circuit, **kwargs):
        # serialize circuits submit to backend and create a job
        for kwarg in kwargs:
            if not hasattr(kwarg, self.options):
                warnings.warn("Option %s is not used by this backend" % kwarg)
        options = {
            'shots': kwargs.get('shots', self.options.shots),
            'memory': kwargs.get('memory', self.options.shots),
        }
        
        job = AerSimulator().run(circuit, shots=options['shots'], memory=options['memory'])
        
        return MyJob(self, job.job_id(), job.result())