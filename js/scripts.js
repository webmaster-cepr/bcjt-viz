var month = [];
month[0] = "January";
month[1] = "February";
month[2] = "March";
month[3] = "April";
month[4] = "May";
month[5] = "June";
month[6] = "July";
month[7] = "August";
month[8] = "September";
month[9] = "October";
month[10] = "November";
month[11] = "December";

function buildMap(file='data/jobs-by-state-three-month-median-2018-1.json',jobcat="All",jobmon=1512086400000) {
  
  $.getJSON(file, function (data) {
  
    var filteredData=$(data).filter(function (i,n){return n.category===jobcat && n.date===jobmon});
    
    console.log([file,jobcat,jobmon]);
        
    let d = new Date(jobmon);
    let jobsMonth = month[d.getUTCMonth()];
    let jobsYear = d.getUTCFullYear();

    let viztype = $('input[name=month-select]:checked').next().text();

    if (jobcat=='All') { jobcat = 'All Blue Collar'; }
    
    // Instanciate the map
    Highcharts.mapChart('container', {

        title: {
            text: jobcat + ' Jobs, ' + jobsMonth + " " + jobsYear,
            style: { "fontSize":"28px" }
        },
        
        subtitle: {
            text: viztype
        },
        
        legend: {
            layout: 'horizontal',
            borderWidth: 0,
            backgroundColor: 'rgba(255,255,255,0.85)',
            verticalAlign: 'bottom'
        },
        
        credits: {
            enabled: true,
            text: "Source: Federal Reserve Bank of St. Louis, https://bluecollarjobs.us/,",
            style: {
                fontSize: 12
            },
            position: {
                align: 'left',
                x: 50
            }
        },        

        mapNavigation: {
            enabled: true
        },

        colorAxis: {
            min: -1,
            type: 'linear',
            minColor: '#FFFFFF',
            maxColor: '#1F497D',
            stops: [
                [0, '#FFFFFF'],
                [0.5, '#C5D9F1'],
                [1, '#1F497D']
            ]
        },

        series: [{
            data: filteredData,
            mapData: Highcharts.maps['countries/us/us-all'],
            joinBy: ['postal-code', 'code'],
            dataLabels: {
                enabled: true,
                color: '#FFFFFF',
                format: '{point.code}'
            },
            name: ' ',
            nullColor: "#000",
            tooltip: {
                pointFormat: '{point.code}: {point.value}%'
            }
        }]
    });
  });
}

function buildRBPlot(state="IL") {
   
  let conValues = [];
  let manValues = [];
  let mineValues = [];

   $.getJSON('data/jobs-by-state--2018-1.json', function (data) {
     
     var filteredData=$(data).filter(function (i,n){return n.code == state});

     $.each(filteredData, function(key, val) {
       
        if(val.category == "Construction" ) {
            conValues.push(parseFloat(val.value));
        } else if (val.category == "Manufacturing") {
            manValues.push(parseFloat(val.value));
        } else if (val.category == "Mining and Logging") {
           mineValues.push(parseFloat(val.value));
        }
      
      });

    Highcharts.chart('rb-container', {
      
          title: {
            text: 'Blue Collar Jobs, ' + state,
            style: { "fontSize":"28px" }
          },
      
          xAxis: {
            type: 'datetime'
          },
          
          yAxis: {
            min: 0,
	    floor: 0,
            title: {
              text: 'Persons in thousands'
            },
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            alternateGridColor: null,
            plotBands: [{ // negative values
              from: -10,
              to: 0,
              color: '#EEEEEE'
            }]
            
          },
          
          credits: {
            enabled: true,
            text: "Source: Federal Reserve Bank of St. Louis, https://bluecollarjobs.us/",
            style: {
                fontSize: 12
            },
            position: {
                align: 'left',
                x: 50
            }
          },
          
          plotOptions: {
             series: {
                 pointStart: Date.UTC(2016, 11),
                 pointInterval: 24 * 3600 * 1000 * 31 // one month
               }
          },
          
          series: [
            {
              name: 'Construction',
              data: conValues,
              color: '#1F497D',
              visible: false,
              tooltip: {
                headerFormat: '',
                pointFormat: '{point.y}'
            },
              zoneAxis: 'x',
              zones: [{
                value: new Date(1480550400000),
                dashStyle: 'dot'
              }, {
                value: new Date(1483228800000),
                dashStyle: 'dot'
              }]
            },
            {
              name: 'Manufacturing',
              data: manValues,
              color: '#538DD5',
              tooltip: {
                headerFormat: '',
                pointFormat: '{point.y}'
            },
              zoneAxis: 'x',
              zones: [{
                value: new Date(1480550400000),
                dashStyle: 'dot'
              }, {
                value: new Date(1483228800000),
                dashStyle: 'dot'
              }]
            },
            {
              name: 'Mining and Logging',
              data: mineValues,
              color: '#948A54',
              visible: false,
              tooltip: {
                headerFormat: '',
                pointFormat: '{point.y}'
            },
	      zoneAxis: 'x',
              zones: [{
                value: new Date(1480550400000),
                dashStyle: 'dot'
              }, {
                value: new Date(1483228800000),
                dashStyle: 'dot'
              }]
            }]
      });
    });
}

$(document).ready(function(){

buildMap();
buildRBPlot();

$(document).on('click', '#categories li', function() {
       $("#categories li").removeClass("active");
       $(this).addClass("active");
       buildMap(file=$('input[name=month-select]:checked').val(),jobcat=$("#categories .active").text(), jobmon=Number($('#month').val()));
   });

$(document).on('click', '#month', function() {
      buildMap(file=$('input[name=month-select]:checked').val(), jobcat=$("#categories .active").text(), jobmon=Number($(this).val()));
   });
   
$(document).on('click', 'input[name=month-select]', function() { 
      buildMap(file=$(this).val(), jobcat=$("#categories .active").text(), jobmon=Number($('#month').val()));
});

$(document).on('click', '#states li', function() {
       $("#states li").removeClass("active");
       $(this).addClass("active");
       buildRBPlot(state=$(this).data('id'));
   });

});


