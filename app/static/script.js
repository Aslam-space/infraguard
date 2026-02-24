// ==============================================================
// InfraGuard Dashboard — Live JavaScript Engine
// ==============================================================

const socket = io();

// Chart data storage
const maxPoints = 20;
const labels    = Array(maxPoints).fill('');
const cpuData   = Array(maxPoints).fill(0);
const ramData   = Array(maxPoints).fill(0);
const netInData = Array(maxPoints).fill(0);
const netOutData= Array(maxPoints).fill(0);

// ==============================================================
// Charts
// ==============================================================
const cpuChart = new Chart(document.getElementById('cpuChart'), {
  type: 'line',
  data: {
    labels,
    datasets: [
      { label: 'CPU %',  data: cpuData,  borderColor: '#00d4ff',
        backgroundColor: '#00d4ff11', tension: 0.4, fill: true, pointRadius: 0 },
      { label: 'RAM %',  data: ramData,  borderColor: '#00ff88',
        backgroundColor: '#00ff8811', tension: 0.4, fill: true, pointRadius: 0 }
    ]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      x: { display: false },
      y: { min: 0, max: 100,
           ticks: { color: '#666', callback: v => v + '%' },
           grid:  { color: '#111130' } }
    },
    plugins: { legend: { labels: { color: '#888', font: { size: 10 } } } }
  }
});

const netChart = new Chart(document.getElementById('netChart'), {
  type: 'line',
  data: {
    labels,
    datasets: [
      { label: 'Net In',  data: netInData,  borderColor: '#ffaa00',
        backgroundColor: '#ffaa0011', tension: 0.4, fill: true, pointRadius: 0 },
      { label: 'Net Out', data: netOutData, borderColor: '#ff4444',
        backgroundColor: '#ff444411', tension: 0.4, fill: true, pointRadius: 0 }
    ]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      x: { display: false },
      y: { ticks: { color: '#666' }, grid: { color: '#111130' } }
    },
    plugins: { legend: { labels: { color: '#888', font: { size: 10 } } } }
  }
});

// ==============================================================
// WebSocket — live metric updates
// ==============================================================
socket.on('metrics_update', function(m) {
  updateMetricCards(m);
  updateCharts(m);
});

function updateMetricCards(m) {
  // Values
  document.getElementById('cpu-val').textContent  = m.cpu  + '%';
  document.getElementById('ram-val').textContent  = m.ram  + '%';
  document.getElementById('disk-val').textContent = m.disk + '%';
  document.getElementById('proc-val').textContent = m.processes;

  // Bars
  document.getElementById('cpu-bar').style.width  = m.cpu  + '%';
  document.getElementById('ram-bar').style.width  = m.ram  + '%';
  document.getElementById('disk-bar').style.width = m.disk + '%';

  // Status badge
  const badge = document.getElementById('status-badge');
  if (m.cpu > 90 || m.ram > 85 || m.disk > 85) {
    badge.className = 'badge critical';
    badge.textContent = '● CRITICAL';
  } else if (m.cpu > 75 || m.ram > 75 || m.disk > 75) {
    badge.className = 'badge warning';
    badge.textContent = '● WARNING';
  } else {
    badge.className = 'badge nominal';
    badge.textContent = '● NOMINAL';
  }
}

function updateCharts(m) {
  const now = new Date().toLocaleTimeString();
  labels.push(now);     labels.shift();
  cpuData.push(m.cpu);  cpuData.shift();
  ramData.push(m.ram);  ramData.shift();
  netInData.push(m.net_in);   netInData.shift();
  netOutData.push(m.net_out); netOutData.shift();
  cpuChart.update();
  netChart.update();
}

// ==============================================================
// Fetch SLO data every 30 seconds
// ==============================================================
function fetchSLO() {
  fetch('/api/slo')
    .then(r => r.json())
    .then(d => {
      document.getElementById('uptime-val').textContent =
        d.uptime_percent + '%';
      document.getElementById('budget-val').textContent =
        d.error_budget.remaining_minutes + ' min';
      document.getElementById('budget-status').textContent =
        d.error_budget.status;
      document.getElementById('mttr-val').textContent =
        d.avg_mttr + 's';

      const uv = document.getElementById('uptime-val');
      uv.className = 'card-value ' +
        (d.slo_met ? 'green' : 'red');
    });
}

// ==============================================================
// Fetch incidents every 15 seconds
// ==============================================================
function fetchIncidents() {
  fetch('/api/incidents')
    .then(r => r.json())
    .then(incidents => {
      const tbody = document.getElementById('incident-body');
      if (!incidents.length) return;
      tbody.innerHTML = incidents.map(i => `
        <tr>
          <td>${i.timestamp.slice(11,19)}</td>
          <td><span class="type-${i.type.toLowerCase()}">${i.type}</span></td>
          <td>${i.metric_value}%</td>
          <td>${i.mttr_seconds ? i.mttr_seconds+'s' : '...'}</td>
          <td>${i.resolved ? '✅' : '🔄'}</td>
        </tr>
      `).join('');
    });
}

// ==============================================================
// AI Agent
// ==============================================================
function askAgent() {
  const input = document.getElementById('agent-input');
  const prompt = input.value.trim();
  if (!prompt) return;

  addAgentMsg(prompt, 'user');
  input.value = '';
  addAgentMsg('Thinking...', 'system');

  fetch('/api/agent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  })
  .then(r => r.json())
  .then(d => {
    // Remove thinking message
    const log = document.getElementById('agent-log');
    log.removeChild(log.lastChild);
    addAgentMsg(d.response, 'ai');
  })
  .catch(() => addAgentMsg('Agent error — check console', 'error'));
}

function preset(text) {
  document.getElementById('agent-input').value = text;
  askAgent();
}

function addAgentMsg(text, type) {
  const log = document.getElementById('agent-log');
  const div = document.createElement('div');
  div.className = `agent-msg ${type}`;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

// ==============================================================
// Manual Heal
// ==============================================================
function manualHeal() {
  addAgentMsg('Manual heal triggered...', 'system');
  fetch('/api/heal', { method: 'POST' })
    .then(r => r.json())
    .then(d => {
      addAgentMsg(
        d.success
          ? `✅ Healed in ${d.mttr}s`
          : `❌ Heal failed: ${d.output}`,
        d.success ? 'ai' : 'error'
      );
    });
}

// ==============================================================
// Polling fallback if WebSocket disconnects
// ==============================================================
setInterval(() => {
  fetch('/api/metrics')
    .then(r => r.json())
    .then(m => updateMetricCards(m));
}, 10000);

// Start periodic fetches
fetchSLO();
fetchIncidents();
setInterval(fetchSLO,       30000);
setInterval(fetchIncidents, 15000);
