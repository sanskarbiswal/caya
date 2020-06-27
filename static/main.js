var feedLen = 12;
var recUser = 3;

/**
 * @brief Function to Open Modal
 * @param modal_id
 */
function open_modal(modalID){
    document.getElementById(modalID).style.display = 'block';
}

/**
 * @brief Function to Close Modal
 * @param modal_id
 */
function close_modal(modalID){
    document.getElementById(modalID).style.display = 'none';
}

/* ############### Initial Page Setup ################# */

/**
 * @brief Setup and Load Feed
 */
function init_feed(){
    var i=0;
    table = document.getElementById('feed-table');
    for(i=0;i<feedLen;i++){
        tr = document.createElement('tr');
        tr.setAttribute('id', 'feed-'+String(i));
        if(i%2==0){
            tr.setAttribute('class', 'w3-grey w3-padding-16');
        }else{
            tr.setAttribute('class', 'w3-white w3-padding-16');
        }

        ico_str = "<i class='fa fa-bell w3-text-blue w3-large'></i>";
        td1 = document.createElement('td');
        td1.innerHTML = ico_str;
        
        td2 = document.createElement('td');
        td2.setAttribute('id', `feed-${i}-data`);
        td2.innerHTML = "NONE";

        td3 = document.createElement('td');
        td3.setAttribute('id', 'feed-'+i+'-time');
        td3.innerHTML = "NONE";

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);

        table.appendChild(tr);
    }
}

/**
 * @brief Update Feed
 * @param new_data
 */
function update_feed(new_entry){
    // Shift all content down
}

/* ############### Document Setup ################# */

/**
 * @brief Function to Call on Load
 */
function initLoad(){
    init_feed();
}

function refresh_components(data){
    var i;
    par = document.getElementById("component-search");
    for(i=0;i<data.length;i++){
        op = document.createElement('option');
        op.innerHTML = data[i];
        par.appendChild(op);
    }
}
/* ############### jQuery System ################# */
function download()
{
    var path = "../data/components.csv"; //relative-path
    $('location').attr('href',path);
 }

 $(function () {
     $.ajax(
   { url : '{{ url_for("autocomplete") }}' }
  ).done(function(data){
      $('#autocomplete').autocomplete({
          source: data.json_list,
          minLength: 2
      });
  });
 });
