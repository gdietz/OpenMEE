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

#import pdb
#import os
import sys
import ui_results_window
import edit_forest_plot_form
import edit_phylo_forest_plot_form
import python_to_R
#import shutil

from ome_globals import *
from edit_funnel_plot_form import EditFunnelPlotForm
from edit_data_exploration_plot_form import EditDataExplorationPlotForm

builddatestr = 'OpenMEE build date: %s' % get_build_date()

PageSize = (612, 792)
padding = 15 # padding between items
SCALE_P = .5 # percent images are to be scaled

# these are special forest plots, in that multiple parameters objects are
# require to re-generate them (and we invoke a different method!)
SIDE_BY_SIDE_FOREST_PLOTS = ("NLR and PLR Forest Plot", "Sensitivity and Specificity","Cumulative Forest Plot")

# TODO: Put all the titles + text or title + images into QGraphicsItemGroups

class ResultsWindow(QMainWindow, ui_results_window.Ui_ResultsWindow):

    def __init__(self, results, show_additional_values, show_analysis_selections, summary="", parent=None):
        super(ResultsWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.texts_for_export = [] # text for export not included 'additional values'
        self.show_additional_values = show_additional_values
        self.show_analysis_selections = show_analysis_selections
        self.items_to_ignore = []
        #self.copied_item = QByteArray()
        #self.paste_offset = 5
        #self.add_offset = 5
        self.prev_point = QPoint()
        self.borders = []
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageSize(QPrinter.Letter)
        self.summary=summary

        QObject.connect(self.nav_tree, SIGNAL("itemClicked(QTreeWidgetItem*, int)"),
                                       self.item_clicked)
        
        if "results_data" not in results:
            results["results_data"] = None
        self.export_btn.clicked.connect(lambda: self.export_results(results["results_data"]))
        
        self.nav_tree.setHeaderLabels(["results"])
        self.nav_tree.setItemsExpandable(True)
        self.x_coord = 5
        self.y_coord = 5

        # set (default) splitter sizes
        self.results_nav_splitter.setSizes([200,500])

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
        
        self.items_to_coords = {}
        self.texts = results["texts"]

        self.groupings = [["Likelihood","nlr","plr"],
                          ["sens","spec"],
                          ["Subgroup",],
                          ["Cumulative",],
                          ["Leave-one-out",],]

        # first add the text to self.scene
        self.post_facto_text_to_add = []
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        # Add build date to output
        self._add_text_item(None, builddatestr)
        self.add_text() # adds the body of the text output

        # and now the images
        self.add_images()
        
        # Add post-facto text items (for now, just the references)
        for title, text in self.post_facto_text_to_add:
            self._add_text_item(title, text)
            self.texts_for_export.append((title, text))

        # reset the scene
        self.graphics_view.setScene(self.scene)
        self.graphics_view.ensureVisible(QRectF(0,0,0,0))

        print "Results: %s" % str(results)

        if "results_data" in results and islistortuple(results["results_data"]) and len(results["results_data"]) > 0:
            if self.show_additional_values:
                self.add_additional_values_texts(results["results_data"])
            else:
                # issue #152 show 'k' regardless
                self.add_additional_values_texts(results["results_data"],ADDITIONAL_VALUES_TO_ALWAYS_SHOW, additionalvaluesparent=False)


    def f(self):
        print self.current_line()
        
    def export_results(self, data):
        # Choose file location
        fpath = os.path.join(get_user_desktop_path(), "results.txt") # default
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
        
        # write the file
        with open(fpath,'w') as f:
            # Version
            f.write ("%s\n\n" % boxify(builddatestr))

            # Add input summary
            if self.show_analysis_selections:
                if len(self.summary) > 0:
                    f.write("%s\n" % boxify("Analysis selections summary"))
                    f.write(boxify(self.summary))
                    f.write("\n\n")
            
            # Output summary
            for title, text in self.texts_for_export:
                f.write("%s\n" % boxify(title))
                f.write(text)
                f.write("\n\n")
            
            # Additional Values    
            if self.show_additional_values:
                f.write("%s\n" % boxify("Additional Values"))
                for key, value_data in data:
                    f.write("%s: %s\n" % (key, value_data['description'])) # write out key and description
                    val_str = self._value_to_string(value_data['value'])
                    f.write(val_str)
                    # add space between values
                    f.write("\n")
        
        self.statusbar.showMessage("Saved results to: %s" % fpath,5000)
        
    def _value_to_string(self, value):
        if isinstance(value, str):
            val_str = value+"\n"
        elif isinstance(value, list):
            val_str = ""
            for x in value:
                val_str+= "%s\n" % x
        else:
            raise TypeError("Unrecognized type in data")
        
        return val_str

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
            ordered_images = grouped_images

        for title,image in ordered_images:
            # first add the title
            qt_item = self.add_title(self.purified_title_str(title))
            
            # custom scales to which special plots should be scaled
            title_contents_to_scale = {"histogram":1,
                                       "funnel":1,
                                       "scatterplot":1,
                                       "forest plot of coefficients":1,
                                       }
            for title_contents, scale in title_contents_to_scale.items():
                if title.lower().rfind(title_contents) != -1:
                    print("using scale=%d" % scale)
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

            self.create_pixmap_item(pixmap, self.position(), title, image, params_path=params_path)

            self.items_to_coords[qt_item] = self.position()
            self.y_coord += padding
            
    def purified_title_str(self, title):
        ''' strips out metadata from title i.e. if title is "Forest Plot__phlyo",
        this strips out the __phylo '''
        
        try:
            metadata_index = title.index("__")
        except ValueError:
            return title
        
        return title[0:metadata_index]

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

        pixmap = pixmap.scaled(scaled_width, scaled_height, transformMode=Qt.SmoothTransformation)

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
            # append to texts for export:
            self.texts_for_export.append((title,text))
    
            
    def add_additional_values_texts(self, data, keys_to_display=None, additionalvaluesparent=True, sublist_prefix="__"):
        ''' Creates text items for the additional values and makes them children
        of an 'Additional Values' item in the nav tree.
            keys_to_display: List of keys to always display regardless of
                whether self.show_additional_values is true or false
                If None, all keys are displayed. If not None, only the listed
                keys are displayed.
            additionalvaluesparent: display the additional values under a parent
                item on the left side of the results window
        '''
        if additionalvaluesparent:
            spacer_item = self._add_text_item("", "\n\n--------------------------------------------------")
            additional_values_item = QTreeWidgetItem(self.nav_tree, ["Additional Values"])
            self.items_to_ignore.extend([spacer_item, additional_values_item])
        else:
            additional_values_item = None

        len_sublist_prefix = len(sublist_prefix)
        current_parent = additional_values_item

        for key,value_data in data:
            if keys_to_display and key not in keys_to_display:
                continue
            val_str = self._value_to_string(value_data['value'])
            if key[0:len_sublist_prefix] == sublist_prefix:
                print("Sublist detectected")
                #current_parent = QTreeWidgetItem(additional_values_item,[key[len_sublist_prefix:]])
                current_parent = self._add_text_item(key[len_sublist_prefix:], val_str, parent_item=additional_values_item)
                #self.items_to_ignore.append(current_parent)
            else:
                self._add_text_item(key+": %s" % value_data['description'], val_str, parent_item=current_parent)
            
    def _add_text_item(self, title, text, parent_item=None):
        '''
        parent_item is the parent item in the nav tree
        If title is none, no title is created and no reference to the added item is returned.
        '''

        text = text.replace("\\n","\n") # manual escaping
        if title:
            # first add the title
            qt_item = self.add_title(title, parent_item)

        # now the text
        position = self.position()
        self.create_text_item(unicode(text), position)
        if title:
            self.items_to_coords[qt_item] = position

        # add padding to the next item
        self.y_coord += padding
        if title:
            return qt_item # returns the item in the nav tree
    
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

    def add_title(self, title, parent_item=None):
        text = QGraphicsTextItem()
        # I guess we should use a style sheet here,
        # but it seems like it'd be overkill.
        html_str = '<p style="font-size: 14pt; color: black; face:verdana">%s</p>' % title
        text.setHtml(html_str)
        self.scene.addItem(text)
        if parent_item:
            qt_item = QTreeWidgetItem(parent_item, [title])
        else:
            qt_item = QTreeWidgetItem(self.nav_tree, [title])
        text.setPos(self.x_coord, self.y_coord)
        self.y_coord += text.boundingRect().height()
        return qt_item

    def item_clicked(self, item, column):
        if item in self.items_to_ignore:
            return
        print self.items_to_coords[item]
        self.graphics_view.centerOn(self.items_to_coords[item])

    def create_text_item(self, text, position):
        txt_item = QGraphicsTextItem()
        # This is a dumb way to escape the text for conversion to html but it works for now
        text = text.replace('\r','')
        text = text.replace('<', '&lt;')
        text = text.replace('\n', '<br />')

        # we should use a mono-width font here
        html_str = '<pre>%s</pre>' % text
        txt_item.setHtml(html_str)
        font = QFont(QString('monospace'),12)
        txt_item.setFont(font)

        txt_item.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.scene.addItem(txt_item)
        txt_item.setPos(self.x_coord, self.y_coord)
        txt_item.setToolTip("To copy the text:\n1) Right click on the text and choose \"Select All\".\n2) Right click again and choose \"Copy\".")
        self.y_coord += txt_item.boundingRect().height()
    
    def _get_plot_type(self, title):
        # at present we use the *title* as the type --
        # this is currently _not_ set by the user, so it's
        # 'safe', but it's not exactly elegant. probably
        # we should return a type directly from R.
        # on other hand, this couples R + Python even
        # more...
        plot_type = None
        tmp_title = title.lower()
        if "forest plot of coefficients" in tmp_title:
            plot_type = "forest plot of coefficients"
        elif "forest" in tmp_title and "__phylo" in tmp_title:
            plot_type = "forest__phylo"
        elif "forest" in tmp_title:
            plot_type = "forest"
        elif "regression" in tmp_title:
            plot_type = "regression"
        elif "funnel" in tmp_title:
            plot_type = "funnel"
        elif "histogram" in tmp_title:
            plot_type = "histogram"
        elif "scatterplot" in tmp_title:
            plot_type = "scatterplot"
        return plot_type

    def create_pixmap_item(self, pixmap, position, title, image_path,
            params_path=None, matrix=QMatrix()):
        item = QGraphicsPixmapItem(pixmap)

        item.setFlags(QGraphicsItem.ItemIsSelectable)
        print "creating item @:%s" % position
        
        item.setMatrix(matrix)
        self.scene.clearSelection()
        self.scene.addItem(item)
        item.setPos(self.x_coord, self.y_coord)
        item.setToolTip("To save the image:\nright-click on the image and choose \"save image as\".\nSave as png will correctly render non-latin fonts but does not respect changes to plot made through 'edit_plot ...'")

        self.y_coord += item.boundingRect().height()
        
        # for now we're inferring the plot type (e.g., 'forest'
        # from the title of the plot (see in-line comments, above)
        plot_type = self._get_plot_type(title)

        # attach event handler for mouse-clicks, i.e., to handle
        # user right-clicks
        item.contextMenuEvent = self._make_context_menu(
                params_path, title, image_path, item, plot_type=plot_type)

    def _make_context_menu(self, params_path, title, png_path, 
                           qpixmap_item, plot_type="forest"):
        plot_img = QImage(png_path)
        
        print("plot_img: %s" % plot_img)
        def _graphics_item_context_menu(event):
            def add_save_as_pdf_menu_action(menu):
                action = QAction("save pdf image as...", self)
                QObject.connect(action, SIGNAL("triggered()"),
                                lambda : self.save_image_as(params_path, title, 
                                plot_type=plot_type, fmt="pdf"))
                menu.addAction(action)
            def add_save_as_png_menu_action(menu):
                action = QAction("save png image as...", self)
                QObject.connect(action, SIGNAL("triggered()"),
                            lambda : self.save_image_as(params_path, title, 
                                            plot_type=plot_type,
                                            unscaled_image = plot_img, fmt="png"))
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
                elif plot_type == "forest__phylo":
                    print("Is phylo forest plot")
                    action = QAction("edit plot...", self)
                    QObject.connect(action, SIGNAL("triggered()"),
                            lambda : self.edit_image(params_path, title,
                                                     png_path, qpixmap_item, plot_type=plot_type))
                    menu.addAction(action)
                elif plot_type in ["funnel","histogram","scatterplot"]:
                    action = QAction("edit plot...", self)
                    QObject.connect(action, SIGNAL("triggered()"),
                            lambda : self.edit_image(params_path, title,
                                                     png_path, qpixmap_item, plot_type=plot_type))
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

    def save_image_as(self, params_path, title, plot_type="forest", unscaled_image=None, fmt="png"):
        
        if fmt not in ["pdf","png"]:
            raise Exception("Invalid fmt, needs to be either pdf or png!")
        
        print("unscaled_image: %s" % str(unscaled_image))
        #if not unscaled_image:
        # note that the params object will, by convention,
        # have the (generic) name 'plot.data' -- after this
        # call, this object will be in the namespace
        ##if plot_type not in ["funnel", "histogram", "scatterplot", "forest__phylo"]:
        ##    python_to_R.load_in_R("%s.plotdata" % params_path)
        ##    print("Loaded: %s" % "%s.plotdata" % params_path)
        if plot_type in ["forest", "regression"]:
            python_to_R.load_in_R("%s.plotdata" % params_path)
            print("Loaded: %s" % "%s.plotdata" % params_path)
        elif plot_type == "forest plot of coefficients":
            python_to_R.load_in_R("%s.coef_fp_data" % params_path)
            print("Loaded: %s" % "%s.coef_fp_data" % params_path)

        suffix = unicode("."+fmt)
        default_filename = {"forest":"forest_plot",
                            "forest__phylo":"forest_plot",
                            "regression":"regression",
                            "funnel":"funnel_plot",
                            "histogram":"histogram",
                            "scatterplot":"scatterplot",
                            "forest plot of coefficients":"forest_plot_of_coefficients"}[plot_type] + suffix
        
                        
        default_path = os.path.join(get_user_desktop_path(), default_filename)
        print("default_path for graphic: %s" % default_path)
        default_path = QString(default_path)
        default_path
        
        dfilter = fmt + " files (*." + fmt +")"
        print("filter: %s" % dfilter)

        # where to save the graphic?
        file_path = unicode(QFileDialog.getSaveFileName(self, 
                                                        "OpenMEE -- save plot as",
                                                        default_path,))
                                                        #filter=QString(dfilter)))

        # now we re-generate it, unless they canceled, of course
        if file_path != "":
            if file_path[-4:] != suffix:
                file_path += suffix

            if plot_type == "forest":
                if self._is_side_by_side_fp(title):
                    python_to_R.generate_forest_plot(file_path, side_by_side=True)
                else:
                    python_to_R.generate_forest_plot(file_path)
            elif plot_type == "forest__phylo":
                python_to_R.regenerate_phylo_forest_plot(file_path)
            elif plot_type == "regression":
                python_to_R.generate_reg_plot(file_path)
            elif plot_type == "funnel":
                python_to_R.regenerate_funnel_plot(params_path, file_path)
            elif plot_type in ["histogram","scatterplot"]:
                python_to_R.regenerate_exploratory_plot(params_path, file_path, plot_type=plot_type)
            elif plot_type == "forest plot of coefficients":
                python_to_R.regenerate_forest_plot_of_coefficients(file_path, params_path, fmt)
            else:
                print "sorry -- I don't know how to draw %s plots!" % plot_type
#        else: # case where we just have the png and can't regenerate the pdf from plot data
#            print("Can't regenerate pdf")
#            default_path = '.'.join([title.replace(' ','_'),"png"])
#            file_path = unicode(QFileDialog.getSaveFileName(self, "OpenMeta[Analyst] -- save plot as", QString(default_path)))
#            unscaled_image.save(QString(file_path),"PNG")

            self.statusbar.showMessage("Saved image to %s" % file_path, 10000)
            

    def edit_image(self, params_path, title, png_path, pixmap_item, plot_type="forest"):
        if plot_type == "forest":
            plot_editor_window = edit_forest_plot_form.EditPlotWindow(
                                        params_path,
                                        png_path,
                                        pixmap_item,
                                        title=title,
                                        parent=self)
            if plot_editor_window is not None:
                plot_editor_window.show()
            else:
                # TODO show a warning
                print "sorry - can't edit"
        elif plot_type == "forest__phylo":
            plot_editor_window = edit_phylo_forest_plot_form.EditPhyloForestPlotWindow(
                                        params_path,
                                        png_path,
                                        pixmap_item,
                                        title=title,
                                        parent=self)
            if plot_editor_window is not None:
                plot_editor_window.show()
            else:
                # TODO show a warning
                print "sorry - can't edit"
        elif plot_type == "funnel":
            funnel_params = python_to_R.get_funnel_params(params_path)
            edit_form = EditFunnelPlotForm(funnel_params)
            if edit_form.exec_():
                new_funnel_params = edit_form.get_params()
                python_to_R.regenerate_funnel_plot(params_path, png_path, edited_funnel_params=new_funnel_params)
                new_pixmap = self.generate_pixmap(png_path, custom_scale=1)
                pixmap_item.setPixmap(new_pixmap)
        elif plot_type in ["histogram","scatterplot"]:
            params = python_to_R.get_exploratory_params(params_path)
            edit_form = EditDataExplorationPlotForm(form_type=plot_type, params=params)
            if edit_form.exec_():
                new_params = edit_form.get_params()
                python_to_R.regenerate_exploratory_plot(params_path, png_path, plot_type=plot_type, edited_params=new_params)
                new_pixmap = self.generate_pixmap(png_path, custom_scale=1)
                pixmap_item.setPixmap(new_pixmap)

    def position(self):
        point = QPoint(self.x_coord, self.y_coord)
        return point

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