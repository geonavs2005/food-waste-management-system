/* =========================================================
   Food Waste Management System - JavaScript Client & DSA Visualizers
   ========================================================= */

// --- Global Toast Notification Helper ---
function showToast(message, type = 'success') {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        document.body.appendChild(toast);
    }
    const icon = type === 'error' ? '⚠️' : '✅';
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    toast.style.background = type === 'error' ? '#dc2626' : '#0f172a';
    toast.style.display = 'flex';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3500);
}

// --- Modal Helper Functions ---
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking on overlay background
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// --- Tab Switching Logic ---
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');
            const parent = this.closest('.tabs-container') || document;
            
            parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            parent.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            this.classList.add('active');
            const targetPane = parent.querySelector(`#${targetId}`);
            if (targetPane) targetPane.classList.add('active');
        });
    });
}

// =========================================================
// 1. Food Management (CRUD & Linked List)
// =========================================================
function initFoodModule() {
    const foodForm = document.getElementById('addFoodForm');
    if (foodForm) {
        foodForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(foodForm);
            const payload = Object.fromEntries(formData.entries());

            try {
                const res = await fetch('/api/food', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (res.ok) {
                    showToast(result.message);
                    closeModal('addFoodModal');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(result.message || 'Error adding food item', 'error');
                }
            } catch (err) {
                showToast('Failed to connect to server: ' + err.message, 'error');
            }
        });
    }
}

async function deleteFoodItem(foodId) {
    if (!confirm(`Are you sure you want to delete Food item #${foodId}?`)) return;
    try {
        const res = await fetch(`/api/food/${foodId}`, { method: 'DELETE' });
        const result = await res.json();
        if (res.ok) {
            showToast(result.message);
            setTimeout(() => window.location.reload(), 800);
        } else {
            showToast(result.message, 'error');
        }
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}

// =========================================================
// 2. Donor Module
// =========================================================
function initDonorModule() {
    const form = document.getElementById('addDonorForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            try {
                const res = await fetch('/api/donors', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (res.ok) {
                    showToast(result.message);
                    closeModal('addDonorModal');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(result.message, 'error');
                }
            } catch (err) {
                showToast('Network error: ' + err.message, 'error');
            }
        });
    }
}

async function deleteDonorItem(donorId) {
    if (!confirm(`Delete Donor #${donorId}?`)) return;
    const res = await fetch(`/api/donors/${donorId}`, { method: 'DELETE' });
    const result = await res.json();
    if (res.ok) {
        showToast(result.message);
        setTimeout(() => window.location.reload(), 800);
    } else {
        showToast(result.message, 'error');
    }
}

// =========================================================
// 3. Recipient Module
// =========================================================
function initRecipientModule() {
    const form = document.getElementById('addRecipientForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            try {
                const res = await fetch('/api/recipients', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (res.ok) {
                    showToast(result.message);
                    closeModal('addRecipientModal');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(result.message, 'error');
                }
            } catch (err) {
                showToast('Network error: ' + err.message, 'error');
            }
        });
    }
}

async function deleteRecipientItem(recId) {
    if (!confirm(`Delete Recipient #${recId}?`)) return;
    const res = await fetch(`/api/recipients/${recId}`, { method: 'DELETE' });
    const result = await res.json();
    if (res.ok) {
        showToast(result.message);
        setTimeout(() => window.location.reload(), 800);
    } else {
        showToast(result.message, 'error');
    }
}

// =========================================================
// 4. Request Module & FIFO Queue Processing
// =========================================================
function initRequestModule() {
    const form = document.getElementById('createRequestForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            try {
                const res = await fetch('/api/requests', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                if (res.ok) {
                    showToast(result.message);
                    closeModal('createRequestModal');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(result.message, 'error');
                }
            } catch (err) {
                showToast('Network error: ' + err.message, 'error');
            }
        });
    }
}

async function processNextQueueRequest() {
    try {
        const res = await fetch('/api/requests/process', { method: 'POST' });
        const result = await res.json();
        if (res.ok) {
            showToast(`FIFO Dequeued: Request #${result.processed_item.request_id} for ${result.processed_item.recipient_name}!`);
            setTimeout(() => window.location.reload(), 900);
        } else {
            showToast(result.message, 'error');
        }
    } catch (err) {
        showToast('Processing error: ' + err.message, 'error');
    }
}

// =========================================================
// 5. Stack Undo Demonstration
// =========================================================
async function triggerStackUndo() {
    try {
        const res = await fetch('/api/stack/undo', { method: 'POST' });
        const result = await res.json();
        if (res.ok) {
            showToast(`LIFO Pop: ${result.message}`);
            setTimeout(() => window.location.reload(), 900);
        } else {
            showToast(result.message, 'error');
        }
    } catch (err) {
        showToast('Undo failed: ' + err.message, 'error');
    }
}

// =========================================================
// 6. Tree & BST Canvas Visualizer
// =========================================================
class TreeCanvasRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.highlightNodes = new Set();
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        if (!this.canvas) return;
        this.canvas.width = this.canvas.parentElement.clientWidth;
        this.canvas.height = this.canvas.parentElement.clientHeight || 420;
    }

    drawTree(treeRoot, highlightKey = null) {
        if (!this.canvas || !this.ctx) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        if (!treeRoot) {
            this.ctx.fillStyle = "#94a3b8";
            this.ctx.font = "14px monospace";
            this.ctx.textAlign = "center";
            this.ctx.fillText("Tree is Empty. Insert a node to begin.", this.canvas.width / 2, this.canvas.height / 2);
            return;
        }

        const startX = this.canvas.width / 2;
        const startY = 45;
        const initialOffset = this.canvas.width / 4;

        this._renderNode(treeRoot, startX, startY, initialOffset, highlightKey);
    }

    _renderNode(node, x, y, offset, highlightKey) {
        if (!node) return;
        const radius = 22;

        // Draw branches to children
        this.ctx.strokeStyle = "#94a3b8";
        this.ctx.lineWidth = 2;

        if (node.left) {
            const nextX = x - offset;
            const nextY = y + 70;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y + radius);
            this.ctx.lineTo(nextX, nextY - radius);
            this.ctx.stroke();
            this._renderNode(node.left, nextX, nextY, offset / 2, highlightKey);
        }

        if (node.right) {
            const nextX = x + offset;
            const nextY = y + 70;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y + radius);
            this.ctx.lineTo(nextX, nextY - radius);
            this.ctx.stroke();
            this._renderNode(node.right, nextX, nextY, offset / 2, highlightKey);
        }

        // Draw Node Circle
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
        const isHighlight = highlightKey !== null && String(node.key || node.val) === String(highlightKey);
        this.ctx.fillStyle = isHighlight ? "#ef4444" : "#10b981";
        this.ctx.fill();
        this.ctx.strokeStyle = isHighlight ? "#b91c1c" : "#059669";
        this.ctx.lineWidth = 3;
        this.ctx.stroke();

        // Draw Text inside Node
        this.ctx.fillStyle = "#ffffff";
        this.ctx.font = "bold 12px Segoe UI, sans-serif";
        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "middle";
        this.ctx.fillText(node.key !== undefined ? node.key : node.val, x, y);
    }
}

// =========================================================
// 7. Graph Network Canvas Visualizer
// =========================================================
class GraphCanvasRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.nodePositions = {};
        this.activePath = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        if (!this.canvas) return;
        this.canvas.width = this.canvas.parentElement.clientWidth;
        this.canvas.height = this.canvas.parentElement.clientHeight || 450;
    }

    layoutNodes(vertices) {
        const n = vertices.length;
        if (n === 0) return;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 75;

        vertices.forEach((v, idx) => {
            const angle = (idx / n) * 2 * Math.PI - (Math.PI / 2);
            this.nodePositions[v.name] = {
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle),
                type: v.type
            };
        });
    }

    drawGraph(vertices, edges, highlightedOrder = []) {
        if (!this.canvas || !this.ctx) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (!vertices || vertices.length === 0) {
            this.ctx.fillStyle = "#94a3b8";
            this.ctx.font = "14px monospace";
            this.ctx.textAlign = "center";
            this.ctx.fillText("No Graph Nodes Available", this.canvas.width / 2, this.canvas.height / 2);
            return;
        }

        this.layoutNodes(vertices);

        // 1. Draw Edges
        edges.forEach(edge => {
            const uPos = this.nodePositions[edge.from];
            const vPos = this.nodePositions[edge.to];
            if (uPos && vPos) {
                this.ctx.beginPath();
                this.ctx.moveTo(uPos.x, uPos.y);
                this.ctx.lineTo(vPos.x, vPos.y);
                this.ctx.strokeStyle = "#cbd5e1";
                this.ctx.lineWidth = 2.5;
                this.ctx.stroke();

                // Draw distance weight badge
                const midX = (uPos.x + vPos.x) / 2;
                const midY = (uPos.y + vPos.y) / 2;
                this.ctx.fillStyle = "#ffffff";
                this.ctx.fillRect(midX - 12, midY - 9, 24, 18);
                this.ctx.strokeStyle = "#94a3b8";
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(midX - 12, midY - 9, 24, 18);
                
                this.ctx.fillStyle = "#475569";
                this.ctx.font = "bold 10px monospace";
                this.ctx.textAlign = "center";
                this.ctx.textBaseline = "middle";
                this.ctx.fillText(`${edge.distance}k`, midX, midY);
            }
        });

        // 2. Draw Nodes
        vertices.forEach(v => {
            const pos = this.nodePositions[v.name];
            if (!pos) return;

            const isVisited = highlightedOrder.includes(v.name);
            const visitIndex = highlightedOrder.indexOf(v.name);

            this.ctx.beginPath();
            this.ctx.arc(pos.x, pos.y, 24, 0, 2 * Math.PI);
            
            // Color according to node type or traversal visit
            if (isVisited) {
                this.ctx.fillStyle = "#f59e0b"; // Highlight visited in amber
            } else if (v.type === 'Donor Hub') {
                this.ctx.fillStyle = "#10b981";
            } else if (v.type === 'Collection Center') {
                this.ctx.fillStyle = "#0ea5e9";
            } else {
                this.ctx.fillStyle = "#8b5cf6";
            }
            this.ctx.fill();

            this.ctx.strokeStyle = isVisited ? "#b45309" : "#ffffff";
            this.ctx.lineWidth = 3;
            this.ctx.stroke();

            // Label
            this.ctx.fillStyle = "#ffffff";
            this.ctx.font = "bold 11px Segoe UI, sans-serif";
            this.ctx.textAlign = "center";
            this.ctx.textBaseline = "middle";
            const initial = isVisited ? `#${visitIndex + 1}` : v.name.substring(0, 3).toUpperCase();
            this.ctx.fillText(initial, pos.x, pos.y);

            // Full text underneath
            this.ctx.fillStyle = "#0f172a";
            this.ctx.font = "600 11px Segoe UI, sans-serif";
            this.ctx.fillText(v.name, pos.x, pos.y + 36);
        });
    }

    animateTraversal(vertices, edges, traversalOrder) {
        let currentStep = 0;
        const interval = setInterval(() => {
            if (currentStep > traversalOrder.length) {
                clearInterval(interval);
                return;
            }
            const currentSublist = traversalOrder.slice(0, currentStep);
            this.drawGraph(vertices, edges, currentSublist);
            currentStep++;
        }, 600);
    }
}

// --- Initialize Page Scripts on DOMContentLoaded ---
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initFoodModule();
    initDonorModule();
    initRecipientModule();
    initRequestModule();
});
