"""
API for SciSheets. This consists of three parts: 
  1. the formulas API that is used in formulas 
  2. the plugin API that is used in the python functions referenced in formulas
  3. the administrative API generated by SciSheets
"""

from column import Column
from table import Table
import util


class API(object):
  """
  Code that is common to the formulas and plugin APIs.
  """

  def __init__(self, table):
    self._table = table
    self._column_idx = None

class APIAdmin(API):
  """
  Methods and properties used in support of the user APIs.
  """

  def setColumnIndex(self, column_idx):
    self._column_idx = column_idx


class APIFormulas(API):
  """
  Formulas API
  """

  def _getValidatedColumn(self, column_id):
    """
    :param column_id: either the name of the column or
                        its 1-based index after the name ('row') column
    :return: column object
    :raises: ValueError if column_name doesn't exist
    """
    if isinstance(column_id, int):
      column = self._table.columnFromIndex(column_id)
    elif isinstance(column_id, str):
      column = self._table.columnFromName(column_name)
    else:
      column = None
    if column is None:
      raise ValueError("%s column does not exist." % column_name)
    return column

  def createTruthTable(self, column_names, only_boolean=False):
    """
    Creates a truth table with all combinations of Boolean
    values for the number of columns provided.
    :param list-of-str column_names: names of columns to create
    :param bool only_boolean: True if only want boolean values
                              in the truth table
    """
    columns = []
    for name in column_names:
      columns.add(self._createColumn(name))
    # Create the column values

  def _createColumn(self, column_name, index=None):
    """
    Creates a new column, either just to the right of the
    current column (index=None) are at a specific index.
    :param str column_name: name of the column to create
    :param int index: index where the column is to be placed
    :return: column object
    :raises: ValueError if invalid name for column
    """
    column = Column(column_name)
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
    column = self._getValidatedColumn(column_id)
    error = self._table.deleteColumn(column)
    if error is not None:
      raise ValueError(error)

  def param(self, column_id, row=1):
    """
    :param str column_name: name of the column referenced
    :param int row: row number from which the parameter is extracted
    :return: scalar object at the indicate row for the column.
    :raises: ValueError
    """
    column = self._getValidatedColumn(column_name)
    values = column.getCells()
    if len(values) < row - 1:
      raise ValueError("%s column does not have %d values." 
          % (column_name, row))
    return values[row-1]
