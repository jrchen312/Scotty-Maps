// Google map handler: 
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
  key: "AIzaSyBoIFr6oHJ7DHYKTzjMZzJmFBCc-Ill2U0",
  v: "weekly",
  mapId: "c8d02a78f31968ed",
  // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
});

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
  const hoaPos = { lat: 40.4409058, lng: -79.94249 };

  contentString = `<a href="/building/hallofarts">Hall of Arts</a>
  `;

  const infowindow = new google.maps.InfoWindow({
    content: contentString,
    ariaLabel: "Hall of Arts",
  });

  const marker = new AdvancedMarkerElement({
    map: map,
    position: hoaPos,
    title: "Hall of Arts",
  });

  marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
    });
  });
}


initMap();
