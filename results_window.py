#############################################
#                                           #
#  George Dietz                             #
#  Brown University                         #
#  OpenMEE                                  #
#                                           #
#  This is the component responsible        #
#  for rendering MA results.                #
#                                           #
#############################################

#import random
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import pdb
import os
import sys
import ui_results_window
import edit_forest_plot_form
import python_to_R
#import shutil

from globals import *

PageSize = (612, 792)
padding = 25
horizontal_padding = 75
SCALE_P = .5 # percent images are to be scaled

# these are special forest plots, in that multiple parameters objects are
# require to re-generate them (and we invoke a different method!)
SIDE_BY_SIDE_FOREST_PLOTS = ("NLR and PLR Forest Plot", "Sensitivity and Specificity","Cumulative Forest Plot")
ROW_HEIGHT = 15 # by trial-and-error; seems to work very well



class ResultsWindow(QMainWindow, ui_results_window.Ui_ResultsWindow):

    def __init__(self, results, summary="", parent=None):
        super(ResultsWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.copied_item = QByteArray()
        self.paste_offset = 5
        self.add_offset = 5
        self.buffer_size = 2
        self.prev_point = QPoint()
        self.borders = []
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageSize(QPrinter.Letter)
        self.summary=summary

        QObject.connect(self.nav_tree, SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                                       self.item_clicked)
                       
        self.psuedo_console.blockSignals(False)              
        QObject.connect(self.psuedo_console, SIGNAL("returnPressed(void)"),
                                       self.process_console_input)
        QObject.connect(self.psuedo_console, SIGNAL("upArrowPressed()"),
                                       self.f)
        QObject.connect(self.psuedo_console, SIGNAL("downArrowPressed()"),
                                       self.f)
        
        if "results_data" in results: # not really csv data but using 'text' too much here is confusing
            self.export_btn.clicked.connect(lambda: self.export_results(results["results_data"]))
        else:
            self.export_btn.hide()
                                       
                              
        self.nav_tree.setHeaderLabels(["results"])
        self.nav_tree.setItemsExpandable(True)
        self.x_coord = 5
        self.y_coord = 5

        # set (default) splitter sizes
        self.splitter.setSizes([400, 100])
        self.results_nav_splitter.setSizes([200,500])

        self.scene = QGraphicsScene(self)

        self.images = results["images"]
        print "images returned from analytic routine: %s" % self.images
        self.image_order = None
        if "image_order" in results:
            self.image_order = results["image_order"]
            print "image display order: %s" % self.image_order

        self.params_paths = {}
        if "image_params_paths" in results:
            self.params_paths = results["image_params_paths"]
    
        self.image_var_names = results["image_var_names"]
        self.set_psuedo_console_text()
        self.items_to_coords = {}
        self.texts = results["texts"]

        self.groupings = [["Likelihood","nlr","plr"],
                          ["sens","spec"],
                          ["Subgroup",],
                          ["Cumulative",],
                          ["Leave-one-out",],]

        # first add the text to self.scene
        self.post_facto_text_to_add = []
        self.add_text()

        self.y_coord += ROW_HEIGHT/2.0

        # additional padding for Windows..
        # again, heuristic. I don't know
        # why windows requires so much padding.
        if sys.platform.startswith('win'):
            self.y_coord += 2*ROW_HEIGHT

        # and now the images
        self.add_images()
        
        # Add post-facto text items (for now, just the references)
        for title, text in self.post_facto_text_to_add:
            self._add_text_item(title, text)

        # reset the scene
        self.graphics_view.setScene(self.scene)
        self.graphics_view.ensureVisible(QRectF(0,0,0,0))

        if not SHOW_PSEUDO_CONSOLE_IN_RESULTS_WINDOW:
            self.psuedo_console.setVisible(False)


    def f(self):
        print self.current_line()
        
    def export_results(self, data):
        # Choose file location
        fpath = os.path.join(BASE_PATH, "results.txt") # default
        fpath = QFileDialog.getSaveFileName(caption="Choose location to save file", filter="Text (*.txt)",directory=fpath)
        fpath = str(fpath)
        if fpath == "":
            print("cancelled")
            return
        
        # Add .txt extension if not already present
        index_of_period = fpath.find('.')
        
        if index_of_period != -1:
            fpath = fpath[:index_of_period] + ".txt"
        else:
            fpath+= ".txt"
            
        print("Filepath: %s" % fpath)

# APPARENTLY THIS IS HANDLED BY THE SAVE FILE DIALOG ALREADY
#         if os.path.exists(fpath):
#             msgBox = QMessageBox()
#             msgBox.setText("A file by that name already exists, overwrite it?")
#             msgBox.setWindowTitle("Overwrite existing file?")
#             msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
#             msgBox.setDefaultButton(QMessageBox.Yes)
#             choice = msgBox.exec_()
#             if choice == QMessageBox.Cancel:
#                 return
        
        keys_in_order = data['keys_in_order'] # make sure key order is consistent
        values = data['values'] # a dictionary mapping keys--> values
        
        
        # write the file
        with open(fpath,'w') as f:
            # Add input summary
            if len(self.summary) > 0:
                f.write("Analysis selections summary:\n")
                f.write(boxify(self.summary))
                f.write("\n\n")
            for key in keys_in_order:
                value = values[key]
                f.write("%s: %s\n" % (key, data['value_info'][key]['description'])) # write out key and description
                if isinstance(value, str):
                    f.write(value+"\n")
                elif isinstance(value, list):
                    for x in value:
                        f.write("%s\n" % x)
                else:
                    raise TypeError("Unrecognized type in data")
                # add space between values
                f.write("\n")
        
        self.statusbar.showMessage("Saved results to: %s" % fpath,5000)

    def set_psuedo_console_text(self):
        text = ["\t\tOpenMeta(analyst)",
               "This is a pipe to the R console. The image names are as follows:"]
        if self.image_var_names is not None:
            for image_var_name in self.image_var_names.values():
                text.append(image_var_name)
        self.psuedo_console.setPlainText(QString("\n".join(text)))
        self.psuedo_console.append(">> ")


    def add_images(self):
        # temporary fix!
        image_order = self.images.keys()
        
        if self.image_order is not None:
            image_order = self.image_order
        
        ungrouped_images = [(title, self.images[title]) for title in image_order]
        ordered_images = ungrouped_images
        
        if self.image_order is None:
            # add to the arguments to make more groups, also make sure to add them
            # in add_text
            grouped_images = self._group_items(ungrouped_images, self.groupings)
                                               #["Likelihood","nlr","plr"],
                                               #["sens","spec"])
            ordered_images = grouped_images
        
        
        for title,image in ordered_images:
            print "title: %s; image: %s" % (title, image)
            cur_y = max(0, self.y_coord)
            print "cur_y: %s" % cur_y
            # first add the title
            qt_item = self.add_title(title)
            
            # custom scales to which special plots should be scaled
            title_contents_to_scale = {"histogram":1,
                                       "funnel":1,
                                       }
            for title_contents, scale in title_contents_to_scale.items():
                if title.lower().rfind(title_contents) != -1:
                    pixmap = self.generate_pixmap(image, custom_scale=scale)
                    break
                else:
                    pixmap = self.generate_pixmap(image) 
            
            # if there is a parameters object associated with this object
            # (i.e., it is a forest plot of some variety), we pass it along
            # to the create_pixmap_item method to for the context_menu 
            # construction
            params_path = None
            if self.params_paths is not None and title in self.params_paths:
                params_path = self.params_paths[title]

            img_shape, pos, pixmap_item = self.create_pixmap_item(pixmap, self.position(),\
                                                title, image, params_path=params_path)
            
            self.items_to_coords[qt_item] = pos
            


    def generate_pixmap(self, image, custom_scale=None):
        # now the image
        pixmap = QPixmap(image)
        
        ###
        # we scale to address issue #23.
        # should probably pick a 'target' width/height, in case
        # others generate smaller images by default.
        if custom_scale is not None:
            scaled_width = custom_scale*pixmap.width()
            scaled_height = custom_scale*pixmap.height()
        else:
            scaled_width = SCALE_P*pixmap.width()
            scaled_height = SCALE_P*pixmap.height()
        

        if scaled_width > self.scene.width():
            self.scene.setSceneRect(0, 0, \
                                scaled_width+horizontal_padding,\
                                self.scene.height())
        

        pixmap = pixmap.scaled(scaled_width, scaled_height, \
                            transformMode=Qt.SmoothTransformation)

        return pixmap


    def add_text(self):
        
        # add to the arguments to make more groups, also make sure to add them
        # in add_images
        grouped_items = self._group_items(self.texts.items(), self.groupings)
        
        for title, text in grouped_items:
            if title.lower().rfind("reference") != -1:
                self.post_facto_text_to_add.append((title, text))
                continue
            self._add_text_item(title, text)
            
    def _add_text_item(self, title, text):
        try:
            #text = text[0]
            text = text.replace("\\n","\n") # manual escaping
            print "title: %s; text: %s" % (title, text)
            cur_y = max(0, self.y_coord)
            print "cur_y: %s" % cur_y
            # first add the title
            qt_item = self.add_title(title)

            # now the text
            text_item_rect, pos = self.create_text_item(unicode(text), self.position())
            self.items_to_coords[qt_item] =  pos
        except:
            pass
    
    def _group_items(self, items, groups):
        '''Groups items together if their title contains an element in a group list.
        items is a tuple of key,value pairs i.e. (title,text)
        Each group is a list of strings to which item titles should be matched
        i.e: _group_items(items, ['NLR','PLR'], ['sens','spec'])  '''
        
        def _get_group_id(key):
            for group_id, group in enumerate(groups):
                for grp_member in group:
                    if key.lower().find(grp_member.lower()) != -1:
                        return group_id
            return None
        
        # initialization
        grouped_items = []
        for i in range(len(groups)+1):
            grouped_items.append([])
        no_grp_index = len(groups)
        
        # main loop
        for key, value in items:
            group_id = _get_group_id(key)
            if group_id is None:
                grouped_items[no_grp_index].append((key,value))
            else:
                grouped_items[group_id].append((key,value))
        
        # return result
        result = []
        for x in grouped_items:
            result.extend(x)
        
        # Move references to the start
        ref_index = None
        for index, item in enumerate(result):
            if item[0].lower()=="references":
                ref_index = index
        if ref_index is not None:
            ref_item = result.pop(ref_index)
            result.append(ref_item)
        
        return result

                        

                            
        

    def add_title(self, title):
        print("Adding title")
        text = QGraphicsTextItem()
        # I guess we should use a style sheet here,
        # but it seems like it'd be overkill.
        html_str = '<p style="font-size: 14pt; color: black; face:verdana">%s</p>' % title
        text.setHtml(html_str)
        #text.setPos(self.position())
        print "  title at: %s" % self.y_coord
        self.scene.addItem(text)
        qt_item = QTreeWidgetItem(self.nav_tree, [title])
        self.scene.setSceneRect(0, 0, self.scene.width(), self.y_coord + text.boundingRect().height() + padding)
        print("  Setting position at (%d,%d)" % (self.x_coord, self.y_coord))                        
        text.setPos(self.position()) #####
        self.y_coord += text.boundingRect().height()
        return qt_item

    def item_clicked(self, item, column):
        print self.items_to_coords[item]
        self.graphics_view.centerOn(self.items_to_coords[item])

    def create_text_item(self, text, position):
        txt_item = QGraphicsTextItem(QString(text))
        txt_item.setFont(QFont("courier", 12))
        txt_item.setToolTip("To copy the text:\n1) Right click on the text and choose \"Select All\".\n2) Right click again and choose \"Copy\".")
        txt_item.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.scene.addItem(txt_item)

        self.scene.setSceneRect(0, 0, max(self.scene.width(),
                                          txt_item.boundingRect().size().width()),
                                          self.y_coord+txt_item.boundingRect().height()+padding)
        
        self.y_coord += txt_item.boundingRect().height()
        txt_item.setPos(position)
        
        return (txt_item.boundingRect(), position)

    def process_console_input(self):
        res = str(python_to_R.execute_in_R(self.current_line()))

        # echo the result
        self.psuedo_console.append(QString(res))
        self.psuedo_console.append(">> ")

    def current_line(self):
        last_line = self.psuedo_console.toPlainText().split("\n")[-1]
        return str(last_line.replace(">>", "")).strip()

    def _get_plot_type(self, title):
        # at present we use the *title* as the type --
        # this is currently _not_ set by the user, so it's
        # 'safe', but it's not exactly elegant. probably
        # we should return a type directly from R.
        # on other hand, this couples R + Python even
        # more...
        plot_type = None
        tmp_title = title.lower()
        if "forest" in tmp_title:
            plot_type = "forest"
        elif "regression" in tmp_title:
            plot_type = "regression"
        elif "funnel" in tmp_title:
            plot_type = "funnel"
        return plot_type

    def create_pixmap_item(self, pixmap, position, title, image_path,\
                             params_path=None, matrix=QMatrix()):
        item = QGraphicsPixmapItem(pixmap)
        item.setToolTip("To save the image:\nright-click on the image and choose \"save image as\".\nSave as png will correctly render non-latin fonts but does not respect changes to plot made through 'edit_plot ...'")
        
        self.y_coord += item.boundingRect().size().height()
#        item.setFlags(QGraphicsItem.ItemIsSelectable|
#                      QGraphicsItem.ItemIsMovable)
        item.setFlags(QGraphicsItem.ItemIsSelectable)


        self.scene.setSceneRect(0, 0,
                                max(self.scene.width(),
                                    item.boundingRect().size().width()),
                                self.y_coord+item.boundingRect().size().height()+padding)

        print "creating item @:%s" % position
        
        item.setMatrix(matrix)
        self.scene.clearSelection()
        self.scene.addItem(item)
        item.setPos(position)
        
        # for now we're inferring the plot type (e.g., 'forest'
        # from the title of the plot (see in-line comments, above)
        plot_type = self._get_plot_type(title)

        # attach event handler for mouse-clicks, i.e., to handle
        # user right-clicks
        item.contextMenuEvent = self._make_context_menu(
                params_path, title, image_path, item, plot_type=plot_type)

        return (item.boundingRect().size(), position, item)




    def _make_context_menu(self, params_path, title, png_path, 
                           qpixmap_item, plot_type="forest"):
        plot_img = QImage(png_path)
        
        print("plot_img: %s" % plot_img)
        def _graphics_item_context_menu(event):
            def add_save_as_pdf_menu_action(menu):
                action = QAction("save pdf image as...", self)
                QObject.connect(action, SIGNAL("triggered()"),
                                lambda : self.save_image_as(params_path, title, 
                                plot_type=plot_type, format="pdf"))
                menu.addAction(action)
            def add_save_as_png_menu_action(menu):
                action = QAction("save png image as...", self)
                QObject.connect(action, SIGNAL("triggered()"),
                            lambda : self.save_image_as(params_path, title, 
                                            plot_type=plot_type,
                                            unscaled_image = plot_img, format="png"))
                menu.addAction(action)
            def add_edit_plot_menu_action(menu):
                # only know how to edit *simple* (i.e., _not_ side-by-side, as 
                # in sens and spec plotted on the same canvass) forest plots for now
                if plot_type == "forest" and not self._is_side_by_side_fp(title):
                    action = QAction("edit plot...", self)
                    QObject.connect(action, SIGNAL("triggered()"),
                            lambda : self.edit_image(params_path, title,
                                                     png_path, qpixmap_item))
                    menu.addAction(action)
                
            
            context_menu = QMenu(self)
            if params_path:
                add_save_as_pdf_menu_action(context_menu)
                add_save_as_png_menu_action(context_menu) 
                add_edit_plot_menu_action(context_menu)
            else: # no params path given, just give them the png
                add_save_as_png_menu_action(context_menu)

            pos = event.screenPos()
            context_menu.popup(pos)
            event.accept()

        return _graphics_item_context_menu


    def _is_side_by_side_fp(self, title):
        return any([side_by_side in title for side_by_side in SIDE_BY_SIDE_FOREST_PLOTS])

    def save_image_as(self, params_path, title, plot_type="forest", unscaled_image=None, format="png"):
        
        if format not in ["pdf","png"]:
            raise Exception("Invalid format, needs to be either pdf or png!")
        
        print("unscaled_image: %s" % str(unscaled_image))
        #if not unscaled_image:
        # note that the params object will, by convention,
        # have the (generic) name 'plot.data' -- after this
        # call, this object will be in the namespace
        python_to_R.load_in_R("%s.plotdata" % params_path)
        print("Loaded: %s" % "%s.plotdata" % params_path)

        suffix = unicode("."+format)
        default_filename = {"forest":"forest_plot", \
                            "regression":"regression"}[plot_type] + suffix
        
                        
        default_path = os.path.join(BASE_PATH, default_filename)
        print("default_path for graphic: %s" % default_path)
        default_path = QString(default_path)
        default_path
        
        filter = format + " files (*." + format +")"
        print("filter: %s" % filter)

        # where to save the graphic?
        file_path = unicode(QFileDialog.getSaveFileName(self, 
                                                        "OpenMeta[Analyst] -- save plot as",
                                                        default_path,))
                                                        #filter=QString(filter)))

        # now we re-generate it, unless they canceled, of course
        if file_path != "":
            if file_path[-4:] != suffix:
                file_path += suffix
                
                
            
            if plot_type == "forest":
                if self._is_side_by_side_fp(title):
                    python_to_R.generate_forest_plot(file_path, side_by_side=True)
                else:
                    python_to_R.generate_forest_plot(file_path)
            elif plot_type == "regression":
                python_to_R.generate_reg_plot(file_path)
            else:
                print "sorry -- I don't know how to draw %s plots!" % plot_type
#        else: # case where we just have the png and can't regenerate the pdf from plot data
#            print("Can't regenerate pdf")
#            default_path = '.'.join([title.replace(' ','_'),"png"])
#            file_path = unicode(QFileDialog.getSaveFileName(self, "OpenMeta[Analyst] -- save plot as", QString(default_path)))
#            unscaled_image.save(QString(file_path),"PNG")
            

    def edit_image(self, params_path, title, png_path, pixmap_item):
        plot_editor_window = edit_forest_plot_form.EditPlotWindow(\
                                            params_path, png_path,\
                                            pixmap_item, title=title, parent=self)
        if plot_editor_window is not None:
            plot_editor_window.show()
        else:
            # TODO show a warning
            print "sorry - can't edit"
        
    def position(self):
        point = QPoint(self.x_coord, self.y_coord)
        return self.graphics_view.mapToScene(point)

if __name__ == "__main__":
    
    # make test results based on results from when meta-analysis run from amino sample data
    test_results = {}
    test_results['images'] = {'Forest Plot': './r_tmp/forest.png'}
    test_results['texts'] = {'Weights':'studies             weights\nGonzalez       1993  7.3%\nPrins          1993  6.2%\nGiamarellou    1991  2.1%\nMaller         1993 10.7%\nSturm          1989  2.0%\nMarik          1991 12.2%\nMuijsken       1988  7.5%\nVigano         1992  1.8%\nHansen         1988  5.3%\nDe Vries       1990  6.1%\nMauracher      1989  2.2%\nNordstrom      1990  5.3%\nRozdzinski     1993 10.3%\nTer Braak      1990  8.7%\nTulkens        1988  1.2%\nVan der Auwera 1991  2.0%\nKlastersky     1977  6.0%\nVanhaeverbeek  1993  1.2%\nHollender      1989  1.8%\n',
                             'Summary':'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Estimate  Lower bound   Upper bound   p-Value  \n\n 0.770        0.485         1.222       0.267   \n\n\n Heterogeneity\n\n tau^2  Q(df=18)   Het. p-Value   I^2  \n\n 0.378   33.360        0.015      46%  \n\n\n Results (log scale)\n\n Estimate  Lower bound   Upper bound   Std. error  \n\n -0.262      -0.724         0.200         0.236    \n\n\n'
                            }
    test_results['image_var_names'] = {'forest plot': 'forest_plot'}
    test_results['image_params_paths'] = {'Forest Plot': 'r_tmp/1369769105.72079'} # change this number as necessary
    test_results['image_order'] = None
    
    
    app = QApplication(sys.argv)
    resultswindow = ResultsWindow(test_results)
    resultswindow.show()
    sys.exit(app.exec_())