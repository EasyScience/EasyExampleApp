function line(xArray, slope, yIntercept) {
    return xArray.map(x => slope * x + yIntercept)
}

function lineMeas(xArray, slope, yIntercept) {
    return xArray.map(x => slope * x + yIntercept + randomUniform(-0.1, 0.1))
}

function randomUniform(min, max) {
    return Math.random() * (max - min) + min
}
