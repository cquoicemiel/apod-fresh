// Le fichier javascript permet de rendre fonctionnelles les flèches de navigation et il change l'url pour que la date adéquate y soit appliquée

function dateAujourdhui() {
  //Fonction renvoyant la date actuelle au format "aaaa-mm-dd" 
  const aujourdHui = new Date();
  const annee = aujourdHui.getFullYear();
  const mois = String(aujourdHui.getMonth() + 1).padStart(2, '0');
  const jour = String(aujourdHui.getDate()).padStart(2, '0');
  const heure = aujourdHui.getHours();
  if(heure <= 6){
    return jourPrecedent(`${annee}-${mois}-${jour}`);
  }
  else{
    return `${annee}-${mois}-${jour}`;
      }
}

function isToday(dateString) {
  //Fonction renvoyant un booléen indiquant si la date en paramètre est la date        d'aujourd'hui
  // Entrées:
  // (string) dateString: date au format "aaaa-mm-dd")
  //
  // Sortie:
  // (bool): False si la date entrée est la date actuelle, sinon False
    const date = new Date(dateString);
    const dateToday = new Date();
    return date.getFullYear() === dateToday.getFullYear() &&
        date.getMonth() === dateToday.getMonth() &&
        date.getDate() === dateToday.getDate();
}


function jourPrecedent(dateString) {
  //Fonction utilisée pour naviguer au jour précédent
  //Entrées:
  //(string) dateString: date au format "aaaa-mm-dd"
  //Sortie:
  //(string): nouvelle date au format "aaaa-mm-dd"
    const date = new Date(dateString);
    date.setDate(date.getDate() - 1);

    // Convertir la date au bon format: year-month-day
    return date.toISOString().slice(0, 10);
}

function jourSuivant(dateString) {
  //Fonction utilisée pour naviguer au jour suivant
  //Entrées:
  //(string) dateString: date au format "aaaa-mm-dd"
  //Sortie:
  //(string): nouvelle date au format "aaaa-mm-dd"
    const date = new Date(dateString);
    date.setDate(date.getDate() + 1);

    return date.toISOString().slice(0, 10);
}

function changeParam(key, value) {
  //Fonction permettant d'ajouter ou de modifier un paramètre donné de l'url par une valeur donnée 
  //Entrées:
  //(string) key: nom du paramètre à modifier
  //(string) value: valeur du paramètre à modifier
  //Sortie:
  //La fonction ne renvoie rien
    const url = new URL(window.location.href);
    url.searchParams.set(key, value);
    window.history.replaceState({}, '', url.toString());
}

//On récupère les deux flèches du index.html
prevArrow = document.getElementById("previous")
nextArrow = document.getElementById("next")


const urlParams = new URLSearchParams(window.location.search);
const date = urlParams.get('date');


// Si l'url ne contient pas de date on lui attribue la date d'aujourdhui
if (urlParams.get("date")){
    const date = urlParams.get('date');
}else{
    changeParam("date", dateAujourdhui())
    window.location.reload()
}


// Rendre la flèche du jour suivant transparente et non cliquable si on est au dernier jour disponible
if (isToday(date)){
    nextArrow.style.opacity = "0.4";
    nextArrow.style.cursor = "default"
    nextArrow.style.pointerEvents = "none"
}


prevArrow.onclick = function() {
    changeParam("date", jourPrecedent(date))
    window.location.reload()
}
nextArrow.onclick = function(e) {
    changeParam("date", jourSuivant(date))
    window.location.reload()
}