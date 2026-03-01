import "./style.css";

const els = {
  mode: document.getElementById("mode"),
  serverSelect: document.getElementById("serverSelect"),
  btnDiscover: document.getElementById("btnDiscover"),
  btnRefresh: document.getElementById("btnRefresh"),
  btnStart: document.getElementById("btnStart"),
  btnStop: document.getElementById("btnStop"),
  search: document.getElementById("search"),
  startName: document.getElementById("startName"),
  procBody: document.getElementById("procBody"),
  logs: document.getElementById("logs"),
  kpiServer: document.getElementById("kpiServer"),
  kpiCount: document.getElementById("kpiCount"),
  kpiLast: document.getElementById("kpiLast"),
};

let processes = [];

function log(msg) {
  const ts = new Date().toLocaleTimeString();
  els.logs.textContent += `[${ts}] ${msg}\n`;
}

function mockDiscover() {
  els.serverSelect.innerHTML = `
    <option>Server-A</option>
    <option>Server-B</option>
  `;
  log("Servidores encontrados: 2");
}

function mockList() {
  processes = [
    { pid: 101, name: "nginx", status: "RUNNING", cpu: 1.2, ram: 120 },
    { pid: 202, name: "postgres", status: "RUNNING", cpu: 2.5, ram: 350 }
  ];
  renderProcesses();
}

function renderProcesses() {
  els.procBody.innerHTML = processes.map(p => `
    <tr>
      <td>${p.pid}</td>
      <td>${p.name}</td>
      <td>${p.status}</td>
      <td>${p.cpu}</td>
      <td>${p.ram}</td>
    </tr>
  `).join("");

  els.kpiCount.textContent = processes.length;
  els.kpiLast.textContent = new Date().toLocaleTimeString();
}

els.btnDiscover.addEventListener("click", mockDiscover);
els.btnRefresh.addEventListener("click", mockList);

log("App iniciada.");