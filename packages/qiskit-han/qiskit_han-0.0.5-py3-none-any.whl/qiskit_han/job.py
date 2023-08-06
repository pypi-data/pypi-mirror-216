from qiskit.providers import JobV1 as Job
from qiskit.providers import JobError
from qiskit.providers import JobTimeoutError
from qiskit.providers.jobstatus import JobStatus
from qiskit.result import Result
import time


class MyJob(Job):

    def __init__(self, backend, job_id, result):
        super().__init__(backend, job_id)
        self._result = result

    def result(self):
        return self._result

    def status(self):
        return JobStatus.DONE