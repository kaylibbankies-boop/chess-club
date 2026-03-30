<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Chess Club • Pretoria</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body class="bg-gray-50 dark:bg-zinc-950">
  <div class="flex h-screen">
    <!-- Sidebar -->
    <div class="w-72 bg-white dark:bg-zinc-900 border-r border-gray-200 dark:border-zinc-800 flex flex-col">
      <div class="p-8 border-b border-gray-200 dark:border-zinc-800">
        <h1 class="text-4xl font-bold flex items-center gap-3">
          ♟️ <span class="text-amber-600">Chess Club</span>
        </h1>
        <p class="text-gray-500 mt-1">Pretoria, South Africa</p>
      </div>

      <nav class="flex-1 p-4">
        <ul class="space-y-1" id="nav-menu">
          <li onclick="navigate('leaderboard')" class="nav-item active flex items-center gap-3 px-5 py-4 rounded-2xl text-lg cursor-pointer"><i class="fas fa-trophy"></i> Leaderboard</li>
          <li onclick="navigate('members')" class="nav-item flex items-center gap-3 px-5 py-4 rounded-2xl text-lg cursor-pointer"><i class="fas fa-users"></i> Members</li>
          <li onclick="navigate('record')" class="nav-item flex items-center gap-3 px-5 py-4 rounded-2xl text-lg cursor-pointer"><i class="fas fa-chess-knight"></i> Record Match</li>
          <li onclick="navigate('history')" class="nav-item flex items-center gap-3 px-5 py-4 rounded-2xl text-lg cursor-pointer"><i class="fas fa-history"></i> Match History</li>
        </ul>
      </nav>
    </div>

    <!-- Main Area -->
    <div class="flex-1 flex flex-col">
      <header class="h-16 bg-white dark:bg-zinc-900 border-b flex items-center px-8 justify-between">
        <h2 id="page-title" class="text-3xl font-semibold">Leaderboard</h2>
        <div class="flex items-center gap-4">
          <div id="status" class="text-sm text-emerald-600 flex items-center gap-2">
            <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></span>
            Connected
          </div>
        </div>
      </header>

      <div class="flex-1 overflow-auto p-8" id="main-content">
        <!-- Content loaded by JS -->
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div id="toast" class="hidden fixed bottom-6 right-6 bg-zinc-800 text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3"></div>

  <script src="/static/js/app.js"></script>
</body>
</html>