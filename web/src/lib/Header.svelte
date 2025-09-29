<script lang="ts">
  import { onMount } from 'svelte';
  let isDark = false;

  // Decide initial theme:
  function detectInitial() {
    const saved = typeof localStorage !== 'undefined' ? localStorage.getItem('theme') : null;
    if (saved === 'dark') return true;
    if (saved === 'light') return false;
    // fall back to system preference
    return typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  onMount(() => {
    isDark = detectInitial();
    document.documentElement.classList.toggle('dark', isDark);
    // Optional: listen to system changes if user hasn't explicitly set a preference
    if (!localStorage.getItem('theme') && window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = (e: MediaQueryListEvent) => {
        isDark = e.matches;
        document.documentElement.classList.toggle('dark', isDark);
      };
      mq.addEventListener?.('change', handler);
      // cleanup if this component ever unmounts
      return () => mq.removeEventListener?.('change', handler);
    }
  });

  function toggleTheme() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);
    try {
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    } catch (e) {
      // ignore private mode errors
    }
  }
</script>

<header class="topbar" aria-label="Top navigation">
  <div class="brand">
    {#if isDark}
        <a href="/"><img src="/weighly_dark_mode.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
    {:else}
        <a href="/"><img src="/weighly_light_mode.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
    {/if}
  </div>

  <nav aria-label="Main">
    <!-- Add links here -->
    
  </nav>

  <div class="flex items-center gap-3 h-full">
  <a href="/login"
     class="flex items-center justify-center accent_color_button p-4 rounded hover:scale-105 max-h-[70%]">
    Login
  </a>

  <div class="controls flex items-center">
    <button class="theme-toggle flex items-center justify-center p-2 max-h-[70%]"
            on:click={toggleTheme}
            aria-pressed={isDark} aria-label="Toggle theme">
      {#if isDark}
        <img src="/light_mode.png" alt="Light Mode Icon" class="w-5 h-5">
      {:else}
        <img src="/dark_mode.png" alt="Dark Mode Icon" class="w-5 h-5">
      {/if}
    </button>
  </div>
</div>

</header>