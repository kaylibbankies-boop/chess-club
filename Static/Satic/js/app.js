const API_BASE = 'http://127.0.0.1:5000/api';

let allMembers = [];
let allMatches = [];
let currentUser = null;
let currentPreviewUrl = null;
let editingId = null;

function showToast(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.style.cssText = `position:fixed;bottom:30px;right:30px;padding:16px 26px;border-radius:9999px;color:white;z-index:10000;font-weight:500;`;
  toast.style.background = type === 'success' ? '#10b981' : '#ef4444';
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4500);
}

function checkAuth() {
  const saved = localStorage.getItem('currentUser');
  if (saved) currentUser = JSON.parse(saved);
}

// ==================== CREATE / EDIT MODAL ====================
function showMemberModal(isEdit = false, member = {}) {
  editingId = isEdit ? member.id : null;
  if (currentPreviewUrl) URL.revokeObjectURL(currentPreviewUrl);
  currentPreviewUrl = null;

  const title = isEdit ? "Edit Profile" : "Create New Account";
  const btnText = isEdit ? "Save Changes" : "Create Account";

  const html = `
    <div id="member-modal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-[300]">
      <div class="bg-zinc-900 rounded-3xl w-full max-w-lg overflow-hidden">
        <div class="px-8 py-6 border-b border-zinc-800 flex justify-between items-center">
          <h3 class="text-2xl font-semibold">${title}</h3>
          <button onclick="closeMemberModal()" class="text-3xl text-zinc-400 hover:text-white">×</button>
        </div>
        <form id="member-form" class="p-8 space-y-6">
          <div class="flex flex-col items-center">
            <div id="profile-preview" onclick="document.getElementById('profile-upload').click()" 
                 class="w-32 h-32 rounded-3xl bg-zinc-800 border-2 border-dashed border-zinc-700 flex items-center justify-center cursor-pointer hover:border-amber-500 overflow-hidden">
              <div id="preview-content" class="text-center w-full h-full">
                <i class="fas fa-camera text-4xl text-zinc-500"></i>
                <p class="text-xs text-zinc-500 mt-2">Upload Profile Photo</p>
              </div>
            </div>
            <input type="file" id="profile-upload" accept="image/*" class="hidden" onchange="handleProfilePreview(event)">
          </div>

          <div>
            <label class="block text-sm text-zinc-400 mb-1.5">Full Name</label>
            <input type="text" id="full_name" value="${member.full_name || ''}" required 
                   class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-3.5 focus:border-amber-500 outline-none">
          </div>

          <div>
            <label class="block text-sm text-zinc-400 mb-1.5">Email Address</label>
            <input type="email" id="email" value="${member.email || ''}" required 
                   class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-3.5 focus:border-amber-500 outline-none">
          </div>

          ${!isEdit ? `
          <div>
            <label class="block text-sm text-zinc-400 mb-1.5">Password</label>
            <input type="password" id="password" required minlength="6"
                   class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-3.5 focus:border-amber-500 outline-none">
          </div>` : ''}

          <div>
            <label class="block text-sm text-zinc-400 mb-1.5">Birthday (optional)</label>
            <input type="date" id="birthday" value="${member.birthday || ''}"
                   class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-3.5 focus:border-amber-500 outline-none">
          </div>

          <div class="pt-6 flex gap-4">
            <button type="button" onclick="closeMemberModal()" class="flex-1 py-4 bg-zinc-800 hover:bg-zinc-700 rounded-2xl font-medium">Cancel</button>
            <button type="submit" class="flex-1 py-4 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 rounded-2xl font-semibold">${btnText}</button>
          </div>
        </form>
      </div>
    </div>`;

  document.body.insertAdjacentHTML('beforeend', html);
  document.getElementById('member-form').addEventListener('submit', handleMemberSubmit);
}

function handleProfilePreview(e) {
  const file = e.target.files[0];
  if (!file) return;
  if (currentPreviewUrl) URL.revokeObjectURL(currentPreviewUrl);
  currentPreviewUrl = URL.createObjectURL(file);
  document.getElementById('preview-content').innerHTML = `<img src="${currentPreviewUrl}" class="w-full h-full object-cover rounded-3xl">`;
}

async function handleMemberSubmit(e) {
  e.preventDefault();
  const formData = new FormData();
  formData.append('full_name', document.getElementById('full_name').value.trim());
  formData.append('email', document.getElementById('email').value.trim());
  formData.append('birthday', document.getElementById('birthday').value);

  if (!editingId) {
    const passwordField = document.getElementById('password');
    if (passwordField && passwordField.value) formData.append('password', passwordField.value);
  }

  const fileInput = document.getElementById('profile-upload');
  if (fileInput.files[0]) formData.append('profile_picture', fileInput.files[0]);

  const url = editingId ? `${API_BASE}/members/${editingId}` : `${API_BASE}/members`;
  const method = editingId ? 'PUT' : 'POST';

  try {
    const res = await fetch(url, { method, body: formData });
    const data = await res.json();
    if (res.ok) {
      showToast(editingId ? "Profile updated!" : "Account created! Welcome ♟️", "success");
      if (!editingId && data.user) {
        currentUser = data.user;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
      }
      closeMemberModal();
      navigate('members');
    } else {
      showToast(data.message || "Failed to save", "error");
    }
  } catch (err) {
    showToast("Cannot connect to backend", "error");
  }
}

function closeMemberModal() {
  if (currentPreviewUrl) URL.revokeObjectURL(currentPreviewUrl);
  currentPreviewUrl = null;
  const modal = document.getElementById('member-modal');
  if (modal) modal.remove();
}

// ==================== LOGIN ====================
function showLoginModal() {
  const html = `
    <div id="login-modal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-[300]">
      <div class="bg-zinc-900 rounded-3xl w-full max-w-md p-8">
        <h3 class="text-2xl font-bold text-center mb-8">Login to Chess Club</h3>
        <input id="login-email" type="email" placeholder="Email" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-4 mb-4">
        <input id="login-password" type="password" placeholder="Password" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-5 py-4 mb-6">
        <button onclick="handleLogin()" class="w-full py-4 bg-amber-600 hover:bg-amber-500 rounded-2xl font-semibold mb-4">Login</button>
        <button onclick="showMemberModal(false)" class="w-full py-4 bg-zinc-800 hover:bg-zinc-700 rounded-2xl font-medium">Create New Account</button>
        <button onclick="closeLoginModal()" class="mt-6 w-full text-zinc-400">Close</button>
      </div>
    </div>`;
  document.body.insertAdjacentHTML('beforeend', html);
}

async function handleLogin() {
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  if (!email || !password) return showToast("Email and password required", "error");

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
      currentUser = data.user;
      localStorage.setItem('currentUser', JSON.stringify(currentUser));
      showToast(`Welcome back, ${currentUser.full_name}!`, "success");
      closeLoginModal();
      navigate('members');
    } else {
      showToast(data.message || "Invalid credentials", "error");
    }
  } catch (err) {
    showToast("Cannot connect to server", "error");
  }
}

function closeLoginModal() {
  const modal = document.getElementById('login-modal');
  if (modal) modal.remove();
}

function logout() {
  currentUser = null;
  localStorage.removeItem('currentUser');
  showToast('Logged out successfully');
  navigate('members');
}

// ==================== NAVIGATION ====================
function navigate(page) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const active = document.querySelector(`[onclick="navigate('${page}')"]`);
  if (active) active.classList.add('active');

  document.getElementById('page-title').textContent = 
    page === 'members' ? 'Members' : 
    page === 'record' ? 'Record Match' :
    page === 'leaderboard' ? 'Leaderboard' : 'Match History';

  if (page === 'members') loadMembersPage();
  if (page === 'record') loadRecordMatchPage();
  if (page === 'leaderboard') loadLeaderboard();
  if (page === 'history') loadMatchHistory();
}

// ==================== MEMBERS PAGE ====================
async function loadMembersPage() {
  try {
    const res = await fetch(`${API_BASE}/members`);
    allMembers = await res.json();
  } catch (e) {
    showToast("Failed to load members", "error");
    allMembers = [];
  }

  const userHTML = currentUser ? `
    <div class="flex items-center gap-4">
      ${currentUser.profile_picture ? `<img src="${currentUser.profile_picture}" class="w-9 h-9 rounded-2xl object-cover">` : `<div class="w-9 h-9 bg-amber-600 rounded-2xl flex items-center justify-center text-lg">${currentUser.full_name[0]}</div>`}
      <div>
        <div class="font-medium">${currentUser.full_name}</div>
        <div class="text-amber-400 text-xs">ELO ${currentUser.elo || 1200}</div>
      </div>
      <button onclick="logout()" class="text-xs px-4 py-1 bg-red-900/30 hover:bg-red-900/50 rounded-xl">Logout</button>
    </div>` : `<button onclick="showLoginModal()" class="bg-amber-600 px-6 py-3 rounded-2xl">Login</button>`;

  document.getElementById('header-user').innerHTML = userHTML;

  let html = `
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-semibold">Club Members</h2>
      <button onclick="showMemberModal(false)" class="bg-gradient-to-r from-amber-600 to-orange-600 px-7 py-3.5 rounded-2xl font-semibold flex items-center gap-2">
        <i class="fas fa-plus"></i> Add Member
      </button>
    </div>
    <div class="bg-zinc-900 rounded-3xl overflow-hidden border border-zinc-800">
      <table class="w-full">
        <thead>
          <tr class="border-b border-zinc-800 text-zinc-400 text-sm">
            <th class="p-6 text-left">Rank</th>
            <th class="p-6 text-left">Player</th>
            <th class="p-6 text-left">Email</th>
            <th class="p-6 text-center">ELO</th>
            <th class="p-6 text-center">Actions</th>
          </tr>
        </thead>
        <tbody id="members-tbody"></tbody>
      </table>
    </div>`;

  document.getElementById('main-content').innerHTML = html;
  renderMembersTable();
}

function renderMembersTable() {
  const tbody = document.getElementById('members-tbody');
  let html = '';

  allMembers.forEach(m => {
    const isOwn = currentUser && currentUser.id === m.id;
    const avatar = m.profile_picture 
      ? `<img src="${m.profile_picture}" class="w-11 h-11 rounded-2xl object-cover">` 
      : `<div class="w-11 h-11 bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl flex items-center justify-center text-white font-bold text-2xl">${m.full_name[0]}</div>`;

    html += `
      <tr class="border-b border-zinc-800 hover:bg-zinc-800/60">
        <td class="p-6 font-mono text-amber-400">#${m.current_rank || '—'}</td>
        <td class="p-6">
          <div class="flex items-center gap-4">${avatar}<span class="font-semibold">${m.full_name}</span></div>
        </td>
        <td class="p-6 text-zinc-300">${m.email}</td>
        <td class="p-6 text-center font-mono">${m.elo || 1200}</td>
        <td class="p-6 text-center">
          <button onclick="viewProfile(${m.id})" class="px-4 py-1.5 text-amber-400 hover:text-amber-300">View</button>
          ${isOwn ? `<button onclick="showMemberModal(true, ${JSON.stringify(m)})" class="ml-3 px-4 py-1.5 text-blue-400 hover:text-blue-300">Edit</button>` : ''}
        </td>
      </tr>`;
  });

  tbody.innerHTML = html || `<tr><td colspan="5" class="py-24 text-center text-zinc-500">No members yet</td></tr>`;
}

// ==================== RECORD MATCH ====================
function loadRecordMatchPage() {
  const members = allMembers;
  if (members.length < 2) {
    document.getElementById('main-content').innerHTML = `<div class="text-center py-32"><p class="text-3xl text-amber-400">Add at least 2 members first</p></div>`;
    return;
  }

  const html = `
    <div class="max-w-2xl mx-auto px-4">
      <div class="flex items-center gap-4 mb-10">
        <div class="w-14 h-14 bg-amber-500/10 rounded-3xl flex items-center justify-center text-4xl">♟️</div>
        <div><h1 class="text-4xl font-bold text-white">Record New Match</h1><p class="text-zinc-400">Update ratings instantly</p></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <label class="block text-amber-400 font-medium mb-3 text-lg">WHITE PLAYER</label>
          <select id="white-player" onchange="updateEloPreview()" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-6 py-5 text-lg focus:border-amber-500">
            <option value="">Select White...</option>
            ${members.map(m => `<option value="${m.id}">${m.full_name} (${m.elo || 1200})</option>`).join('')}
          </select>
        </div>
        <div>
          <label class="block text-zinc-400 font-medium mb-3 text-lg">BLACK PLAYER</label>
          <select id="black-player" onchange="updateEloPreview()" class="w-full bg-zinc-800 border border-zinc-700 rounded-2xl px-6 py-5 text-lg focus:border-amber-500">
            <option value="">Select Black...</option>
            ${members.map(m => `<option value="${m.id}">${m.full_name} (${m.elo || 1200})</option>`).join('')}
          </select>
        </div>
      </div>

      <div class="flex justify-center gap-6 mt-14">
        <button onclick="recordResult('white')" class="px-14 py-7 bg-white text-black rounded-3xl font-bold text-xl hover:bg-amber-400">♔ WHITE WINS</button>
        <button onclick="recordResult('draw')" class="px-14 py-7 bg-zinc-700 hover:bg-zinc-600 rounded-3xl font-bold text-xl">½ DRAW</button>
        <button onclick="recordResult('black')" class="px-14 py-7 bg-zinc-900 border-2 border-zinc-600 hover:border-red-500 rounded-3xl font-bold text-xl">BLACK WINS ♚</button>
      </div>

      <div id="rating-preview" class="hidden mt-16 bg-zinc-900 border border-zinc-700 rounded-3xl p-10">
        <h3 class="text-2xl font-semibold text-amber-400 mb-8 text-center">Live Rating Preview</h3>
        <div id="preview-content"></div>
      </div>
    </div>`;

  document.getElementById('main-content').innerHTML = html;
}

function updateEloPreview() { /* same as before - kept for brevity */ 
  // (You can keep your previous updateEloPreview function here)
  const whiteId = document.getElementById('white-player').value;
  const blackId = document.getElementById('black-player').value;
  if (!whiteId || !blackId || whiteId === blackId) {
    document.getElementById('rating-preview').classList.add('hidden');
    return;
  }
  // ... (paste your previous updateEloPreview logic if you want the preview)
}

async function recordResult(winner) {
  const whiteId = document.getElementById('white-player').value;
  const blackId = document.getElementById('black-player').value;
  if (!whiteId || !blackId || whiteId === blackId) return showToast("Select two different players", "error");

  try {
    const res = await fetch(`${API_BASE}/matches`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ white_id: parseInt(whiteId), black_id: parseInt(blackId), result: winner })
    });
    if (res.ok) {
      showToast(`Match recorded! ${winner.toUpperCase()} wins.`, "success");
      await loadMembersPage();
      setTimeout(() => loadRecordMatchPage(), 1000);
    }
  } catch (err) {
    showToast("Failed to record match", "error");
  }
}

// ==================== LEADERBOARD PAGE ====================
function loadLeaderboard() {
  const sorted = [...allMembers].sort((a, b) => (b.elo || 1200) - (a.elo || 1200));

  let html = `
    <div class="max-w-4xl mx-auto">
      <h2 class="text-4xl font-bold mb-10 flex items-center gap-4"><span>🏆</span> Leaderboard</h2>
      <div class="bg-zinc-900 rounded-3xl overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="border-b border-zinc-800 text-zinc-400">
              <th class="p-6 text-left">Rank</th>
              <th class="p-6 text-left">Player</th>
              <th class="p-6 text-center">ELO</th>
              <th class="p-6 text-center">Games</th>
            </tr>
          </thead>
          <tbody id="leaderboard-tbody"></tbody>
        </table>
      </div>
    </div>`;

  document.getElementById('main-content').innerHTML = html;

  const tbody = document.getElementById('leaderboard-tbody');
  let rows = '';
  sorted.forEach((m, index) => {
    const avatar = m.profile_picture ? `<img src="${m.profile_picture}" class="w-10 h-10 rounded-2xl">` : `<div class="w-10 h-10 bg-amber-500 rounded-2xl flex items-center justify-center text-white">${m.full_name[0]}</div>`;
    rows += `
      <tr class="border-b border-zinc-800 hover:bg-zinc-800/50">
        <td class="p-6 font-bold text-amber-400">#${index + 1}</td>
        <td class="p-6"><div class="flex items-center gap-4">${avatar} ${m.full_name}</div></td>
        <td class="p-6 text-center font-mono">${m.elo || 1200}</td>
        <td class="p-6 text-center">${m.games_played || 0}</td>
      </tr>`;
  });
  tbody.innerHTML = rows;
}

// ==================== MATCH HISTORY PAGE ====================
async function loadMatchHistory() {
  try {
    const res = await fetch(`${API_BASE}/matches`);
    allMatches = await res.json();
  } catch (e) {
    allMatches = [];
  }

  let html = `
    <div class="max-w-4xl mx-auto">
      <h2 class="text-4xl font-bold mb-10">Match History</h2>
      <div class="bg-zinc-900 rounded-3xl overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="border-b border-zinc-800 text-zinc-400 text-sm">
              <th class="p-6 text-left">Date</th>
              <th class="p-6 text-left">White</th>
              <th class="p-6 text-left">Black</th>
              <th class="p-6 text-center">Result</th>
              <th class="p-6 text-center">ELO Change</th>
            </tr>
          </thead>
          <tbody id="history-tbody"></tbody>
        </table>
      </div>
    </div>`;

  document.getElementById('main-content').innerHTML = html;
  renderMatchHistory();
}

function renderMatchHistory() {
  const tbody = document.getElementById('history-tbody');
  let html = '';

  allMatches.forEach(match => {
    const resultText = match.result === 'white' ? 'White Wins' : match.result === 'black' ? 'Black Wins' : 'Draw';
    html += `
      <tr class="border-b border-zinc-800 hover:bg-zinc-800/50">
        <td class="p-6 text-zinc-400">${new Date(match.played_at).toLocaleDateString()}</td>
        <td class="p-6">${match.white_name || 'Player'}</td>
        <td class="p-6">${match.black_name || 'Player'}</td>
        <td class="p-6 text-center font-medium">${resultText}</td>
        <td class="p-6 text-center">
          <span class="text-green-400">+${match.white_change || 0}</span> / 
          <span class="text-red-400">${match.black_change || 0}</span>
        </td>
      </tr>`;
  });

  tbody.innerHTML = html || `<tr><td colspan="5" class="py-20 text-center text-zinc-500">No matches recorded yet</td></tr>`;
}

// ==================== PROFILE VIEW ====================
function viewProfile(memberId) {
  const member = allMembers.find(m => m.id == memberId);
  if (!member) return;

  const isOwn = currentUser && currentUser.id === member.id;

  const html = `
    <div id="profile-modal" class="fixed inset-0 bg-black/90 flex items-center justify-center z-[400]">
      <div class="bg-zinc-900 rounded-3xl w-full max-w-lg overflow-hidden">
        <div class="p-10 text-center">
          <div class="w-40 h-40 mx-auto rounded-3xl overflow-hidden border-4 border-amber-500 mb-6">
            ${member.profile_picture ? `<img src="${member.profile_picture}" class="w-full h-full object-cover">` : `<div class="w-full h-full bg-gradient-to-br from-amber-500 to-orange-600 text-7xl flex items-center justify-center">${member.full_name[0]}</div>`}
          </div>
          <h2 class="text-3xl font-bold">${member.full_name}</h2>
          <p class="text-amber-400 text-xl mt-2">#${member.current_rank || '—'} • ELO ${member.elo || 1200}</p>
          
          <div class="mt-8 grid grid-cols-2 gap-6 text-left bg-zinc-950 p-6 rounded-2xl">
            <div><p class="text-xs text-zinc-500">Email</p><p>${member.email}</p></div>
            <div><p class="text-xs text-zinc-500">Birthday</p><p>${member.birthday || '-'}</p></div>
          </div>

          ${isOwn ? `<button onclick="editOwnProfile()" class="mt-8 w-full py-4 bg-amber-600 rounded-2xl font-semibold">Edit Profile</button>` : ''}
        </div>
        <div class="p-6 border-t border-zinc-800 text-right">
          <button onclick="closeProfileModal()" class="px-8 py-3 bg-zinc-800 hover:bg-zinc-700 rounded-2xl">Close</button>
        </div>
      </div>
    </div>`;
  document.body.insertAdjacentHTML('beforeend', html);
}

function closeProfileModal() {
  const modal = document.getElementById('profile-modal');
  if (modal) modal.remove();
}

function editOwnProfile() {
  closeProfileModal();
  if (currentUser) showMemberModal(true, allMembers.find(m => m.id === currentUser.id));
}

// Initialize
window.onload = () => {
  checkAuth();
  navigate('members');
};

// Global functions
window.navigate = navigate;
window.showMemberModal = showMemberModal;
window.showLoginModal = showLoginModal;
window.logout = logout;
window.closeMemberModal = closeMemberModal;
window.handleProfilePreview = handleProfilePreview;
window.loadRecordMatchPage = loadRecordMatchPage;
window.recordResult = recordResult;
window.loadLeaderboard = loadLeaderboard;
window.loadMatchHistory = loadMatchHistory;
window.viewProfile = viewProfile;
window.closeProfileModal = closeProfileModal;
window.editOwnProfile = editOwnProfile;