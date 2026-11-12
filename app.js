const assets = [
  { name: 'Compresor industrial A', location: 'Planta norte', state: 'Operativo', icon: '◉' },
  { name: 'Banda transportadora 02', location: 'Línea de producción', state: 'Revisión próxima', icon: '▤', attention: true },
  { name: 'Generador eléctrico', location: 'Cuarto técnico', state: 'Operativo', icon: 'ϟ' },
  { name: 'Bomba hidráulica B', location: 'Planta sur', state: 'Operativo', icon: '◌' },
];
let orders = [
  { title: 'Inspección de filtros', asset: 'Compresor industrial A', owner: 'Laura Méndez', priority: 'Media', state: 'En progreso' },
  { title: 'Ajuste de tensión', asset: 'Banda transportadora 02', owner: 'Carlos Rojas', priority: 'Alta', state: 'Abierta' },
  { title: 'Lubricación preventiva', asset: 'Bomba hidráulica B', owner: 'Ana Torres', priority: 'Baja', state: 'Abierta' },
  { title: 'Cambio de rodamiento', asset: 'Ventilador extractor 01', owner: 'Luis Pérez', priority: 'Baja', state: 'Cerrada' },
];
const stories = [
  ['HU-01', 'Como técnico, quiero consultar el inventario de activos para planificar su mantenimiento.'],
  ['HU-02', 'Como supervisor, quiero registrar activos con ubicación para mantener el inventario actualizado.'],
  ['HU-03', 'Como técnico, quiero crear órdenes de trabajo con prioridad y activo asociado.'],
  ['HU-04', 'Como coordinador, quiero revisar el estado de órdenes y activos para priorizar tareas.'],
  ['HU-05', 'Como estudiante, quiero consultar mis historias y los cambios de mi repositorio para verificar mi trabajo individual.'],
];
let showAllOrders = false;
const orderList = document.querySelector('#order-list');
const assetList = document.querySelector('#asset-list');
const storyList = document.querySelector('#story-list');
const orderDialog = document.querySelector('#order-dialog');
const assetDialog = document.querySelector('#asset-dialog');
const toast = document.querySelector('#toast');
let toastTimer;

function renderOrders() {
  orderList.innerHTML = (showAllOrders ? orders : orders.slice(0, 3)).map(order => {
    const priorityClass = { Alta: 'high', Media: 'medium', Baja: 'low' }[order.priority] || 'low';
    const stateClass = { Abierta: 'open', 'En progreso': 'progress', Cerrada: 'done' }[order.state] || 'open';
    return `<tr><td><span class="order-title">${escapeHtml(order.title)}</span><span class="order-sub">${escapeHtml(order.asset)}</span></td><td>${escapeHtml(order.owner)}</td><td><span class="priority ${priorityClass}">${escapeHtml(order.priority)}</span></td><td><span class="state ${stateClass}">${escapeHtml(order.state)}</span></td></tr>`;
  }).join('');
  document.querySelector('#open-count').textContent = String(orders.filter(order => order.state !== 'Cerrada').length).padStart(2, '0');
}

function renderAssets() {
  assetList.innerHTML = assets.slice(0, 4).map(asset => `<div class="asset-row"><div class="asset-info"><span class="asset-symbol" aria-hidden="true">${asset.icon}</span><div><strong>${escapeHtml(asset.name)}</strong><small>${escapeHtml(asset.location)}</small></div></div><span class="asset-health ${asset.attention ? 'attention' : ''}">${escapeHtml(asset.state)}</span></div>`).join('');
  document.querySelector('#asset-count').textContent = String(assets.length + 4).padStart(2, '0');
  document.querySelector('#order-asset').innerHTML = assets.map(asset => `<option>${escapeHtml(asset.name)}</option>`).join('');
}

function renderStories() {
  storyList.innerHTML = stories.map(([id, description]) => `<article class="story-card"><span class="story-number">${id}</span><p>${escapeHtml(description)}</p><span class="implemented">✓ Implementada</span></article>`).join('');
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('visible'), 2800);
}

document.querySelector('#new-order').addEventListener('click', () => orderDialog.showModal());
document.querySelector('#new-asset').addEventListener('click', () => assetDialog.showModal());
document.querySelector('#order-form').addEventListener('submit', event => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  orders.unshift({ title: form.get('title').trim(), asset: form.get('asset'), owner: 'Maikol Lozano', priority: form.get('priority'), state: 'Abierta' });
  renderOrders();
  event.currentTarget.reset();
  orderDialog.close();
  showToast('Orden de trabajo creada.');
});
document.querySelector('#asset-form').addEventListener('submit', event => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  assets.unshift({ name: form.get('name').trim(), location: form.get('location').trim(), state: 'Operativo', icon: '▤' });
  renderAssets();
  event.currentTarget.reset();
  assetDialog.close();
  showToast('Activo registrado correctamente.');
});
document.querySelector('#show-all').addEventListener('click', event => {
  const button = event.currentTarget;
  const showingAll = button.dataset.all === 'true';
  showAllOrders = !showingAll;
  button.dataset.all = String(showAllOrders);
  button.innerHTML = showAllOrders ? 'Mostrar recientes <span>↑</span>' : 'Ver todas <span>→</span>';
  renderOrders();
  showToast(showingAll ? 'Mostrando órdenes recientes.' : 'Mostrando todas las órdenes registradas.');
});
renderOrders();
renderAssets();
renderStories();
