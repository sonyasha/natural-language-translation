$( document ).ready(function() {
    console.log( "i'm ready!" );
});

$("#submitForm").click(function(event) {
        event.preventDefault();
        $("#translate-form").submit();		
});

$(window).resize(createChart);

createChart();


function createChart() {
    if ($('#inputlang').val() != '') {

        (!$('#graph').is(':empty')) ? $('#graph').empty() : $('#graph').empty()

        var selection = d3.select('#graph')
            .append('select')
            .attr('id', 'plot-select')
            .attr('onchange', 'changeData(this.value)')

        selection.append('option')
            .attr('value', 'engl')
            .text('input')
        selection.append('option')
            .attr('value', 'other')
            .text('output')

        var inputdata = $('#inputlang').val();
        var outputdata = $('#outputlang').val();

        var plotdata = getLetters(inputdata);

        plotdata.forEach(el => {
            el.value = +el.value;     
        });

        renderChart(plotdata); 
    }      
}

function changeData(value) {
    if ($('#inputlang').val() != '') {

        var inputdata = $('#inputlang').val();
        var outputdata = $('#outputlang').val();
        switch (value) {
        case "engl":
        data = getLetters(inputdata);
        break;
        case "other":
        data = getLetters(outputdata);
        break;
        }
        renderChart(data);
    }
}

function renderChart(data) {
    
    $('svg').remove()
    
    var svgWidth = window.innerWidth/2.5;
    var svgHeight = window.innerHeight/3;

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var radius = Math.min(svgWidth, svgHeight) / 2;

    var pie = d3.pie()
        .sort(null)
        .value(function(d) { return d.value; })(data);
        
    var arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 60);
    
    var labelArc = d3.arc()
        .outerRadius(radius - 40)
        .innerRadius(radius - 40);

    var svg = d3.select("#graph")
        .append("svg")
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .append("g")
        .attr("transform", 'translate(' + svgWidth / 2 + "," + svgHeight / 2 + ')')
        .attr('class', 'chartG');

    var g = svg.selectAll("arc")
        .data(pie)
        .enter()
        .append("g")
        .attr("class", "arc");
    
    g.append("path")
        .style("fill", function(d) {
            return color(d.data.name);
        })
        .transition()
        .delay(function(d,i) {
            return i * 170; })
        .duration(50)
        .attr("d", arc);
        

    g.append("text")
        .attr("transform", function(d) {
            return "translate(" + labelArc.centroid(d) + ")";
        })
        .transition()
	    .delay(900)
        .text(function(d) { return d.data.name;})
        .style("fill", "#fff");


    var tooltip = d3.select("#graph").append("div").attr("class", "toolTip");

    d3.selectAll("path").on("mouseover", function(d) {
	    tooltip.style("left", d3.event.pageX+10+"px");
        tooltip.style("top", d3.event.pageY-25+"px");
        tooltip.style("display", "inline-block");

        tooltip.html('letter: ' + (d.data.name) + '<br>frequency: ' + (d.data.value));
    });
	  
    d3.selectAll("path").on("mouseout", function(d){
        tooltip.style("display", "none");
    });
}

// Returns a dictionary of letters from a string (no punctuation marks please)

function getLetters(inputs) {

    var letter_dict = {};

    inputs.toLowerCase().split(' ').forEach(item => {
        item.split('').forEach(letter => {
            (letter_dict[letter]) ? letter_dict[letter] ++ : letter_dict[letter] = 1
        })  
    })

    var dict = Object.keys(letter_dict).map((item, ind) => {
        return {'name': item, 'value': Object.values(letter_dict)[ind]}
    });

    return dict    
}


