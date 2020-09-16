class PyQmlProxy {

    // Properties

    get calculatorList() {
        return ["calculator1"]
    }

    get calculatorIndex() {
        return 0
    }

    get minimizerList() {
        return ["minimizer1"]
    }

    get minimizerIndex() {
        return 0
    }

    get amplitude() {
        return 3.5
    }

    get period() {
        return 2.0
    }

    get xShift() {
        return 0
    }

    get yShift() {
        return 0
    }

    get statusModelAsXml() {
        return "<root><item><label>Calculator</label><value>calculator1</value></item><item><label>Minimizer</label><value>minimizer1</value></item></root>"
    }

    // Functions

    addLowerMeasuredSeriesRef(series) {}

    addUpperMeasuredSeriesRef(series) {}

    setCalculatedSeriesRef(series) {}

    updateCalculatedData() {}

    generateMeasuredData() {}

    startFitting() {}
}
