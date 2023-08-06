import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

##################_____CIRCUITGATES_____##################
class Test_CircuitGates(unittest.TestCase):

    # CIRCUIT GATES
    def test_CircuitGates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        self.assertEqual(type(circuit).__name__, 'CircuitGates')

    # NOT LOGGED IN
    def test_CircuitFlow_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.CircuitGates()
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')

##################_____GET CIRCUIT BODY_____##################
class Test_GetCircuitBody(unittest.TestCase):

    # GET CIRCUIT BODY EMPTY
    def test_getCircuitBody_empty(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        circuitBody = circuit.getCircuitBody()

        self.assertIsInstance(circuitBody, list)
        self.assertEqual(circuitBody, [[]])


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY EMPTY
    def test_getParsedBody_empty(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        parsedBody = circuit.getParsedBody()

        self.assertIsInstance(parsedBody, str)
        self.assertEqual(parsedBody, 'circuit={"cols": [[]], "init": []}')


##################_____GET QUBIT STATES_____##################
class Test_GetQubitStates(unittest.TestCase):

    # GET QUBIT STATES EMPTY
    def test_getQubitStates_empty(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, [])
    
    # GET QUBIT STATES
    def test_getQubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['0', '0', '0'])


##################_____GET NUMBER OF QUBITS_____##################
class Test_GetNumberOfQubits(unittest.TestCase):

    # GET NUMBER OF QUBITS EMPTY
    def test_getNumberOfQubits_empty(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertIsInstance(numberOfQubits, int)
        self.assertEqual(numberOfQubits, 0)
    
    # GET NUMBER OF QUBITS
    def test_getNumberOfQubits(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertIsInstance(numberOfQubits, int)
        self.assertEqual(numberOfQubits, 3)


##################_____GET DEFAULT QUBIT STATE_____##################
class Test_GetDefaultQubitState(unittest.TestCase):

    # GET DEFAULT QUBIT STATE
    def test_getDefaultQubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertIsInstance(defaultQubitState, str)
        self.assertEqual(defaultQubitState, '0')


##################_____SET DEFAULT QUBIT STATE_____##################
class Test_SetDefaultQubitState(unittest.TestCase):

    # SET DEFAULT QUBIT STATE
    def test_setDefaultQubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        circuit.setDefaultQubitState('1')

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertIsInstance(defaultQubitState, str)
        self.assertEqual(defaultQubitState, '1')

    # SET DEFAULT STATE EXISTING CIRCUIT
    def test_setDefaultQubitState_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.setDefaultQubitState('1')
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['0', '1', '1'])
    
    # BAD ARGUMENT qubitState
    def test_setDefaultQubitState_badArgument_qubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState('state')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
    
    # BAD ARGUMENT TYPE qubitState
    def test_setDefaultQubitState_badArgumentType_qubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState(0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____INITIALIZE QUBIT STATES_____##################
class Test_InitializeQubitStates(unittest.TestCase):

    # INITIALIZE QUBIT STATES
    def test_initializeQubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        circuit.initializeQubitStates(['1', '1', '1'])

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['1', '1', '1'])

    # BAD ARGUMENT qubitStates
    def test_initializeQubitStates_badArgument_qubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', '1'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT qubitStates LIST
    def test_initializeQubitStates_badArgument_qubitStates_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', 'state'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE qubitStates
    def test_initializeQubitStates_badArgumentType_qubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates('states')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE qubitStates LIST
    def test_initializeQubitStates_badArgumentType_qubitStates_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        try:
            circuit.initializeQubitStates(['1', '1', 1])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()