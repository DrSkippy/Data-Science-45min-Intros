#!/usr/bin/env python

# imports
import os
import sys
from datetime import *


def mkdir(directoryList):
    for path in directoryList:
        if not os.path.exists(path):
            os.makedirs(path)

if __name__ == "__main__":
    # get present working directory
    pwd = os.getcwd()
    # create cs, js
    dirList = ['/js','/css','/data']
    mkdir([pwd+item for item in dirList])
    # create index.html
    htmlContent = """
<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8">
        <!-- D3 -->
        <script src="http://d3js.org/d3.v3.min.js"></script>
        <!-- Heatmap -->
        <script src="js/heatmap.js" type="text/javascript"></script>

        <!-- CSS -->
        <link href="css/style.css" type="text/css" rel="stylesheet">

        <style>
        /* CSS */
        </style>

    </head>
    <body>
        <script src="js/app.js" type="text/javascript"></script>
    </body>
</html>
"""
    # create heatmap.js
    heatmapContent = """
// Closure
(function() {
  /**
   * Decimal adjustment of a number.
   *
   * @param {String}  type  The type of adjustment.
   * @param {Number}  value The number.
   * @param {Integer} exp   The exponent (the 10 logarithm of the adjustment base).
   * @returns {Number} The adjusted value.
   */
  function decimalAdjust(type, value, exp) {
    // If the exp is undefined or zero...
    if (typeof exp === 'undefined' || +exp === 0) {
      return Math[type](value);
    }
    value = +value;
    exp = +exp;
    // If the value is not a number or the exp is not an integer...
    if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
      return NaN;
    }
    // Shift
    value = value.toString().split('e');
    value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
    // Shift back
    value = value.toString().split('e');
    return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
  }

  // Decimal round
  if (!Math.round10) {
    Math.round10 = function(value, exp) {
      return decimalAdjust('round', value, exp);
    };
  }
  // Decimal floor
  if (!Math.floor10) {
    Math.floor10 = function(value, exp) {
      return decimalAdjust('floor', value, exp);
    };
  }
  // Decimal ceil
  if (!Math.ceil10) {
    Math.ceil10 = function(value, exp) {
      return decimalAdjust('ceil', value, exp);
    };
  }
})();


// add elements in which to place the chart
function heatmap(){
  var gridSize = 50
    , margin = { top: 100, right: 0, bottom: 100, left: 130 , legend: gridSize}
    , width =1500 - margin.left - margin.right
    , height = 1500 - margin.top - margin.bottom
    , colors = ['#990000','#ff9900']
    , colorDomain = [-2,2]
    , colorScale = d3.scale.linear().domain(colorDomain).range(colors)
    , title = 'Reuseable Heatmap';

  function chart(selection){
    // the chart function builds the heatmap.
    // note: selection is passed in from the .call(myHeatmap), which is the same as myHeatmap(d3.select('.stuff')) -- ??
    selection.each(function(data){
        console.log(data)
        console.log(height)
        var columns = Object.keys(data[0]).length -1
          , rows = data.length;

        var rowLabelSet = new Set();
        data.forEach(function(d){
            rowLabelSet.add(d.row_name)
        })

        var svg = selection.append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var rowLabels = svg.selectAll(".rowLabel")
            .data(Array.from(rowLabelSet))
            .enter().append("text")
            .classed('rowLabel',true)
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize; })
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")");
            //.attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

        var colLabels = svg.selectAll(".colLabel")
            .data(d3.range(columns))
            .enter().append("text")
            .text(function(d) { return 'c'+d; })
            .attr("x", function(d, i) { return i * gridSize; })
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)");
            //.attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

        var rowElement = svg.append('g')
            .classed('row',true);

        var myRows = rowElement.selectAll('g')
            .data(data).enter()
            .append('g')
            .classed('test_rows',true);


        // add rectangles WITH a data binding

        var gTest = svg.append('g')
            .classed('gTest',true);

        // notice that we bind the data here and use a transform to adjust the y-value for each g. 
            // note: each g represents one row.
        var testGs = gTest.selectAll('g')
            .data(data)
            .enter()
            .append('g')
            .attr("transform", function(d,i) { return "translate(0," + (i * gridSize) + ")";});

        // create a selection that is ready to bind with data
            // note: d3.entries() breaks the object into an array of row elements each representing an item in that column.
        var dataBoundElements = testGs.selectAll("rect")
            .data(function(d,i) { 
              return d3.entries(d).filter(function(e) { return e.key != "row_name";});
            });

        // create the rectangles.
        var rectElements = dataBoundElements
            .enter().append("rect")
            .attr({
              x: function(d,i) { return i * gridSize;}
            , y: 0
            , width: gridSize
            , height: gridSize
            , class:"cell"
            })
            .style('fill',colors[0])
            .transition().duration(3000)
            .style('fill',function(d) {
              return colorScale( +d.value )} );

        // create text in the elements
        var textElements = dataBoundElements
            .enter().append('text')
            .attr({
              x: function(d,i) { return i * gridSize + 10;}
            , y: 0.5 * gridSize
            , class:"cellText"
            })
            .text(function(d){return Math.round10(+d.value,-1)});

        /*
        // add rectangles WITHOUT a data binding 
        data.forEach(function(d,i){
            for (col in d3.range(columns)){
                rowElement.append('rect')
                    .attr("x", function(d) { return (+col) * gridSize; })
                    .attr("y", function(d) { return (+i) * gridSize; })
                    .attr("rx", 4)
                    .attr("ry", 4)
                    .attr("class", "cell")
                    .attr("width", gridSize)
                    .attr("height", gridSize)
                    .style("fill", colors[0])
                    .transition().duration(3000)
                      .style('fill',function(d) { 
                        return colorScale( Math.round10(+d[i]['c'+col],-1) )} );

               rowElement.append('text')
                    .attr("x", function(d) { return ((+col) * gridSize) + 10; })
                    .attr("y", function(d) { return ((+i) * gridSize) + (0.5*gridSize); })
                    .attr("class", "cellText")
                    .text(Math.round10(+d['c'+col],-1))
                    .style('text-anchor','right')
                    .style("fill", 'white');

            }
         })

        */ 

         // create legend
         var legendData = d3.range(colorDomain[0],colorDomain[1], (colorDomain[1]-colorDomain[0]) / columns );

         var legend = svg.append('g')
            .classed('legend',true)
            .attr("transform", function(d,i) { return "translate(0," + ( height - margin.bottom - margin.top + margin.legend) + ")";});

         console.log((colorDomain[1]-colorDomain[0]) / columns)
         legend.selectAll('.legendRect')
            .data(legendData)
            .enter().append('rect')
            .attr({
              x: function(d,i){ return gridSize * i }
            , y: 0
            , height: gridSize
            , width: gridSize
            })
            .classed('cell',true)
            .classed('legendRect',true)
            .style('fill', function(d){
              return colorScale( +d )} );

        legendData.push(colorDomain[1]);
        console.log(legendData)
        console.log(colorDomain[1])

        legend.selectAll('.legendText')
            .data(legendData)
            .enter().append('text')
            .attr({
              x: function(d,i) { return (i * gridSize)-5;}
            , y: gridSize+10
            , class:"legendText"
            })
            .text(function(d){return Math.round10(+d,-1)});

        // Add title
        svg.append('g')
            .classed('title_container',true)
            .append('text')
            .classed('title',true)
            .attr({
                x: 0
              , y: (margin.top/2)-(gridSize*2)
            })
            .text(title)

    })
  }

  chart.margin = function(m) {
    if (!arguments.length) { return margin; }
    margin = m;
    return chart;
  };

  chart.width = function(w) {
    if (!arguments.length) { return width; }
    width = w;
    return chart;
  };

  chart.height = function(h) {
    if (!arguments.length) { return height; }
    height = h;
    return chart;
  };

  chart.gridSize = function(m) {
    if (!arguments.length) { return gridSize; }
    gridSize = m;
    return chart;
  };

  chart.colors = function(c) {
    if (!arguments.length) { return colors; }
    colors = c;
    colorScale = d3.scale.linear().domain(colorDomain).range(colors);
    return chart;
  };

  chart.colorDomain = function(d) {
    if (!arguments.length) { return colorDomain; }
    colorDomain = d;
    colorScale = d3.scale.linear().domain(colorDomain).range(colors);
    return chart;
  };

  chart.title = function(t) {
    if (!arguments.length) { return title; }
    title = t;
    return chart;
  };

  return chart
}
"""
    # create app.js
    appContent = """
(function() {
  // call the heatmap constructor
  var myHeatmap = heatmap();

  // the number of elements in this array determines the number of heatmaps created
  var dataPathArray = ['PD1_and_PD2_edm_agg.csv'
    ,'PD1_and_PD2_country_agg.csv'
                      ];

  // create a heatmap for each dataset
  dataPathArray.forEach(function(dataFileName){
    console.log(dataFileName)

    var data = d3.csv('./data/'+dataFileName,function(error, data){
      if (error) return console.warn(error);
      var colCount = Object.keys(data[0]).length -1
        , rowCount = data.length;

      myHeatmap.height( (myHeatmap.gridSize()*rowCount) +  myHeatmap.margin().top + myHeatmap.margin().bottom)
      myHeatmap.width( (myHeatmap.gridSize()*colCount) + myHeatmap.margin().right + myHeatmap.margin().left)
      //myHeatmap.colors(['#e5f5f9','#2ca25f'])
      myHeatmap.title( 'Heatmap: '+dataFileName )
      var container = d3.select("body").selectAll('#'+dataFileName);

      container.data([data])
          .enter()
          .append("div")
          .attr('id',dataFileName)
          .call(myHeatmap);

    })

  })
}())
"""
    # dataset1
    dataset1Content = """row_name,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9
BYOB,-0.3768676174,0.33986063,-0.4560061111,-0.6338553185,-0.9787854505,0.3791164167,0.1319010482,0.7686667752,-0.6463068054,-0.23308059
Bro-country,-1.825092936,-1.473007802,-0.2040391542,0,-1.040716408,1.711669874,0,-0.9131733948,0,0
Cumulus.com,0,0,0,0,0,1.241339927,0,0,0,0.8009931775
at home,-0.1464325905,0.2245497835,-1.107832067,-0.2976752345,-0.5282885389,-0.06992443433,0.01386911158,0.7727479752,0.2772754021,0.2589787827
bar,0.4421837213,0.258734471,-0.9783220814,0.4170901011,-0.5055928244,0.2029946332,-0.06199025491,-0.1245843927,-0.3260431118,0.1204553024
barbecue,0.2890968285,-1.078070816,-1.979298073,-1.31496452,-2.838549649,0.9820850107,-0.8115724183,0.8666471836,0.3843007542,0.1113002318
bbq,-0.123048409,-0.5699831353,-0.8725540549,-0.3283972533,-0.9008569086,0.7182072732,-0.280152506,0.4397556384,0.3098339599,0.09402334199
beer,-0.9875339065,-1.655381511,0.8277349305,0.4206116606,-1.598783067,0.4301481755,-1.839084116,0.07660237115,0.3506055054,-0.850542362
burger,0.3812925628,0.5287803089,-0.5543817322,-0.7462498608,-0.9694830579,0.203462205,0.02683254598,-0.4967341278,-0.556961705,0.2673229211
celebrate,-0.2362933794,0.3453627658,-1.034325733,-0.5333717371,-0.2397055391,-0.09641073532,0.757983102,-0.07942263911,-0.1216767277,-0.1174811951
concert,-0.04835754156,0.06282188369,1.162665948,-0.1914480518,-1.201926856,-0.4186580536,-0.9459695925,-0.6949998933,-0.03199376816,-1.550798499
day,-0.3221480211,-0.1958335746,-0.8810225076,-0.3569108836,-0.1548482088,0.2353925321,0.4629842779,0.1462122639,-0.1333182039,0.07076332987
friends,-0.1759847367,0.6627547539,-1.02982867,-0.920612154,-1.063447011,0.1189843882,0.3910528371,0.2366087586,0.7623933322,-0.05865576823
game,-0.6232566555,0.5913938108,-0.8402156575,-0.1195898879,0.09306640924,-0.3721849442,0.1741741184,-0.04042140945,-0.09125722392,0.3158764459
gamer,-0.8043116323,1.249920812,-2.187506389,-1.258009628,-0.8672329646,-0.3743285348,0.4283758726,-0.9115402081,0.3476348607,0.2485976375
gaming,-0.9315651255,0.7735395805,-0.34520797,0.05113806034,-1.85193669,-0.09738034405,-0.155201146,0.1514489101,-0.6031673127,0.1773027979
gourmet,-0.3824077978,1.054866604,-1.665519096,-0.5216124632,0,0.8135275205,-0.4490032771,-0.0170319627,-1.344994166,-0.1208377347
holiday,-0.2016668194,0.3826710628,-1.642803269,-0.7517650669,0.8219640801,0.04320661529,0.3001169517,0.4071885706,0.2103724293,0.1005705471
iHeartRadio,0.1122047146,0.5663830733,-1.289259257,-0.6308604405,-0.2618729447,0.1782733623,0.787012114,-0.3067849659,-0.3228400321,-0.4239551714
mash-up,-1.007135954,2.034814838,-2.63687186,-2.195681859,0.5780184189,-0.9685133583,-0.05572317684,-1.412198974,-0.09095147611,-0.5285013855
mashup,-1.160470263,2.062001337,-2.849046669,-2.712185131,-0.1339536827,-0.4124486303,0.2204797794,-1.715128146,-0.2069401456,-1.160047549
night,-0.4683724824,-0.5489702489,0.3104120802,0.4379426068,-0.4209318796,-0.2357490629,-0.5570410041,0.1922901724,-0.2613735974,0.130035326
party,-0.8086374996,0.008444177846,0.4259126494,0.2048944895,-1.290001378,-0.4456812379,-0.4388438981,-0.4709842304,-0.6964178676,0.2640370249
restaurant,-0.6332077673,0.1101887272,-1.750651943,1.359672842,-1.182481867,0.528715421,-0.3986981538,-1.050898444,-0.4531218573,-0.3852433563
weekend,-0.02306523693,-0.07365731214,-0.6561756511,-0.04119768727,-0.8393674413,0.1955570146,0.1721770543,-0.1244458429,-0.1319228547,0.2358293702
youtube,1.625148575,0.8950027338,-1.333039694,-0.8785955866,1.834246255,-0.4023159424,-2.023229906,-1.608747608,1.075019928,-0.09858517528
"""
    # dataset2
    dataset2Content = """row_name,c0,c1,c2,c3,c4,c5,c6,c7,c8,c9
at home,-0.7185878722,-0.643770399,0.3366659393,1.197899236,-0.5818119991,-0.7942992557,-0.01813790994,0.218031348,-0.002930854352,0.8188920181
bar,0.1788881397,-0.1849581921,-0.4619834515,-0.761548576,-0.6908556629,-0.1857178231,-0.3542772755,1.355897264,-0.2067118816,0.2606947757
beer,-0.3164700755,-0.4061270711,-0.2198862188,-0.9298696219,-0.4187837196,-1.010176811,-0.4601551761,0.4578200381,0.3920281798,0.8042656927
celebrate,-0.8803236313,-0.3712566845,0.1848607484,0.4699390736,0.1804972624,0.7524130959,-0.003169560428,-0.5643607423,0.2564122802,0.2765760674
day,-0.6290509394,-0.08103898982,0.3640543599,-0.0548602462,-0.2175863631,-0.003910020731,0.4436523248,0.02990871618,-0.2726503861,-0.002348744998
download,0.2328291317,0.6058976874,-1.695302033,-0.3475269866,0.2557901399,-0.398693041,-0.8795591975,-1.592947085,-0.2444810364,-0.804578753
fashion,-1.192409097,0.2662339026,-0.3773046835,-1.893925909,0.3654772912,-1.354697735,-1.168826184,-0.4234274722,0.6350802719,-1.335524815
festival,-1.565647905,-0.6038868167,-0.3265556859,-0.4250570465,0.1152508975,-1.006821634,-1.215445804,-1.619374082,1.235976807,-2.081489287
food,-0.7135429479,-0.1108898698,-0.3580985667,-1.268507597,-0.07998380812,-1.231234652,-0.360029758,0.9990205618,0.2445606896,0.2564934034
friends,-0.6007202967,-0.00585720876,0.3934170537,-0.09067806364,-0.07275377306,-0.3701082209,0.2662797298,0.0231831744,-0.1006632976,-0.2725139528
game,0.4242767099,-0.2351994365,-0.9447457704,-0.03752961057,-1.109516692,-0.3241516414,-0.5855192756,0.7783699923,-0.7275190357,1.200914275
gamer,0.1272869777,-1.40063675,-1.805892182,-1.907469633,-1.619527282,-2.349070712,-1.006862688,2.404290858,-0.4955347332,-0.08085346537
gaming,1.625415502,-0.454047808,-0.3499583354,-0.6161577661,-1.215191759,-0.9523983296,-0.475187743,0.9630585841,-0.6714613856,-0.04020151698
gourmet,-0.1465160067,-0.4758258487,-0.4535093965,0,-1.195363799,-1.679784771,-0.7053015274,1.11415293,-0.06384676064,1.156016433
holiday,-0.1633010465,-0.1549161253,-0.3071427955,-0.3970583068,0.08136378865,-0.2945765404,-0.1194089803,0.829382068,0.04165149689,0.2773613258
night,-0.5974356114,0.08258760174,-0.2430731411,0.562416092,0.3120323847,0.3079523049,0.2447936074,-0.5379328676,-0.4615210359,0.3589869681
party,-0.443492338,0.4451128472,-0.004513725428,-0.1209469645,-0.4195663476,-0.05052716657,-0.1553890951,-0.3272176294,-0.3851706672,-0.8505027967
restaurant,-0.5629764862,-0.7716145087,0.4206043852,0.9113135045,0.6792190538,-0.5759073332,-0.3347960712,1.020183157,0.07063012027,0.1045703634
style,0.2937887361,0.4569077862,-0.7011499499,-0.8017700049,0.05439905582,-0.5560890229,-0.3125961312,-1.179424517,-0.5482989586,0.110944918
vinyl,0.06726713176,-0.01222271061,-1.785604454,-0.7176952772,-0.9490044904,-1.472646176,0.1436909545,-0.5902171964,-0.06191018413,1.026682792
weekend,-1.464791434,-0.2675982728,1.26609168,0.3653412549,0.09083378477,0.07083295455,-0.02768437247,-0.8218716607,-0.4974863469,-0.7564591007
work,0.004063240767,0.1984563219,-0.3448818607,-0.301147085,-0.2592034518,-0.3350333363,-0.1894307197,0.5875479602,-0.1732331788,-0.158284724
working,0.09259741006,0.1213732811,-0.1424982405,-0.1074821562,-0.3383656864,0.1068911542,-0.07715354393,0.625971279,-0.3321166235,-0.1386706486
youtube,1.759430983,-0.7388139094,-1.119392002,0.01214931249,0.4638197593,0.8487465544,-1.245332597,0.1292965878,-0.8810370856,0.4523274819
"""
    # css
    cssContent = """
.cell {
  stroke: #E6E6E6;
  stroke-width:2px;
}

.cellText {
  fill: #fff;
  text-anchor:start;
  font-size:15px;
}

.legendText {
  fill: #000;
  text-anchor:start;
  font-size:15px;
}

.title{
  fill: #000;
  text-anchor:start;
  font-size:30px;

}
"""
    # write to file
    with open(pwd+'/index.html','wb') as html:
        html.write(htmlContent)
    with open(pwd+'/js/heatmap.js','wb') as js:
        js.write(heatmapContent)
    with open(pwd+'/js/app.js','wb') as js:
        js.write(appContent)
    with open(pwd+'/css/style.css','wb') as css:
        css.write(cssContent)
    with open(pwd+'/data/PD1_and_PD2_country_agg.csv','wb') as csv:
        csv.write(dataset1Content)
    with open(pwd+'/data/PD1_and_PD2_edm_agg.csv','wb') as csv:
        csv.write(dataset2Content)
    sys.stderr.write('Full js dir structure complete.\n{}\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
