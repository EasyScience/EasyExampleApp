import easyAppGui.Globals 1.0 as EaGlobals

import Gui.Components 1.0 as ExComponents
import Gui.Globals 1.0 as ExGlobals

ExComponents.DataChartView {
    visible: ExGlobals.Variables.analysisPageEnabled

    showMeasured: true
}
