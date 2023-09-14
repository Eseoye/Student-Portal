

// Populating States and LGA
let states = $('#state');
let lgas = $('#lga');
$("form#portalForm").find(':input', ':select').after(`<div class="form-text text-danger"></div>`);

states.empty();
lgas.empty();

states.append("<option selected='true' disabled>Choose State</option>");
states.prop('selectedIndex', 0);

lgas.append("<option selected='true' disabled>Choose Local Government</option>");
lgas.prop('selectedIndex', 0);

const url = 'static/json/states-localgovts.json'

// Populate states with json
$.getJSON(url, function(data){
    $.each(data, function(key, value){
        states.append($('<option></option>').attr('value', value.state).text(value.state));
    });
});

//Populate lga with json
$('#state').change(function(){
    lgas.empty();
    lgas.append("<option selected='true' disabled> Choose Local Government</option>");
    lgas.prop('selectedIndex', 0);

    let stat = $('#state').val()

    $.getJSON(url, function(data){
        $.each(data, function(key, value){
            if (value.state == stat){
                for(let i=0; i < value.local.length; i++)
                lgas.append($('<option></option>').attr('value', value.local[i]).text(value.local[i]));
            }
        });
    });
});