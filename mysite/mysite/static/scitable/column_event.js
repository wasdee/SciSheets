/*jshint onevar: true */
/*jshint todo: true */
/*jshint qunit: true */
/*jshint jquery: true */
/*jshint yui: true */
/*jslint plusplus: true */
/*jshint onevar: false */
/*global SciSheetsUtilEvent, $, alert, YAHOO, SciSheetsUtilClick */
/*jslint unparam: true*/
/*jslint browser: true */
/*jslint indent: 2 */
/*jslint newcap: true */

var ROW_NAME = "row";

function SciSheetsColumn(scisheet) {
  "use strict";
  this.scisheet = scisheet;
}

SciSheetsColumn.prototype.click = function (oArgs) {
  "use strict";
  var ep;
  ep = new SciSheetsUtilEvent(this.scisheet, oArgs);
  if (ep.columnName  === ROW_NAME) {
    SciSheetsUtilClick("FirstColumnClickMenu", function (eleId) {
      var msg;
      msg = "Column '" + ep.columnName + "' clicked.";
      msg += " Selected " + eleId + ".";
      console.log(msg);
    });
  } else {
    SciSheetsUtilClick("ColumnClickMenu", function (eleId) {
      var msg;
      msg = "Column '" + ep.columnName + "' clicked.";
      msg += " Selected " + eleId + ".";
      console.log(msg);
    });
  }
};
