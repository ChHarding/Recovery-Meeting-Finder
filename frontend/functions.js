let markers = [];



function correct_json(jsonString){
  // preserve newlines, etc - use valid JSON
  tmp = jsonString.replace("\n","<br>")
                 .replace(/\\n/g, "\\n")
                 .replace(/\\'/g, "\\'")
                 .replace(/\\"/g, '\\"')
                 .replace(/\\&/g, "\\&")
                 .replace(/\\r/g, "\\r")
                 .replace(/\\t/g, "\\t")
                 .replace(/\\b/g, "\\b")
                 .replace(/\\f/g, "\\f");

  // remove non-printable and other non-valid JSON chars
  tmp = tmp.replace(/[\u0000-\u0019]+/g,"");

  return tmp;
}



function refreshMap(){

filter_y12sr     = document.getElementById('chk_y12sr').checked;
filter_smart     = document.getElementById('chk_smart').checked;
filter_day       = document.getElementById('meeting_day').value;
filter_from_time = document.getElementById('from_time').value;
filter_to_time   = document.getElementById('to_time').value;

y12sr_meetings_to_show = [];
smart_meetings_to_show = [];


if (filter_y12sr){
  for (i=0;i<y12sr.length;i++){
    if (y12sr[i].days.includes(filter_day)){
      for(j=0;j<y12sr[i].times.length;j++){
        if(isInRange(y12sr[i].times[j], filter_from_time, filter_to_time)){
          y12sr_meetings_to_show.push(y12sr[i]);
          break;
        }
      }
    }
  }
}


if (filter_smart){
  for (i=0;i<smart.length;i++){
    if (smart[i].days.includes(filter_day)){
      for(j=0;j<smart[i].times.length;j++){
        if(isInRange(smart[i].times[j], filter_from_time, filter_to_time)){
          smart_meetings_to_show.push(smart[i]);
          break;
        }
      }
    }
  }
}



var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var violetIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


console.log("markers are: " + markers.length);


for (i=0; i<markers.length; i++){
  markers[i].remove();
}

markers = [];

for (var i = 0; i < y12sr_meetings_to_show.length; i++) {
  if (y12sr_meetings_to_show[i].latitude !=="-" && y12sr_meetings_to_show[i].longitude !=="-"){

    tootlipContent  = "<h3>Y12SR</h3> meeting at: <b>" + y12sr_meetings_to_show[i].times.toString()+"</b> on " + y12sr_meetings_to_show[i].days.toString();
    tootlipContent += "<br><br><i><a target=_blank href='https://maps.google.com/?q=" + y12sr_meetings_to_show[i].address+"'>" + y12sr_meetings_to_show[i].address + "</a>";
    tootlipContent += "<br><br><center><button onclick=\"markerClicked('Y12SR', '" + y12sr_meetings_to_show[i].days.toString() + "','" + y12sr_meetings_to_show[i].times.toString() + "','" + y12sr_meetings_to_show[i].address + "','" + y12sr_meetings_to_show[i].details + "');\">More details ...</button></center><br>";

    marker = new L.marker([y12sr_meetings_to_show[i].latitude, y12sr_meetings_to_show[i].longitude], {icon: violetIcon})
      .bindPopup(tootlipContent)
      .addTo(map);
    markers.push(marker);
  }

}


for (var i = 0; i < smart_meetings_to_show.length; i++) {
  if (smart_meetings_to_show[i].latitude !=="-" && smart_meetings_to_show[i].longitude !=="-"){

    tootlipContent  = "<h3>SMART</h3> meeting at: <b>" + smart_meetings_to_show[i].times.toString()+"</b> on " + smart_meetings_to_show[i].days.toString();
    tootlipContent += "<br><br><i><a target=_blank href='https://maps.google.com/?q=" + smart_meetings_to_show[i].address+"'>" + smart_meetings_to_show[i].address + "</a>";
    tootlipContent += "<br><br><center><button onclick=\"markerClicked('SMART','" + smart_meetings_to_show[i].days.toString() + "','" + smart_meetings_to_show[i].times.toString() + "','" + smart_meetings_to_show[i].address + "','" + smart_meetings_to_show[i].details + "');\">More details ...</button></center><br>";


    marker = new L.marker([smart_meetings_to_show[i].latitude, smart_meetings_to_show[i].longitude], {icon: greenIcon})
      .bindPopup(tootlipContent)
      .addTo(map);
    markers.push(marker);
  }
}

}


function isInRange(timeStr, t1, t2){
if(timeStr.toLowerCase().includes('am')){
  ampm = "am"
} else if(timeStr.toLowerCase().includes('pm')){
  ampm = "pm"
} else{
  return 0;
}

timeStr = timeStr.split(" ")[0];

t = Number(timeStr.split(":")[0]) + (Number(timeStr.split(":")[1]) / 60);

if (ampm == "pm"){
  t = t + 12;
}

if(t>=t1 && t<=t2){
  return 1;
}else{
  return 0;
}

}


function markerClicked(type, days, times, address, details){
//alert(days + times+ address+ details);
leftpanel = document.getElementById('leftpanel');
leftpanel.innerHTML  ='<div style="position:absolute;right:15px;background-color:#ddd;border-radius:50%;width:25px;height:25px;text-align:center;line-height:25px;font-size:25px;color:gray;cursor:pointer" onclick="document.getElementById(`leftpanel`).style.left=`-530px`;">&times;</div>';
leftpanel.innerHTML += "<h2>" + type + " Meeting</h2>";
leftpanel.innerHTML += "<b>" + days + "</b> at <i>" + times + "</i><hr>";
leftpanel.innerHTML += "<br><i><a target=_blank href='https://maps.google.com/?q=" + address+"'>" + address + "</a>";
leftpanel.innerHTML += "<br><br><h3>More details</h3><hr>";
leftpanel.innerHTML += details;

leftpanel.style.left="18px";
}
