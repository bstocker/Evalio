/* Chapitre QCM : ranger les QCM dans les sections de l'enseignant.

   Trois gestes, pour le meme effet :
   - glisser un module par son en-tete et le lacher dans une section, a la
     place voulue ;
   - choisir sa section dans la liste de son corps (clavier, ecran tactile,
     ou le glisser-deposer HTML5 ne marche pas) ;
   - « Renommer », qui demande le nouveau nom.

   Apres un deplacement, l'ordre complet de la section d'arrivee part au
   serveur (cf. `place_modules` dans admin.py). Le deplacement est fait dans
   la page d'abord : en cas de refus, on recharge pour revenir a l'etat
   enregistre plutot que de laisser croire a un rangement qui n'a pas eu
   lieu. */
(function () {
  "use strict";

  var chapter = document.querySelector("details.chapter[data-chapter=qcm]");
  if (!chapter) return;

  var PLACE_URL = "/admin/api/qcm/sections/place";
  var dragged = null;
  var marker = document.createElement("div");
  marker.className = "drop-marker";

  function zones() {
    return Array.prototype.slice.call(chapter.querySelectorAll(".drop-zone"));
  }

  function zoneOf(sectionId) {
    return chapter.querySelector(".drop-zone[data-section='" + sectionId + "']");
  }

  function modulesIn(zone) {
    return Array.prototype.slice.call(zone.children).filter(function (node) {
      return node.matches && node.matches("details.module");
    });
  }

  function save(zone) {
    var section = zone.getAttribute("data-section");
    var body = {
      section: section === "" ? null : parseInt(section, 10),
      modules: modulesIn(zone).map(function (m) {
        return m.getAttribute("data-module");
      })
    };
    return fetch(PLACE_URL, {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
    }).catch(function () {
      window.alert("Le rangement n'a pas pu être enregistré : la page va "
                   + "se recharger.");
      window.location.reload();
    });
  }

  // Le module rejoint sa nouvelle section : la liste de son corps suit,
  // et les comptes des en-tetes aussi.
  function settle(module, zone) {
    var select = module.querySelector("select[data-move]");
    if (select) select.value = zone.getAttribute("data-section");
    var group = zone.closest("details.qcm-group");
    if (group) group.open = true;
    document.dispatchEvent(new CustomEvent("catalogue:moved"));
  }

  // Le module avant lequel lacher, d'apres la hauteur du pointeur.
  function before(zone, y) {
    var list = modulesIn(zone).filter(function (m) { return m !== dragged; });
    for (var i = 0; i < list.length; i += 1) {
      var box = list[i].getBoundingClientRect();
      if (y < box.top + box.height / 2) return list[i];
    }
    var hint = zone.querySelector(".drop-hint");
    return hint || null;
  }

  chapter.addEventListener("dragstart", function (event) {
    var head = event.target.closest && event.target.closest("summary.module-head");
    if (!head) return;
    dragged = head.parentNode;
    dragged.classList.add("dragging");
    event.dataTransfer.effectAllowed = "move";
    // Firefox ne lance pas de glisser sans donnee.
    event.dataTransfer.setData("text/plain", dragged.getAttribute("data-module"));
  });

  chapter.addEventListener("dragend", function () {
    if (dragged) dragged.classList.remove("dragging");
    dragged = null;
    if (marker.parentNode) marker.parentNode.removeChild(marker);
    zones().forEach(function (z) { z.classList.remove("drag-over"); });
  });

  zones().forEach(function (zone) {
    zone.addEventListener("dragover", function (event) {
      if (!dragged) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      zones().forEach(function (z) { z.classList.toggle("drag-over", z === zone); });
      zone.insertBefore(marker, before(zone, event.clientY));
    });

    zone.addEventListener("dragleave", function (event) {
      if (!zone.contains(event.relatedTarget)) {
        zone.classList.remove("drag-over");
        if (marker.parentNode === zone) zone.removeChild(marker);
      }
    });

    zone.addEventListener("drop", function (event) {
      if (!dragged) return;
      event.preventDefault();
      var module = dragged;
      zone.insertBefore(module, before(zone, event.clientY));
      settle(module, zone);
      save(zone);
    });
  });

  chapter.addEventListener("change", function (event) {
    var select = event.target;
    if (!select.matches || !select.matches("select[data-move]")) return;
    var module = select.closest("details.module");
    var zone = zoneOf(select.value);
    if (!module || !zone) return;
    // En fin de section : c'est la que l'on cherche un QCM qu'on vient d'y
    // envoyer.
    zone.insertBefore(module, zone.querySelector(".drop-hint"));
    settle(module, zone);
    save(zone).then(function () {
      module.scrollIntoView({ block: "nearest" });
      select.focus();
    });
  });

  // Renommer : le bouton vit dans un <summary>, d'ou le preventDefault qui
  // evite de replier la section dans le meme geste.
  chapter.addEventListener("click", function (event) {
    var button = event.target.closest && event.target.closest("[data-rename]");
    if (!button) return;
    event.preventDefault();
    var title = window.prompt("Nouveau nom de la section :",
                              button.getAttribute("data-title"));
    if (title === null || !title.trim()) return;
    var form = document.getElementById("section-ren-" + button.getAttribute("data-rename"));
    form.elements.title.value = title.trim();
    form.submit();
  });
})();
