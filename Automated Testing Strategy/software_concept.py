"""
Concept architecture for the NI USB-6000 automated testing framework.
"""

class Channel:                     # all channels of all types
    name: str
    divice: str
    def measure(backend, n_samples) -> "Data": ...
    def write(backend, value) -> None: ...


class AnalogChannel(Channel):
    input_range_v: tuple           # static
    sample_rate_hz: float          # static
    direction: "ChannelDirection"  # static


class DigitalChannel(Channel):
    supports_pfi: bool             # static
    sample_rate_hz: float          # static
    mode: "DigitalMode"            # state -> DI / DO active / DO open-collector / PFI
    def set_mode(backend, mode: "DigitalMode") -> None: ...


class DUT:
    serial_number: str             # static
    firmware_version: str          # state
    analog_channels: list[AnalogChannel]
    digital_channels: list[DigitalChannel]
    def connect(backend) -> None: ...
    def disconnect(backend) -> None: ...


class TestingInstrument:           # the PCIe-6738 card in the test bench
    analog_channels: list[AnalogChannel]      # e.g. AO channels driving stimulus onto the DUT's AI
    digital_channels: list[DigitalChannel]    # e.g. DO driving PFI0 pulses, DI reading the DUT's DO
    def connect() -> None: ...
    def disconnect() -> None: ...


class InstrumentBackend:           # hardware abstraction layer to talk to the DUT + reference instrument

    ...


class Data:
    source: str                    # which channel/instrument this came from, e.g. "DUT.AI0", "PCIe.AI3"
    timestamps: list[float]
    values: list                   # float for analog, bool for digital


class Analysis:
    metrics: dict                  # analysis of the data (fit results, caluclations, etc.)


class TestResult:
    test_name: str
    conditions: dict                # what set_conditions checked / applied
    data: list[Data]                # output of run_test
    analysis: Analysis              # output of analyze
    passed: bool                    # output of pass_test
    specs: dict                     # acceptance criteria
    log_file: str


class BaseTest:
    def set_conditions() -> dict: ... # set channel mode, check measurement conditions
    def run_test() -> list[Data]: ... # set output channels and collect data
    def analyze(data: list[Data]) -> Analysis: ... # analyze the data
    def pass_test(analysis: Analysis) -> tuple[bool, dict]: ...  # (passed, specs)
    def run() -> TestResult: ...             # runs the 4 above + logging


class TestSuite:
    tests: list[BaseTest]
    def run_all() -> list[TestResult]: ...


class ReportGenerator:
    def generate_report() -> ReportPdf: ...