/* Projection d'une liste de classe, dans sa propre fenetre : le QR code en
   grand, et le nombre d'inscrits relu toutes les 3 secondes. Elle vit
   seule : l'enseignant peut fermer ou quitter la page de la liste, la
   projection continue. */
(function () {
  "use strict";

  var POLL_MS = 3000;

  var qrBox = document.getElementById("qr");
  var count = document.getElementById("count");
  var hint = document.getElementById("hint");
  var closed = document.getElementById("closed");
  var fullscreen = document.getElementById("fullscreen");

  // Meme dessin que sur la page de la liste (cf. admin_roster.js) :
  // niveau de correction M, marge de quatre modules.
  if (typeof qrcode === "function") {
    var qr = qrcode(0, "M");
    qr.addData(qrBox.getAttribute("data-url"));
    qr.make();
    qrBox.innerHTML = qr.createSvgTag({ cellSize: 8, margin: 32, scalable: true });
  }

  function refresh() {
    fetch(window.ROSTER_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then(function (data) {
        count.textContent = data.count + (data.count > 1 ? " inscrits" : " inscrit");
        // Une liste close garde son QR code a l'ecran, mais le dit : un
        // eleve qui le flashe tomberait sur un refus.
        var open = data.status === "open";
        hint.hidden = !open;
        closed.hidden = open;
        qrBox.classList.toggle("dimmed", !open);
      })
      .catch(function () { /* le prochain tour reessaiera */ });
  }

  refresh();
  setInterval(refresh, POLL_MS);

  // Le plein ecran exige un geste de l'utilisateur : un bouton, cache des
  // qu'on y est.
  if (!document.documentElement.requestFullscreen) {
    fullscreen.hidden = true;
  } else {
    fullscreen.addEventListener("click", function () {
      document.documentElement.requestFullscreen().catch(function () {});
    });
    document.addEventListener("fullscreenchange", function () {
      fullscreen.hidden = !!document.fullscreenElement;
    });
  }
})();
