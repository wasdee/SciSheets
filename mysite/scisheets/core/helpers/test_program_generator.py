'''Tests for program_generator'''

import program_generator as pg
from ..helpers_test import createTable,  \
    stdoutIO, TableFileHelper, TEST_DIR
from ...core import column as cl
from api_util import writeTableToFile
import os
import numpy as np
import shutil
import unittest


# Constants
COLUMN = "DUMMY"
COLUMN1 = "DUMMY1"
COLUMN2 = "A"
COLUMN3 = "DUMMY3"
COLUMN4 = "DUMMY4"
COLUMN5 = "B"
COLUMNC = "C"
COLUMN_VALID_FORMULA = "VALID_FORMULA"
COLUMN_INVALID_FORMULA = "INVALID_FORMULA"
TABLE_NAME = "DUMMY_TABLE"
LIST = [2.0, 3.0]
LIST2 = [3.0]
TABLE = 'DUMMY'
VALID_FORMULA = "np.sin(A) + B"
VALID_FORMULA_WITH_USER_FUNCTION = "np.sin(A) + timesTwo(B)"
SECOND_VALID_FORMULA = "np.cos(C)"
INVALID_FORMULA = "np.cun(A)" # Invalid function
COLUMN1_CELLS = ["one", "two", "three"]
COLUMN2_CELLS = [10.0, 20.0, 30.0]
COLUMN5_CELLS = [100.0, 200.0, 300.0]
COLUMNC_CELLS = [1000.0, 2000.0, 3000.0]
IMPORT_PATHS = ["", "scisheets.core"]


#############################
# Helper Functions
#############################
def _compile(statements):
  """
  Compiles the statements
  :param str statements:
  :return str/None: None if no error
  """
  error = None
  try:
    compile(statements, "string", "exec")
  except SyntaxError as err:
    error = str(err)
  return error


#############################
# Tests
#############################
# pylint: disable=W0212
# pylint: disable=C0111
# pylint: disable=R0904
class TestFunctions(unittest.TestCase):
 
  def testMakeOutputStr(self):
    result = pg._makeOutputStr(["a"])
    self.assertEqual(result, "a")
    result = pg._makeOutputStr(["a", "b"])
    self.assertEqual(result, "a,b")
    result = pg._makeOutputStr([])
    self.assertEqual(result, "")

  def testMakeFunctionStatement(self):
    statement = pg._makeFunctionStatement("func", ["a", "bb"])
    expected = "def func(a, bb):"
    self.assertEqual(statement, expected)
    statement = pg._makeFunctionStatement("func", [])
    expected = "def func():"
    self.assertEqual(statement, expected)
    statement = pg._makeFunctionStatement("func", ["a"])
    expected = "def func(a):"
    self.assertEqual(statement, expected)


class TestProgramGenerator(unittest.TestCase):

  def setUp(self):
    self.table = createTable(TABLE_NAME)
    self._addColumn(COLUMN1, cells=COLUMN1_CELLS)
    self.column_a = self._addColumn(COLUMN2, cells=COLUMN2_CELLS)
    self.column_b = self._addColumn(COLUMN5, cells=COLUMN5_CELLS)
    self.column_c = self._addColumn(COLUMNC, cells=COLUMNC_CELLS)
    self.column_valid_formula = self._addColumn(COLUMN_VALID_FORMULA,
                                                formula=VALID_FORMULA)
    writeTableToFile(self.table)
    self.pgm_gen = pg.ProgramGenerator(self.table, TEST_DIR)

  def _addColumn(self, name, cells=None, formula=None):
    column = cl.Column(name)
    if formula is not None:
      column.setFormula(formula)
    if cells is not None:
      column.addCells(cells)
    self.table.addColumn(column)
    return column

  def testFindFileNames(self):
    filename = "dummy"
    helper = TableFileHelper(filename, TEST_DIR)
    helper.create()
    python_files = self.pgm_gen._findFilenames()
    self.assertTrue(python_files.index(filename) > -1)
    helper.destroy()

  def testMakeFormulaImportStatements(self):
    statements = self.pgm_gen._makeFormulaImportStatements()
    self.assertEqual(len(statements), 0)
    self.column_valid_formula.setFormula("dummy()")
    statement = self.pgm_gen._makeFormulaImportStatements()
    expected = "from dummy import dummy"
    self.assertEqual(statement, expected)

  def _testAssignmentStatements(self, function):
    """
    Function that returns assignment statements
    :param function function:
    """
    stg = "ColumnValues("
    statements = function()
    expected = self.table.numColumns()
    self.assertEqual(expected, statements.count(stg))
    statements = function(excludes=['row'])
    expected = self.table.numColumns() - 1
    self.assertEqual(expected, statements.count(stg))
    statements = function(only_includes=['row'])
    self.assertEqual(1, statements.count(stg))
    self.assertEqual(statements.count('row'), 2)
    self.assertIsNone(_compile(statements))

  def testAssignmentStatements(self):
    self._testAssignmentStatements(
        self.pgm_gen._makeColumnValuesAssignmentStatements)
    self._testAssignmentStatements(
        self.pgm_gen. _makeVariableAssignmentStatements)

  def testFormulaColumns(self):
    columns = self.pgm_gen._formulaColumns()
    self.assertEqual(columns[0].getName(), 'VALID_FORMULA')
    self.table.deleteColumn(columns[0])
    columns = self.pgm_gen._formulaColumns()
    self.assertEqual(len(columns), 0)

  def testMakeVariablePrintStatements(self):
    statements = self.pgm_gen._makeVariablePrintStatements()
    for column in self.table.getColumns():
      self.assertTrue(column.getName() in statements)

  def testMakePrologue(self):
    statements = self.pgm_gen._makePrologue()
    self.assertTrue('import' in statements)
    self.assertIsNone(_compile(statements))

  def testMakeFormulaStatements(self):
    statements = self.pgm_gen._makeFormulaStatements()
    formula_column = self.table.columnFromName('VALID_FORMULA')
    self.assertTrue(formula_column.getFormula() in statements)
    self.assertIsNone(_compile(statements))

  def testMakeAPIPluginInitializationStatements(self):
    statements = self.pgm_gen._makeAPIPluginInitializationStatements()
    self.assertTrue(self.table.getFilepath() in statements)
    self.assertTrue("initialize()" in statements)
    self.assertIsNone(_compile(statements))

  def _checkWorkflow(self, program, tags):
    """
    Verifies that the tags occur in order in the program
    :param str program:
    :param list-of-str tags:
    """
    last_index = 0
    error = None
    for tag in tags:
      try:
        current_index = program.index(tag)
      except ValueError as err:
        import pdb; pdb.set_trace()
        error = str(err)
      self.assertIsNone(error)
      if not(last_index < current_index):
        import pdb; pdb.set_trace()
      self.assertTrue(last_index < current_index)
      last_index = current_index
    error = _compile(program)
    if error is not None:
      import pdb; pdb.set_trace()
    self.assertIsNone(_compile(program))

  def testMakeEvaluationScriptProgram(self):
    tags = ["import", "#_table", "getColumnValues", "np.sin", \
        "setColumnValues"]
    program = self.pgm_gen.makeEvaluationScriptProgram()
    self._checkWorkflow(program, tags)
    tags = ["import", "_table", "getColumnValues", "np.sin", \
        "setColumnValues"]
    program = self.pgm_gen.makeEvaluationScriptProgram(
        create_API_object=True)
    self._checkWorkflow(program, tags)

  def testMakeExportScriptProgram(self):
    tags = ["import", "_table", "getColumnValues", "np.sin", \
        "print"]
    program = self.pgm_gen.makeExportScriptProgram()
    self._checkWorkflow(program, tags)

  def testMakeFunctionProgram(self):
    function_name = "my_func"
    inputs = ["A", "B"]
    outputs = ["C"]
    def_stmt = "def %s(" % function_name
    tags = ["import", "api.APIPlugin", def_stmt,  \
        "getColumnValues", "np.sin", "return"]
    program = self.pgm_gen.makeFunctionProgram(function_name,
                                               inputs,
                                               outputs)
    self._checkWorkflow(program, tags)

  def testMakeTestProgram(self):
    function_name = "my_func"
    inputs = ["A", "B"]
    output = "C"
    function_call = "%s = %s(" % (output, function_name)
    tags = ["import", "class ", "api.APIPlugin", function_call, \
        "self.assert"]
    program = self.pgm_gen.makeTestProgram(function_name,
                                           inputs,
                                           [output])
    self._checkWorkflow(program, tags)
    

if  __name__ == '__main__':
  unittest.main()
