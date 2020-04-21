import os
import sip
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import (
    QgsDataCollectionItem,
    QgsDataItemProvider,
    QgsDataProvider
)

from .browser_rastermaps import RasterCollection
#from .browser_vectormaps import VectorCollection

from .configue_dialog import ConfigueDialog

ICON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

class DataItemProvider(QgsDataItemProvider):
    def __init__(self):
        QgsDataItemProvider.__init__(self)

    def name(self):
        return "MapTilerProvider"

    def capabilities(self):
        return QgsDataProvider.Net

    def createDataItem(self, path, parentItem):
        root = RootCollection()
        sip.transferto(root, None)
        return root

class RootCollection(QgsDataCollectionItem):
    def __init__(self):
        QgsDataCollectionItem.__init__(self, None, "MapTiler", "/MapTiler")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "maptiler_icon.svg")))
    
    def createChildren(self):
        #init default dataset
        raster_standard_dataset = {
            'Basic':r'https://api.maptiler.com/maps/basic/256/{z}/{x}/{y}.png?key=',
            'Bright':r'https://api.maptiler.com/maps/bright/256/{z}/{x}/{y}.png?key='
        }
        raster_local_dataset = {
            'JP MIERUNE Street':r'https://api.maptiler.com/maps/jp-mierune-streets/256/{z}/{x}/{y}.png?key='
        }
        vector_standard_collection = {
            'Basic':r'https://api.maptiler.com/tiles/v3/{z}/{x}/{y}.pbf?key='
        }
        #init Collections
        raster_standard_collection = RasterCollection('Standard raster tile', raster_standard_dataset)
        raster_local_collection = RasterCollection('Local raster tile', raster_local_dataset)
        raster_user_collection = RasterCollection('User raster tile', {}, user_editable=True)
        #vector_standard_collection = VectorCollection('Standard Vector tile', vector_standard_collection)

        sip.transferto(raster_standard_collection, self)
        sip.transferto(raster_local_collection, self)
        sip.transferto(raster_user_collection, self)
        #sip.transferto(vector_standard_collection, self)

        return [raster_standard_collection, raster_local_collection, raster_user_collection]
        #return [raster_standard_collection, raster_local_collection, raster_user_collection, vector_standard_collection]

    def actions(self, parent):
        actions = []

        configue_action = QAction(QIcon(), 'Configue', parent)
        configue_action.triggered.connect(self.open_configue_dialog)
        actions.append(configue_action)

        return actions

    def open_configue_dialog(self):
        configue_dialog = ConfigueDialog()
        configue_dialog.exec_()