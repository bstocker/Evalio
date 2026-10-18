/* Liste de classe, cote enseignant : le QR code, le lien vers sa
   projection, et les inscrits relus toutes les 3 secondes.
   PythonAnywhere n'offre pas de WebSocket : on interroge le serveur, comme
   le suivi direct d'une session (cf. admin_live.js). */
(function () {
  "use strict";

  var POLL_MS = 3000;

  var body = document.getElementById("entries");
  var empty = document.getElementById("empty");
  var count = document.getElementById("count");
  var stamp = document.getElementById("live-stamp");

  // Le QR code est dessine ici, dans le navigateur : aucune dependance de
  // plus a installer sur le serveur. Niveau de correction M, et une marge
  // de quatre modules, celle que demande la norme pour etre lu.
  function drawQr(box) {
    if (!box || typeof qrcode !== "function") return;
    var qr = qrcode(0, "M");
    qr.addData(box.getAttribute("data-url"));
    qr.make();
    box.innerHTML = qr.createSvgTag({ cellSize: 8, margin: 32, scalable: true });
  }
  drawQr(document.getElementById("qr"));

  function cell(text) {
    var td = document.createElement("td");
    td.textContent = text;
    return td;
  }

  function remove(entry, button) {
    if (!confirm("Retirer " + entry.first_name + " " + entry.last_name
                 + " de la liste ?")) return;
    button.disabled = true;
    fetch(window.ROSTER_DELETE.replace("/0/delete", "/" + entry.id + "/delete"),
          { method: "POST", credentials: "same-origin" })
      .then(refresh, function () { button.disabled = false; });
  }

  function render(data) {
    count.textContent = data.count;
    empty.hidden = data.count > 0;
    body.textContent = "";
    data.entries.forEach(function (entry) {
      var tr = document.createElement("tr");
      tr.appendChild(cell(entry.last_name));
      tr.appendChild(cell(entry.first_name));
      var at = cell(entry.at);
      at.className = "mono";
      tr.appendChild(at);
      var actions = document.createElement("td");
      actions.className = "row-actions";
      var button = document.createElement("button");
      button.type = "button";
      button.className = "ghost danger-text";
      button.textContent = "Retirer";
      button.addEventListener("click", function () { remove(entry, button); });
      actions.appendChild(button);
      tr.appendChild(actions);
      body.appendChild(tr);
    });
  }

  function refresh() {
    return fetch(window.ROSTER_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (r.status === 401) {
          stamp.textContent = "session enseignant expirée";
          throw new Error("401");
        }
        return r.json();
      })
      .then(function (data) {
        render(data);
        stamp.textContent = "à jour · " + new Date().toLocaleTimeString("fr-FR");
        stamp.className = "pill ok";
      })
      .catch(function () {
        stamp.className = "pill warn";
        if (stamp.textContent.indexOf("expirée") < 0) {
          stamp.textContent = "connexion perdue";
        }
      });
  }

  refresh();
  setInterval(function () {
    if (!document.hidden) refresh();
  }, POLL_MS);

  // Projection : une fenetre a part, que l'enseignant glisse sur l'ecran
  // du videoprojecteur. Sa page continue de vivre pendant qu'il travaille
  // ailleurs. Sans JavaScript, le lien l'ouvre dans un nouvel onglet.
  var project = document.getElementById("project");
  project.addEventListener("click", function (event) {
    var win = window.open(project.href, project.target,
                          "popup,width=960,height=1000");
    if (win) {
      event.preventDefault();
      win.focus();
    }
  });
})();
