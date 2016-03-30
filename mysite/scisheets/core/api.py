"""
The API provides runtime support for user execution. There are two runtime environments:
(a) evaluation of the formulas in a Table object and (b) execution of a standalone
python program that was exported from a Table object.
The API consists of these parts: 
  1. APIFormulas provides extended capabilities for executing formulas (e.g., trinary logical operations
     and truth tables)
  2. APIPlugin provides runtime support for standalone execution
  3. API base clase provides common code.
"""

from column import Column
from table import Table
import util.util as util
import util.api_util as api_util
from util.trinary import Trinary
from util.combinatoric_list import CombinatoricList
import collections
import os


class API(object):
  """
  Code that is common to the formulas and plugin APIs.
  Usage:
     S = API(table_filepath)
     S.initialize()
  """

  def __init__(self, table_filepath):
    """
    :param str table_filepath: full path to the table file
    """
    self._table_filepath = table_filepath
    self._table = None
    self._column_idx = None

  def getColumnValues(self, column_name):
    """
    :param str column_name: name of the column
    :return: iterable of object
    :raises: ValueError
    """
    column = self._table.columnFromName(column_name)
    if column is None:
      raise ValueError("Column name not found: %s" % column_name)
    data_class = column.getDataClass()
    return data_class.cons(column.getCells())

  def getTable(self):
    return self._table

  def initialize(self):
    """
    Does initialization at the beginning of executing table
    code.
    """
    self._table = api_util.getTableFromFile(self._table_filepath)

  def setColumnValues(self, column_name, values):
    """
    :param str column_name: name of the column
    :param iterable-of-object values:
    :raises: ValueError
    """
    column = self._table.columnFromName(column_name)
    if column is None:
      raise ValueError("Column name not found: %s" % column_name)
    if isinstance(values, list):
      list_values = values
    elif "tolist" in dir(values):
      list_values = values.tolist()
    else:
      list_values = list(values)
    column.addCells(list_values, replace=True)

  def updateTableFile(self):
    api_util.writeTableToFile(self._table.getFilepath())


class APIFormulas(API):
  """
  The API extends formulas with: Trinary logic, creation of scalar 
  parameters, creation and deletion of columns.
  Key concepts:
    column_id - either the column name or column index
  """

  def __init__(self, table_filepath):
    super(APIFormulas, self).__init__(table_filepath)

  def _getColumn(self, column_id, validate=True):
    """
    :param column_id: either the name of the column or
                      its 1-based index after the name ('row') column
    :param bool validate: Validates the columns present if True
    :return: column object
    :raises: ValueError if column_name doesn't exist
    """
    if isinstance(column_id, int):
      column = self._table.columnFromIndex(column_id)
    elif isinstance(column_id, str):
      column = self._table.columnFromName(column_id)
    else:
      column = None
    if column is None and validate:
      import pdb; pdb.set_trace()
      raise ValueError("%s column does not exist." % str(column_id))
    return column

  def createTruthTable(self, column_names, only_boolean=False):
    """
    Creates a truth table with all combinations of Boolean
    values for the number of columns provided.
    :param list-of-str column_names: names of columns to create
    :param bool only_boolean: True if only want boolean values
                              in the truth table
    Usage example:
      S.createTruthTable(['A', 'B'])
      Ap = S.createTrinary(A)  # Trinary object
      Bp = S.createTrinary(B)  # Trinary object
      Cp = Ap & Bp | -Bp
    """
    columns = []
    for name in column_names:
      columns.append(self._createColumn(name, asis=True))
    # Create the column values
    elements = [False, True]
    if not only_boolean:
      elements.insert(0, None)
    num_lists = len(column_names)
    combinatorics = CombinatoricList(elements)
    results = combinatorics.run(num_lists)
    # Assign the results
    for idx in range(num_lists):
      column = columns[idx]
      self._table.addCells(column, results[idx])

  @staticmethod 
  def createTrinary(iterable):
    return Trinary(iterable)

  def _createColumn(self, column_name, index=None, asis=False):
    """
    Creates a new column, either just to the right of the
    current column (index=None) are at a specific index.
    :param str column_name: name of the column to create
    :param int index: index where the column is to be placed
    :param bool asis: Column data should not be coerced
    :return: column object
    :raises: ValueError if invalid name for column
    """
    # First delete the column to make sure that it doesn't exist
    self.deleteColumn(column_name)
    # Now create the column
    column = Column(column_name, asis=asis)
    error = self._table.addColumn(column, index)
    if error is not None:
      raise ValueError(error)
    return column

  def createColumn(self, column_name, index=None):
    """
    Creates a new column, either just to the right of the
    current column (index=None) are at a specific index.
    :param str column_name: name of the column to create
    :param int index: index where the column is to be placed
    """
    self._createColumn(column_name, index)

  def deleteColumn(self, column_id):
    """
    Detes an existing a column if it exists.
    :param column_id: either the name of the column or 
                      the 1-based index after the 'row' column
    """
    column = self._getColumn(column_id, validate=False)
    if column is not None:
      _  = self._table.deleteColumn(column)

  def param(self, column_id, row_num=1):
    """
    :param str column_name: name of the column referenced
    :param int row_num: row from which the parameter is extracted
    :return: scalar object at the indicate row for the column.
    :raises: ValueError
    """
    column = self._getColumn(column_id)
    values = column.getCells()
    if len(values) < row_num - 1:
      raise ValueError("%s column does not have %d values." 
          % (column_id, row_num))
    return values[row_num-1]


class APIPlugin(API):
  """
  Support for running standalone codes
  """

  def __init__(self, table_filepath, inputs, outputs):
    """
    :param list-of-str inputs: names of input columns
    :param list-of-str outputs: names of output columns
    """
    self._inputs = inputs
    self._outputs = outputs
    super(APIPlugin, self).__init__(table_filepath)
