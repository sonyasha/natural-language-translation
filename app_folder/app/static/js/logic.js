$( document ).ready(function() {
    console.log( "Hey! Welcome to our website, hope you will enjoy it!" );
    $('.spa').addClass('active');
    $('.fra').addClass('passive');
    $('#submitForm').text('To Spanish');
    $('#invizeng').attr('value', ($('#inputlang').val()));
    $('#invizother').attr('value', ($('#outputlang').val()));
    $('#invizlanng').attr('value', ($('#invizlang').val()));
    $('#invizlang').attr('value', 'spa');
    // $('#invizhaik').attr('value', ($('.gen-text').val()));
    // $('.gen-text').attr('value', ($('#label').html()));
    
});

// submit Form
$("#submitForm").click(function(event) {
    event.preventDefault();
    $("#translate-form").submit();		
});

// generate Form
$("#submitGen").click(function(event) {
    event.preventDefault();
    $("#generate-form").submit();		
});

// responsive behaviour
$(window).resize(createChart);

createChart();


function createChart() {
    if ($('#inputlang').val() != '') {

        // (!$('#graph').is(':empty')) ? $('#graph').empty() : $('#graph').empty()
        $('#graph').empty()
        $('#arrow').empty()

        var selection = d3.select('#arrow')
            .append('select')
            .attr('id', 'plot-select')
            .attr('onchange', 'changeData(this.value)')

        selection.append('option')
            .attr('value', 'engl')
            .text('input')
        selection.append('option')
            .attr('value', 'other')
            .text('output')

        // default chart
        renderChart(getLetters($('#inputlang').val())); 
    }      
}

// change chart based on text source

function changeData(value) {
    if ($('#inputlang').val() != '') {

        switch (value) {
        case "engl":
        data = getLetters($('#inputlang').val());
        break;
        case "other":
        data = getLetters($('#outputlang').val());
        break;
        }
        renderChart(data);
    }   
}

function renderChart(data) {
    
    $('svg').remove()

    var svgWidth = window.innerWidth/2.5;
    var svgHeight = window.innerHeight/3;

    
    var color = d3.scaleOrdinal(d3.schemeYlGnBu[9]);

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
        .attr("transform", 'translate(' + svgWidth / 2 + "," + svgHeight / 2 + ')');

    svg.append("text")
        .attr("text-anchor", "middle")
        .attr('y', 8)
        .attr("class", "donut-text")
        .style("fill", "rgb(186, 197, 214)")
        .text(data.length);

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
        .style("fill", "rgb(22, 53, 102)");


    var tooltip = d3.select("#graph").append("div").attr("class", "toolTip");

    d3.selectAll("path").on("mouseover", function(d) {
	    tooltip.style("left", d3.event.pageX+15+"px");
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


// resize font size if more than 20 letters
$('#inputlang').each(function(){
    var el = $(this);
      var textLength = el.val().length;
       if (textLength > 20) {
           el.css('font-size', '0.99em');
       }
});

$('#outputlang').each(function(){
    var el = $(this);
      var textLength = el.val().length;
       if (textLength > 20) {
           el.css('font-size', '0.99em');
       }
});


// add classes to translate form


$('.spa').click(function(){
    $('#invizlang').attr('value', 'spa');
    $('#invizlanng').attr('value', 'spa');
    $('#submitForm').text('To Spanish')
    $('.spa').addClass('active');
    $('.fra').removeClass('active');
    $('.fra').addClass('passive');
    $('.spa').removeClass('passive');
})

$('.fra').click(function(){
    $('#invizlang').attr('value', 'fra');
    $('#invizlanng').attr('value', 'fra');
    $('#submitForm').text('To French')
    $('.fra').addClass('active');
    $('.spa').removeClass('active');
    $('.spa').addClass('passive');
    $('.fra').removeClass('passive');
})

