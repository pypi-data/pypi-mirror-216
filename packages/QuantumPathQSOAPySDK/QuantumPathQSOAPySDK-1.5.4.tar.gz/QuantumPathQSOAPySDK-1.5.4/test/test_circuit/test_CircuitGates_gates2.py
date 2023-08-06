import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


##################_____CCX_____##################
class Test_CCX(unittest.TestCase):

    # CCX position 0, 1, 2
    def test_ccx_position_0_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'X']])

    # CCX position 0, 1, 3
    def test_ccx_position_0_1_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 1, 'X']])

    # CCX position 1, 2, 3
    def test_ccx_position_position_1_2_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position NEW COLUMN
    def test_ccx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ccx(0, 1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position SAME COLUMN
    def test_ccx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position BETWEEN SWAP
    def test_ccx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 4)

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 1, 'Swap'], [1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position UNDER SWAP
    def test_ccx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ccx(2, 3, 4)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'CTRL'), (3, 'CTRL'), (4, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'CTRL', 'X']])

    # CCX add
    def test_ccx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(1, 2, 3, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE position1
    def test_ccx_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx('position', 2, 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_ccx_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 'position', 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position3
    def test_ccx_badArgumentType_position3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_ccx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____MEASURE_____##################
class Test_Measure(unittest.TestCase):

    # MEASURE position 0
    def test_measure_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.measure(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Measure']])

    # MEASURE EXISTING CIRCUIT position NEW COLUMN
    def test_measure_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Measure']])

    # MEASURE EXISTING CIRCUIT position SAME COLUMN
    def test_measure_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position BETWEEN SWAP
    def test_measure_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position UNDER SWAP
    def test_measure_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.measure(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Measure']])

    # MEASURE position LIST
    def test_measure_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.measure([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure', 'Measure']])
    
    # MEASURE position LIST EXISTING CIRCUIT
    def test_measure_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.measure([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['Measure', 'Measure', 'Measure']])

    # MEASURE position LIST EXISTING CIRCUIT WITH SWAP
    def test_measure_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure'), (3, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Measure', 'Measure', 'Measure', 'Measure']])

    # MEASURE position ALL
    def test_measure_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.measure()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure']])

    # MEASURE position ALL BETWEEN SWAP
    def test_measure_position_all_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Measure', 'Measure', 'Measure']])
    
    # BAD ARGUMENT position LIST
    def test_measure_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_measure_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_measure_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_measure_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BARRIER_____##################
class Test_Barrier(unittest.TestCase):

    # BARRIER position 0
    def test_barrier_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.barrier(0)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER']])

    # BARRIER EXISTING CIRCUIT position NEW COLUMN
    def test_barrier_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(0)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SPACER']])

    # BARRIER EXISTING CIRCUIT position SAME COLUMN
    def test_barrier_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(1)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'SPACER']])

    # BARRIER EXISTING CIRCUIT position BETWEEN SWAP
    def test_barrier_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier(1)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SPACER']])

    # BARRIER EXISTING CIRCUIT position UNDER SWAP
    def test_barrier_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.barrier(2)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SPACER']])

    # BARRIER position LIST
    def test_barrier_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.barrier([0, 1, 2])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER', 'H', 'SPACER'], [1, 'SPACER']])
    
    # BARRIER position LIST EXISTING CIRCUIT
    def test_barrier_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.barrier([0, 1, 2])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['X', 'SPACER', 'SPACER'], ['SPACER']])

    # BARRIER position LIST EXISTING CIRCUIT WITH SWAP
    def test_barrier_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier([0, 1, 2, 3])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SPACER', 'SPACER', 'SPACER', 'SPACER']])

    # BARRIER position ALL
    def test_barrier_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.barrier()

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['SPACER', 'SPACER']])

    # BARRIER position ALL BETWEEN SWAP
    def test_barrier_position_all_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier()

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SPACER', 'SPACER', 'SPACER']])

    # BAD ARGUMENT position LIST
    def test_barrier_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_barrier_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_barrier_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_barrier_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BEGIN REPEAT_____##################
class Test_BeginRepeat(unittest.TestCase):

    # BEGIN REPEAT position 0
    def test_beginRepeat_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_beginRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_beginRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_beginRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_beginRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.beginRepeat(2, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST
    def test_beginRepeat_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.beginRepeat([0, 1], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST EXISTING CIRCUIT
    def test_beginRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.beginRepeat([0, 1, 2], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'}), (2, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['X'], [{'arg': '2', 'id': 'BEGIN_R'}, {'arg': '2', 'id': 'BEGIN_R'}, {'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT position LIST EXISTING CIRCUIT WITH SWAP
    def test_beginRepeat_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.beginRepeat([0, 1, 2, 3], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'}), (2, {'id': 'BEGIN_R', 'arg': '2'}), (3, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BAD ARGUMENT position LIST
    def test_beginRepeat_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_beginRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 0], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_beginRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat('position', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_beginRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 'position'], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE repetitions
    def test_beginRepeat_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat(0, 'repetitions')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____END REPEAT_____##################
class Test_EndRepeat(unittest.TestCase):

    # END REPEAT position 0
    def test_endRepeat_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['END_R']])

    # END REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_endRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['END_R']])

    # END REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_endRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_endRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_endRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.endRepeat(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'END_R']])

    # END REPEAT position LIST
    def test_endRepeat_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.endRepeat([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['END_R', 'END_R', 'END_R']])

    # END REPEAT position LIST EXISTING CIRCUIT
    def test_endRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.endRepeat([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['END_R', 'END_R', 'END_R']])

    # END REPEAT position LIST EXISTING CIRCUIT WITH SWAP
    def test_endRepeat_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.endRepeat([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R'), (3, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['END_R', 'END_R', 'END_R', 'END_R']])

    # BAD ARGUMENT position LIST
    def test_endRepeat_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_endRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_endRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_endRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CONTROL_____##################
class Test_Control(unittest.TestCase):

    # CONTROL position 0
    def test_control_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(cx, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # BAD ARGUMENT TYPE position
    def test_control_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            cx = circuit.control('position', circuit.h(0, False))
            circuit.addCreatedGate(cx)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE circuit
    def test_control_badArgumentType_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(0, 'circuit')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD CREATED GATE_____##################
class Test_AddCreatedGate(unittest.TestCase):

    # ADD CREATED GATE position 0
    def test_addCreatedGate_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # BAD ARGUMENT TYPE gate
    def test_addCreatedGate_badArgumentType_gate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.addCreatedGate('gate')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____MULTI CONTROL GATE_____##################
class Test_MCG(unittest.TestCase):

    # MCG position 0
    def test_mcg_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position NEW COLUMN
    def test_mcg_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position SAME COLUMN
    def test_mcg_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position BETWEEN SWAP
    def test_mcg_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position UNDER SWAP
    def test_mcg_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.mcg(2, circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'X']])

    # MCG position LIST
    def test_mcg_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.mcg([0, 2], circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['CTRL', 1, 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT
    def test_mcg_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['CTRL', 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT WITH SWAP
    def test_mcg_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['CTRL', 'CTRL', 'X']])

    # MCG add
    def test_mcg_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg([0, 2], circuit.x(3, False), False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST
    def test_mcg_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([], circuit.x(3))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_mcg_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 0], circuit.x(3))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT circuit
    def test_mcg_badArgument_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg(1, circuit.x(3))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (1, 'CTRL')])
        self.assertNotEqual(circuit.getCircuitBody(), [[1, 'CTRL', 1, 'X']])

    # BAD ARGUMENT TYPE position
    def test_mcg_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg('position', circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_mcg_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 'position'], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_mcg_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 2], circuit.x(3, False), 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()