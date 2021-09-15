var grid = document.querySelector('.grid');
var iso = new Isotope( grid, {
  itemSelector: '.grid-item',
  columnWidth: '.grid-item',
  percentPosition:true,
  stamp: '.stamp',
  sortBy:'position',
  getSortData: {
    'position': '.position parseInt'
  }
});
imagesLoaded( grid ).on( 'progress', function() {
  iso.layout();
});
function double(data) {
  artist_id = data.getElementsByClassName('artist_id')[0].innerText;
  album_position = data.getElementsByClassName('position')[0].innerText;
  album_id = data.getElementsByClassName('album_id')[0].innerText;
  var request = new XMLHttpRequest();
  request.open('GET','http://localhost:8000/?position=' + album_position + '&artist_id=' + artist_id + '&album_id=' + album_id);
  request.responseType = "document";
  request.onload = function () {
    if (this.status = 200) {
      iso.insert(this.responseXML.body.children)
    }
  }
  request.send();
};
function single(data) {
  let text_container = data.getElementsByClassName('text-container--off')[0];
  let image = data.getElementsByTagName('img')[0];
  function off() {
    text_container.classList.remove('text-container--on');
    image.classList.remove('img--off');
  }
  text_container.classList.add('text-container--on');
  image.classList.add('img--off');
  setTimeout(off,2000);
};

var mouse_down;
var mouse_up;
var elapsed;

function press(data,event) {
  const date = new Date();

  function long(data) {
    const url = 'https://duckduckgo.com/?q=';
    let artist = data.getElementsByClassName('artist')[0].innerText;
    let album = data.getElementsByClassName('title')[0].innerText;
    let link = url + artist + " " + album;
    window.open(link,'_blank')
  };

  if (event.type == "mousedown") {
    mouse_down = date.getTime();
  }

  if (event.type == "mouseup") {
    mouse_up = date.getTime();
    elapsed = date.getTime() - mouse_down;
    if (elapsed >= 500) {
      long(data);
    }
  }
};
