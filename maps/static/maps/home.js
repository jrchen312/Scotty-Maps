// // Google map handler: 
// (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
//   key: ":(",
//   v: "weekly",
//   mapId: "c8d02a78f31968ed",
//   // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
// });

// use proxy on webserver to load google maps...
function loadMapsScript() {
  fetch('/get_maps_script')  // Proxy url endpoint
      .then(response => response.text())
      .then(scriptContent => {
          const script = document.createElement('script');
          script.innerHTML = scriptContent; // Set the script content dynamically
          document.head.appendChild(script);
      })
      .then(initMap())
      .catch(error => console.error('Error loading Maps script:', error));
}

// Call to load the Maps script:
loadMapsScript(); 


// Initialize and add the map
let map;

async function initMap() {
  // center the map over cmu main campus. 
  const position = { lat: 40.4424812, lng: -79.9436793 };

  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
    zoom: 17,
    center: position,
    mapId: "c8d02a78f31968ed",
  });

  // Markers
  $.get("/get_map_pins", function(data, status) {
    // console.log("Data: " + JSON.parse(data) + "\nStatus: " + status);
    let json_data = JSON.parse(data);

    for (let i = 0; i < json_data.length; i=i+1) {
      let loc = json_data[i];

      let floorString = ``;

      for (let k = 0; k < loc.floors.length; k=k+1) {
        floorString += `
        <p class="card_text">
          <a href="${loc.floors[k].img_path}">${loc.floors[k].name}</a>
        </p>
        `;
      }

      const contentString = `
        <div class="card-body">
          <h5 class="card-title">${loc.name}</h5>

          ${floorString}
        </div>
      `;

      const pos = { lat : loc.lat, lng : loc.lng };

      const infowindow = new google.maps.InfoWindow({
        content: contentString,
        ariaLabel: loc.name,
      });

      const marker = new AdvancedMarkerElement({
        map: map,
        position: pos,
        title: loc.name
      });

      marker.addListener("click", () => {
        infowindow.open({
          anchor: marker,
          map,
        });
      });

    }

  });

}


