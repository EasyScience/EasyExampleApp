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

    get fitablesListAsXml() {
        return "<root><item><number>1</number><label>amplitude</label><value>3.5</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>2</number><label>period</label><value>3.141592653589793</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>3</number><label>x_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>4</number><label>y_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item></root>"
    }

    get fitablesDict() {
        return {'amplitude': 3.5, 'period': 3.141592653589793, 'x_shift': 0.0, 'y_shift': 0.0}
    }

    get constraintsListAsXml() {
        return "<root><item><number>1</number><dependentName>amplitude</dependentName><relationalOperator>=</relationalOperator><value>1.0000</value><arithmeticOperator>*</arithmeticOperator><independentName>period</independentName><enabled>1</enabled></item><item><number>2</number><dependentName>amplitude</dependentName><relationalOperator>&lt;</relationalOperator><value>4.0000</value><arithmeticOperator></arithmeticOperator><independentName></independentName><enabled>1</enabled></item></root>"
    }

    get projectInfoAsJson() {
        return {"calculations":"experiments.cif","experiments":"experiments.cif","keywords":"sine, cosine, lmfit, bumps","modified":"18.09.2020, 09:24","name":"Example Project","samples":"samples.cif"}
    }

    // Functions

    addLowerMeasuredSeriesRef(series) {}

    addUpperMeasuredSeriesRef(series) {}

    setCalculatedSeriesRef(series) {}

    updateCalculatedData() {}

    generateMeasuredData() {}

    startFitting() {}

    editFitableValueByName(name, value) {}

    editFitableByIndexAndName(index, name, value) {}

    addConstraints(dependent_par_idx, operator, independent_par_idx) {}

    removeConstraintByIndex(index) {}

    toggleConstraintByIndex(index, enabled) {}

    editProjectInfoByKey(key, value) {}

}
