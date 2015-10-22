
import sys

from PyQt4.Qt import *
from PyQt4.QtGui import *

import python_to_R
from ome_globals import *

import ui_binary_calculator

import pdb
from PyQt4.QtCore import pyqtRemoveInputHook

# This calculator is currently meant to be standalone but might be integrated into
# the spreadsheet later

class BinaryCalculator(QDialog, ui_binary_calculator.Ui_BinaryDataForm):
    def __init__(self, conf_level, digits, debug=False, parent=None):
        super(BinaryCalculator, self).__init__(parent)
        self.setupUi(self)

        # Debug mode. Mainly toggles on a bunch of printing for debuggin
        self.debug = debug
        self.digits = digits

        self.conf_level = conf_level
        self.mult = python_to_R.get_mult_from_r(self.conf_level)

        self._setup_signals_and_slots()
        

        self.entry_widgets = [
            self.raw_data_table,
            self.low_txt_box,
            self.high_txt_box,
            self.effect_txt_box,
        ]
        self.text_boxes = [self.low_txt_box, self.high_txt_box, self.effect_txt_box]
        
        self.ci_label.setText("{0:.1f}% Confidence Interval".format(self.conf_level))
        self.undoStack = QUndoStack(self)

        self.clear_form()
        self._populate_effect_options()      # Add entries to 'effects' combo box

        # self.toggle_inconsistent_state(self.is_consistent(self.table_data))
        self.enable_back_calculation_btn()
        self.back_calc_btn.hide()

    def clear_form(self):
        '''
        Initializes store of table data to None values. Used to undo changes
        to the raw data table
        '''

        self.raw_data_table.blockSignals(True)
        self.raw_data_table.clearContents()
        self.table_data = {}
        for row in range(3):
            for col in range(3):
                self.table_data[idx(row, col)] = None
        self.set_table_widget_values(self.table_data)
        self.raw_data_table.setEnabled(True)
        self.raw_data_table.blockSignals(False)

        self.effect_txt_box.setText('')
        self.low_txt_box.setText('')
        self.high_txt_box.setText('')

    def get_stored_value(self, row, col):
        ''' Gets the stored value for the cell at row,col in the table '''

        return self.table_data[idx(row, col)]

    def set_stored_value(self, value, row, col):
        self.table_data[idx(row, col)] = value

    def _setup_signals_and_slots(self):
        ''' Make all the necessary connections for the the form to work '''

        QObject.connect(self.raw_data_table, SIGNAL("cellChanged(int,int)"), self.cell_changed)

        QObject.connect(self.effect_cbo_box, SIGNAL("currentIndexChanged(int)"), self.effect_changed)
        QObject.connect(self.clear_Btn, SIGNAL("clicked()"), self.clear_form)
        QObject.connect(self.back_calc_btn, SIGNAL("clicked()"), self.enable_back_calculation_btn)

        QObject.connect(self.effect_txt_box, SIGNAL("editingFinished()"), lambda: self.val_changed("est"))
        QObject.connect(self.low_txt_box, SIGNAL("editingFinished()"), lambda: self.val_changed("lower"))
        QObject.connect(self.high_txt_box, SIGNAL("editingFinished()"), lambda: self.val_changed("upper"))

        # For all of the above signals, we should try to see if we can enable
        # the back calculation button so we connect all the signals above
        # to the enable_back_calculation_button
        QObject.connect(self.raw_data_table, SIGNAL("cellChanged(int,int)"), self.enable_back_calculation_btn)

        QObject.connect(self.effect_cbo_box, SIGNAL("currentIndexChanged(QString)"), self.enable_back_calculation_btn)
        QObject.connect(self.clear_Btn, SIGNAL("clicked()"), self.clear_form)
        QObject.connect(self.back_calc_btn, SIGNAL("clicked()"), self.enable_back_calculation_btn)

        QObject.connect(self.effect_txt_box, SIGNAL("editingFinished()"), self.enable_back_calculation_btn)
        QObject.connect(self.low_txt_box, SIGNAL("editingFinished()"), self.enable_back_calculation_btn)
        QObject.connect(self.high_txt_box, SIGNAL("editingFinished()"), self.enable_back_calculation_btn)

        # Add undo/redo actions
        undo = QAction(self)
        redo = QAction(self)
        undo.setShortcut(QKeySequence.Undo)
        redo.setShortcut(QKeySequence.Redo)
        self.addAction(undo)
        self.addAction(redo)
        QObject.connect(undo, SIGNAL("triggered()"), self.undo)
        QObject.connect(redo, SIGNAL("triggered()"), self.redo)

    def enable_back_calculation_btn(self):
        '''
        Enable or disable the back calculation button according to whether or
        not we can back calculate the rest of the values
        '''

        print "not implemented yet"
        pass

    def clicked_back_calculate(self):
        '''
        Handler for clicking the back-calculate button. Back-calculates the rest
        of the values and sets them on the form.
        '''

        print "not implemented yet"
        pass

    def cell_changed(self, row, col):
        '''
        Called when a cell in the raw data table changes. Performs the following
        tasks:
            [X] 1. Validates that the cell data is an integer.
            [X] 2. Verify that the new table after this new value is entered is
                consistent (all values valid +ve integers).
                (if not consistent, set the inconsistent table label)
            [X] 3. If the table is consistent:
                    a) store the values in self.table_data.
                    b) set the values of the table in the widget
                   Otherwise,
                    a) Display a warning and revert the change
                N.B. May want to switch to QTableView to avoid having to set the
                values in both the QTableWidget and separate data object.
            [ ] 4. undo Add command to change the value to the undo stack
        '''

        # Validate the new cell is a positive integer. Otherwise, show a warning message and
        # set the value back to its original value.
        prev_value = self.get_stored_value(row, col)
        prev_value_as_text = "";
        if prev_value is not None:
            prev_value_as_text = str(prev_value)
        item = self.raw_data_table.item(row, col)
        value = str(item.text())
        if not (represents_int(value) and int(value) >= 0):
            QMessageBox.warning(
                self,
                'invalid value',
                '%s is not a valid count value' % value,
            )
            # reset value in tablet to previous value
            self.raw_data_table.blockSignals(True)
            item.setText(prev_value_as_text)
            self.raw_data_table.blockSignals(False)
            return

        # Calculate candidate table
        candidate_table = self.table_data.copy()
        candidate_table[idx(row, col)] = value
        proposed_table = compute_2x2_table(candidate_table)
        if self.debug:
            print "Proposed table: %s" % _table_str(proposed_table)

        # Set the table widget to the proposed table regardless of it being
        # consistent or not
        self.set_table_widget_values(proposed_table)
        if not self.is_consistent(proposed_table):
            print "Set inconsistent state label?"
            QMessageBox.warning(
                self,
                'Inconsistent state',
                "Entering '%s' would put the table in an inconsistent state, reverting change." % value
            )
            # Restore table widget to the way it was before
            self.set_table_widget_values(self.table_data)
            return False

        # Store new table values
        self.table_data = proposed_table

        # do not allow the table to be edited if it is full
        if _table_full(self.table_data):
            self._disable_cells()

        # Recalculate effect size
        if _table_full(self.table_data):
            self.populate_effect_textboxes()

        if self.debug:
            print "the cell at (row,col)=(%d,%d) changed." % (row,col)

    def _disable_cells(self):
        self.raw_data_table.blockSignals(True)
        for row in range(3):
            for col in range(3):
                item = self.raw_data_table.item(row, col)
                flags = item.flags()
                item.setFlags(flags & ~Qt.ItemIsEditable)
        self.raw_data_table.setEnabled(False)

    def set_table_widget_values(self, table_data):
        self.raw_data_table.blockSignals(True)
        for row in range(3):
            for col in range(3):
                index = idx(row,col)
                value = table_data[index]
                text_value = '' if value is None else str(value)
                item = QTableWidgetItem(text_value)
                self.raw_data_table.setItem(row, col, item)
        self.raw_data_table.blockSignals(False)

    def is_consistent(self, table_data):
        '''
        Returns true if the table data is made up of either blanks or positive
        integers.
        '''

        for row in range(3):
            for col in range(3):
                index = idx(row,col)
                value = table_data[index]
                isvalidinteger = represents_int(value) and int(value) >= 0
                if not (value is None or isvalidinteger):
                    return False

        return True

    def _get_val(self, row, col):
        '''
        Gets the value at row,col in the table widget as a string. If there is no data in the cell,
        return the empty string.
        '''
        value = str(self.raw_data_table.item(row,col).text())
        return value

    def effect_changed(self, index):
        ''' Called when a new effect is selected in the combo box '''
        
        #self.cur_effect = unicode(self.effect_cbo_box.currentText().toUtf8(), "utf-8")
        print "Current index is %d" % index
        metric = self.effect_cbo_box.itemData(index).toInt()[0]
        print "Current metric is %s" % str(METRIC_TEXT[metric])

        # Calculate current effect size if possible
        if _table_full(self.table_data):
            self.populate_effect_textboxes()

    def recalculate_effect(self):
        ''' Calculates the effect size based on the data in the table and updates
        the effect textboxes '''

        if not _table_full(self.table_data):
            return

        index = self.effect_cbo_box.currentIndex()
        metric = self.effect_cbo_box.itemData(index).toInt()[0]

        data = {}
        data['experimental_response']   = [self.table_data["0,0"]] # ai
        data['experimental_noresponse'] = [self.table_data["0,1"]] # bi
        data['control_response']        = [self.table_data["1,0"]] # ci
        data['control_noresponse']      = [self.table_data["1,1"]] # di
        print "Data: %s" % str(data)
        result = python_to_R.effect_size(
            metric,
            data_type=TWO_BY_TWO_CONTINGENCY_TABLE,
            data=data,
        )

        yi = result['yi'][0]
        vi = result['vi'][0]

        print "yi, vi: %f, %f" % (yi, vi)

        # includes yi, vi, lb, ub
        bounds = python_to_R.calculate_bounds(yi=yi, vi=vi, conf_level=self.conf_level)
        print "Upper and lower bounds: %s" % str(bounds)
        return bounds


    def populate_effect_textboxes(self):
        '''
        Update the textboxes with values based on the values in the data table
        '''

        result = self.recalculate_effect()
        self.yi = result['yi']
        self.vi = result['vi']
        self.lb = result['lb']
        self.ub = result['ub']


        format_str = "{:.%df}" % self.digits

        self.effect_txt_box.setText(format_str.format(self.yi))
        self.low_txt_box.setText(format_str.format(self.lb))
        self.high_txt_box.setText(format_str.format(self.ub))





        pass

    ####### Undo framework ############
    def undo(self):
        print("undoing....")
        self.undoStack.undo()
        
    def redo(self):
        print("redoing....")
        self.undoStack.redo()
    #################################

    def _set_val(self, row, col, val):
        if is_NaN(val):  # get out quick
            print "%s is not a number" % val
            return
        
        try:
            self.raw_data_table.blockSignals(True)
            str_val = "" if val in EMPTY_VALS else str(int(val))
            if self.raw_data_table.item(row, col) == None:
                self.raw_data_table.setItem(row, col, QTableWidgetItem(str_val))
            else:
                self.raw_data_table.item(row, col).setText(str_val)
            print("    setting (%d,%d) to '%s'" % (row,col,str_val))

            self.raw_data_table.blockSignals(False)
        except:
            print("    Got to except in _set_val when trying to set (%d,%d)" % (row, col))
            raise

    def _populate_effect_options(self):
        ''' Fills in options for effects in effects combo box '''
        binary_metrics = DATA_TYPE_TO_METRICS[TWO_BY_TWO_CONTINGENCY_TABLE]

        self.effect_cbo_box.blockSignals(True)
        for metric in binary_metrics:
            self.effect_cbo_box.addItem(METRIC_TEXT[metric], metric)

        # Set default effect
        self.effect_cbo_box.setCurrentIndex(0)
        self.effect_changed(0)
        self.effect_cbo_box.blockSignals(False)




######## End of BinaryCalculator class Definition ########

def idx(row, col):
    ''' Get key for stored table index '''
    index = "%d,%d" % (row,col)
    return index

def compute_2x2_table(table_data):
    '''
    Computes values for the whole 2x2 table if possible based on partial values
    from the rest of the table'''

    table_data = table_data.copy() # make local copy of the table to avoid side-effects

    # Convert numerical data items to numbers:
    for row in range(3):
        for col in range(3):
            index = idx(row,col)
            value = table_data[index]
            if represents_int(value):
                table_data[index]=int(value)
            else:
                table_data[index]=None
    
    while True:
        changed = False
        for row in range(3):
            for col in range(3):
                # go through row-wise
                if table_data[idx(row,col)] is None:
                    if col == 0:
                        try:
                            #idx(row,col)
                            table_data[idx(row,col)] = table_data[idx(row,2)] - table_data[idx(row,1)]
                            changed = True
                        except:
                            pass
                    if col == 1:
                        try:
                            table_data[idx(row,col)] = table_data[idx(row,2)] - table_data[idx(row,0)]
                            changed = True
                        except:
                            pass
                    if col == 2:
                        try:
                            table_data[idx(row,col)] = table_data[idx(row,0)] + table_data[idx(row,1)]
                            changed = True
                        except:
                            pass
                # and now column-wise
                if table_data[idx(row,col)] is None:
                    if row == 0:
                        try:
                            table_data[idx(row,col)] = table_data[idx(2,col)] - table_data[idx(1,col)]
                            changed = True
                        except:
                            pass
                    if row == 1:
                        try:
                            table_data[idx(row,col)] = table_data[idx(2,col)] - table_data[idx(0,col)]
                            changed = True
                        except:
                            pass
                    if row == 2:
                        try:
                            table_data[idx(row,col)] = table_data[idx(0,col)] + table_data[idx(1,col)]
                            changed = True
                        except:
                            pass
        if not changed:
            break
    ## end of big while loop

    return table_data

def _table_str(table):
    ''' Prints the proposed table (just for debugging) '''
    string = ''
    for row in range(3):
        row_array = []
        for col in range(3):
            index = idx(row,col)
            value = table[index]
            if value in ('',None):
                row_array.append('')
            else:
                row_array.append(str(value))
        string += '\t'.join(row_array) + "\n"
    print string

def _table_full(table):
    ''' Returns true if the table data is completely filled out '''

    values = table.values()
    if len(values) < 9:
        print "Table is not full since less than 9 entries present"
        return False
    for value in values:
        if value is None or value == '':
            print "table not full"
            return False
    print "table is full"
    return True


if __name__ == '__main__': 
    app = QApplication(sys.argv)
    form = BinaryCalculator(conf_level=DEFAULT_CONFIDENCE_LEVEL, debug=True, digits=3)
    rloader = python_to_R.RlibLoader()
    rloader.load_all_libraries()
    form.show()
    form.raise_()
    app.exec_()