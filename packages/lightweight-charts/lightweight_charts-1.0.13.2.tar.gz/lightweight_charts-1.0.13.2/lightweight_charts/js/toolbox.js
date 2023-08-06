

class ToolBox {
    constructor(chart) {
        this.onTrendSelect = this.onTrendSelect.bind(this)

        this.chart = chart
        this.chart.trendLines = []
        this.chart.cursor = 'default'

        this.interval = 24*60*60*1000
        this.activeBackgroundColor = 'rgba(0, 122, 255, 0.7)'
        this.activeIconColor = 'rgb(240, 240, 240)'
        this.iconColor = 'lightgrey'
        this.backgroundColor = 'transparent'
        this.hoverColor = 'rgba(60, 60, 60, 0.7)'

        this.elem = this.makeToolBox()

    }
    makeToolBox() {
        let toolBoxElem = document.createElement('div')
        toolBoxElem.style.position = 'absolute'
        toolBoxElem.style.zIndex = '2000'
        toolBoxElem.style.display = 'flex'
        toolBoxElem.style.alignItems = 'center'
        toolBoxElem.style.top = '30%'
        toolBoxElem.style.borderRight = '2px solid #3C434C'
        toolBoxElem.style.borderTop = '2px solid #3C434C'
        toolBoxElem.style.borderBottom = '2px solid #3C434C'
        toolBoxElem.style.borderTopRightRadius = '4px'
        toolBoxElem.style.borderBottomRightRadius = '4px'
        toolBoxElem.style.backgroundColor = 'rgba(25, 27, 30, 0.5)'
        toolBoxElem.style.flexDirection = 'column'

        this.chart.activeIcon = null

        let testT = this.makeToolBoxElement(this.onTrendSelect, `<rect x="3.84" y="13.67" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -5.9847 14.4482)" width="21.21" height="1.56"/><path d="M23,3.17L20.17,6L23,8.83L25.83,6L23,3.17z M23,7.41L21.59,6L23,4.59L24.41,6L23,7.41z"/><path d="M6,20.17L3.17,23L6,25.83L8.83,23L6,20.17z M6,24.41L4.59,23L6,21.59L7.41,23L6,24.41z"/>`)
        let testH = this.makeToolBoxElement(this.onTrendSelect, `<rect x="4" y="14" width="9" height="1"/><rect x="16" y="14" width="9" height="1"/><path d="M11.67,14.5l2.83,2.83l2.83-2.83l-2.83-2.83L11.67,14.5z M15.91,14.5l-1.41,1.41l-1.41-1.41l1.41-1.41L15.91,14.5z"/>`)
        let testR = this.makeToolBoxElement(this.onTrendSelect, `<rect x="8" y="14" width="17" height="1"/><path d="M3.67,14.5l2.83,2.83l2.83-2.83L6.5,11.67L3.67,14.5z M7.91,14.5L6.5,15.91L5.09,14.5l1.41-1.41L7.91,14.5z"/>`)
        let testB = this.makeToolBoxElement(this.onTrendSelect, `<rect x="8" y="6" width="12" height="1"/><rect x="9" y="22" width="11" height="1"/><path d="M3.67,6.5L6.5,9.33L9.33,6.5L6.5,3.67L3.67,6.5z M7.91,6.5L6.5,7.91L5.09,6.5L6.5,5.09L7.91,6.5z"/><path d="M19.67,6.5l2.83,2.83l2.83-2.83L22.5,3.67L19.67,6.5z M23.91,6.5L22.5,7.91L21.09,6.5l1.41-1.41L23.91,6.5z"/><path d="M19.67,22.5l2.83,2.83l2.83-2.83l-2.83-2.83L19.67,22.5z M23.91,22.5l-1.41,1.41l-1.41-1.41l1.41-1.41L23.91,22.5z"/><path d="M3.67,22.5l2.83,2.83l2.83-2.83L6.5,19.67L3.67,22.5z M7.91,22.5L6.5,23.91L5.09,22.5l1.41-1.41L7.91,22.5z"/><rect x="22" y="9" width="1" height="11"/><rect x="6" y="9" width="1" height="11"/>`)
        toolBoxElem.appendChild(testT)
        toolBoxElem.appendChild(testH)
        toolBoxElem.appendChild(testR)
        toolBoxElem.appendChild(testB)

        this.chart.wrapper.append(toolBoxElem)

        document.addEventListener('keydown',  (event) => {
            if (event.metaKey && event.code === 'KeyZ') {
                this.chart.chart.removeSeries(this.chart.trendLines[this.chart.trendLines.length - 1].line);
                this.chart.trendLines.splice(this.chart.trendLines.length - 1)
            }
        });
        return toolBoxElem
    }
    makeToolBoxElement(action, paths) {
        let elem = document.createElement('div')
        elem.style.margin = '3px'
        elem.style.borderRadius = '4px'
        elem.style.display = 'flex'

        let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("width", "29");
        svg.setAttribute("height", "29");

        let group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.innerHTML = paths
        group.setAttribute("fill", this.iconColor)

        svg.appendChild(group)
        elem.appendChild(svg);

        elem.addEventListener('mouseenter', () => {
            elem.style.backgroundColor = elem === this.chart.activeIcon ? this.activeBackgroundColor : this.hoverColor
            document.body.style.cursor = 'pointer'
        })
        elem.addEventListener('mouseleave', () => {
            elem.style.backgroundColor = elem === this.chart.activeIcon ? this.activeBackgroundColor : this.backgroundColor
            document.body.style.cursor = this.chart.cursor
        })
        elem.addEventListener('click', () => {
            if (this.chart.activeIcon) {
                this.chart.activeIcon.style.backgroundColor = this.backgroundColor
                group.setAttribute("fill", this.iconColor)
                action(false, this.backgroundColor)
            }
            if (this.chart.activeIcon === elem) {
                this.chart.activeIcon = null
                return
            }
            this.chart.activeIcon = elem
            group.setAttribute("fill", this.activeIconColor)
            elem.style.backgroundColor = this.activeBackgroundColor
            action(true, this.backgroundColor)
        })
        document.addEventListener('keydown',  (event) => {
            if (event.altKey && event.code === 'KeyT') {

                if (this.chart.activeIcon) {
                    this.chart.activeIcon.style.backgroundColor = this.backgroundColor
                    group.setAttribute("fill", this.iconColor)
                    action(false, this.backgroundColor)
                }
                this.chart.activeIcon = elem
                group.setAttribute("fill", this.activeIconColor)
                elem.style.backgroundColor = this.activeBackgroundColor
                action(true, this.backgroundColor)
            }
        })
        return elem
    }
    onTrendSelect(toggle, inactiveBackgroundColor) {
        let trendLine = {
            line: null,
            markers: null,
            data: null,
        }
        let firstTime = null
        let firstPrice = null
        let currentTime = null
        let makingTrend = false
        document.body.style.cursor = 'crosshair'
        this.chart.cursor = 'crosshair'

        if (!toggle) {
            this.chart.chart.unsubscribeClick(this.chart.clickHandler)
            return
        }

        let crosshairHandlerTrend = (param) => {
            this.chart.chart.unsubscribeCrosshairMove(crosshairHandlerTrend)

            if (!makingTrend) return
            if (!param.point) return this.chart.chart.subscribeCrosshairMove(crosshairHandlerTrend)


            let currentPrice = this.chart.series.coordinateToPrice(param.point.y)
            currentTime = this.chart.chart.timeScale().coordinateToTime(param.point.x)

            if (!currentTime) return this.chart.chart.subscribeCrosshairMove(crosshairHandlerTrend)

            trendLine.data = calculateTrendLine(firstTime, firstPrice, currentTime, currentPrice, this.interval, this.chart)
            trendLine.line.setData(trendLine.data)

            trendLine.markers = [
                {time: firstTime, position: 'inBar', color: '#1E80F0', shape: 'circle', size: 0.1},
                {time: currentTime, position: 'inBar', color: '#1E80F0', shape: 'circle', size: 0.1}
            ]
            trendLine.line.setMarkers(trendLine.markers)

            setTimeout(() => {
                this.chart.chart.subscribeCrosshairMove(crosshairHandlerTrend)
            }, 5);
        }

        this.chart.clickHandler = (param) => {
            if (!makingTrend) {
                makingTrend = true
                trendLine.line = this.chart.chart.addLineSeries({
                    lineWidth: 2,
                    lastValueVisible: false,
                    priceLineVisible: false,
                    crosshairMarkerVisible: false,
                    autoscaleInfoProvider: () => ({
                        priceRange: {
                            minValue: 1_000_000_000,
                            maxValue: 0,
                        },
                    }),
                })
                firstPrice = this.chart.series.coordinateToPrice(param.point.y)
                firstTime = this.chart.chart.timeScale().coordinateToTime(param.point.x)
                this.chart.chart.subscribeCrosshairMove(crosshairHandlerTrend)
            }
            else {
                makingTrend = false
                trendLine.line.setMarkers([])
                this.chart.trendLines.push(trendLine)
                this.chart.chart.unsubscribeCrosshairMove(crosshairHandlerTrend)
                this.chart.chart.unsubscribeClick(this.chart.clickHandler)
                document.body.style.cursor = 'default'
                this.chart.cursor = 'default'
                this.chart.activeIcon.style.backgroundColor = inactiveBackgroundColor
                this.chart.activeIcon = null
            }
        }
        this.chart.chart.subscribeClick(this.chart.clickHandler)
        let hoveringOver = null


        let hoverOver = (param) => {
            if (!param) return
            this.chart.chart.unsubscribeCrosshairMove(hoverOver)
            this.chart.trendLines.forEach((trendLine) => {
                let trendData = param.seriesData.get(trendLine.line);
                if (!trendData) {return}
                if (Math.abs(this.chart.series.priceToCoordinate(trendData.value) - param.point.y) < 4) {
                    document.body.style.cursor = 'pointer'
                    if (hoveringOver !== trendLine) {
                        trendLine.line.setMarkers(trendLine.markers)
                        this.chart.chart.subscribeClick(checkForClick)
                    }
                    hoveringOver = trendLine
                }
                else if (hoveringOver === trendLine) {
                    hoveringOver = null
                    this.chart.chart.unsubscribeClick(checkForClick)
                    trendLine.line.setMarkers([])
                    document.body.style.cursor = this.chart.cursor
                }
            })
            this.chart.chart.subscribeCrosshairMove(hoverOver)
        }
        let originalIndex = null
        let originalPrice = null
        let checkForClick = (param) => {
            console.log('CLICKED IT!')
            this.chart.chart.subscribeCrosshairMove(checkForDrag)
            this.chart.chart.unsubscribeCrosshairMove(hoverOver)
            originalIndex = param.logical
            originalPrice = this.chart.series.coordinateToPrice(param.point.y)
            this.chart.chart.unsubscribeClick(checkForClick)
        }
        let checkForDrag = (param) => {
            if (!param) return
            this.chart.chart.unsubscribeCrosshairMove(checkForDrag)

            let priceAtCursor = this.chart.series.coordinateToPrice(param.point.y)

            let priceDiff = priceAtCursor-originalPrice
            let barsToMove = param.logical-originalIndex

            let startBar = this.chart.candleData[this.chart.candleData.findIndex(item => equalObjects(item.time, hoveringOver.data[0].time))+barsToMove]
            let endBar = this.chart.candleData[this.chart.candleData.findIndex(item => equalObjects(item.time, hoveringOver.data[hoveringOver.data.length-1].time))+barsToMove]

            let startDate = startBar.time
            let startValue = hoveringOver.data[0].value + priceDiff
            let endDate = endBar.time
            let endValue = hoveringOver.data[hoveringOver.data.length-1].value + priceDiff

            hoveringOver.data = calculateTrendLine(startDate, startValue, endDate, endValue, this.interval, this.chart)

            hoveringOver.line.setData(hoveringOver.data)
            originalIndex = param.logical
            originalPrice = priceAtCursor
            this.chart.chart.subscribeCrosshairMove(checkForDrag)
        }
        this.chart.chart.subscribeCrosshairMove(hoverOver)
    }
}
window.ToolBox = ToolBox

function chartTimeToDate(stampOrBusiness) {
    if (typeof stampOrBusiness === 'number') {
        stampOrBusiness = new Date(stampOrBusiness*1000)
    }
    else if (typeof stampOrBusiness === 'string') {
        let [year, month, day] = stampOrBusiness.split('-').map(Number)
        stampOrBusiness = new Date(year, month-1, day)
    }
    else {
        stampOrBusiness = new Date(stampOrBusiness.year, stampOrBusiness.month - 1, stampOrBusiness.day);
    }
    return stampOrBusiness
}

function dateToChartTime(date, interval) {
    if (interval >= 24*60*60*1000) {
        return {day: date.getDate(), month: date.getMonth()+1, year: date.getFullYear()}
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        return `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`;

    }
    return Math.floor(date.getTime()/1000)
}

function equalObjects(obj1, obj2) {
  const keys1 = Object.keys(obj1);
  for (let key of keys1) {
    if (obj1[key] !== obj2[key]) return false
  }
  return true;
}

function calculateTrendLine(startDate, startValue, endDate, endValue, interval, chart) {
    let reversed = false
    if (chartTimeToDate(endDate) < chartTimeToDate(startDate)) {
        reversed = true;
        [startDate, endDate] = [endDate, startDate];
    }

    let startIndex = chart.candleData.findIndex(item => equalObjects(item.time, startDate))
    let endIndex = chart.candleData.findIndex(item => equalObjects(item.time, endDate))
    let numBars = endIndex-startIndex

    const rate_of_change = (endValue - startValue) / numBars;

    const trendData = [];
    for (let i = 0; i <= numBars; i++) {
        const currentDate = chart.candleData[startIndex+i].time
        const currentValue = reversed ? startValue + rate_of_change * (numBars - i) : startValue + rate_of_change * i;
        trendData.push({ time: currentDate, value: currentValue });
    }
    return trendData;
}
