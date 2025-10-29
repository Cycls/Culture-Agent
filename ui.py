
header = """
<raw>
<div class="flex flex-col md:flex-row border border-gray-200 rounded-lg bg-white overflow-hidden my-4 max-w-7xl mx-auto" style="align-items: stretch;">
  <div class="flex-1 p-8 md:p-12 flex flex-col">
    <div id="user-greeting" class="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
      Welcome to Culture Agent
    </div>
    <p class="text-gray-600 text-lg sm:text-xl mb-6">
      Your AI-powered cultural anthropologist for exploring new cultures, traditions, and ways of life around the world
    </p>
    <div class="flex justify-start items-center mt-auto">
      <a href="https://github.com/Cycls/Culture-Agent" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-5 py-2.5 bg-black text-white rounded-lg hover:bg-gray-800 transition-all no-underline">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
        <span class="text-sm font-medium">GitHub</span>
      </a>
    </div>
  </div>
  <div class="flex-1 relative min-h-[250px] md:min-h-full" style="display: block;">
    <img 
      src="https://images.unsplash.com/photo-1516146544193-b54a65682f16?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1587" 
      alt="Cultural exploration" 
      class="absolute inset-0 w-full h-full object-cover"
      style="object-fit: cover; object-position: center; display: block;"
    />
  </div>
</div>
</raw>
"""

intro = """
<div class="py-3">
  <div class="flex flex-wrap gap-3 justify-center">
    <a href="https://cycls.com/send/${encodeURIComponent('Tell me about Japanese culture')}" class="group relative inline-flex items-center justify-center px-4 py-2 overflow-hidden font-medium text-gray-700 border-2 border-gray-300 rounded-xl shadow-lg bg-gradient-to-br from-gray-50 to-white focus:outline-none hover:border-gray-400 hover:shadow-xl transition-all whitespace-nowrap text-sm">
      <span>Tell me about Japanese culture</span>
    </a>
    <a href="https://cycls.com/send/${encodeURIComponent('What are some unique traditions in India?')}" class="group relative inline-flex items-center justify-center px-4 py-2 overflow-hidden font-medium text-gray-700 border-2 border-gray-300 rounded-xl shadow-lg bg-gradient-to-br from-gray-50 to-white focus:outline-none hover:border-gray-400 hover:shadow-xl transition-all whitespace-nowrap text-sm">
      <span>What are some unique traditions in India?</span>
    </a>
    <a href="https://cycls.com/send/${encodeURIComponent('Explore Brazilian culture')}" class="group relative inline-flex items-center justify-center px-4 py-2 overflow-hidden font-medium text-gray-700 border-2 border-gray-300 rounded-xl shadow-lg bg-gradient-to-br from-gray-50 to-white focus:outline-none hover:border-gray-400 hover:shadow-xl transition-all whitespace-nowrap text-sm">
      <span>Explore Brazilian culture</span>
    </a>
    <a href="https://cycls.com/send/${encodeURIComponent('What makes Moroccan culture unique?')}" class="group relative inline-flex items-center justify-center px-4 py-2 overflow-hidden font-medium text-gray-700 border-2 border-gray-300 rounded-xl shadow-lg bg-gradient-to-br from-gray-50 to-white focus:outline-none hover:border-gray-400 hover:shadow-xl transition-all whitespace-nowrap text-sm">
      <span>What makes Moroccan culture unique?</span>
    </a>
  </div>
</div>

"""
