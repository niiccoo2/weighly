<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';
  import type { User } from '@supabase/supabase-js';
  
  let isDark = false;
  let user: User | null = null;

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
    
    let subscription: { unsubscribe: () => void };
    
    // Check if user is already signed in
    supabase.auth.getSession().then(({ data }) => {
      user = data.session?.user || null;
      
      // Listen for auth changes
      const authListener = supabase.auth.onAuthStateChange(
        (_event, session) => {
          user = session?.user || null;
        }
      );
      
      subscription = authListener.data.subscription;
    });
    
    // Optional: listen to system changes if user hasn't explicitly set a preference
    let cleanupMediaQuery: (() => void) | undefined;
    
    if (!localStorage.getItem('theme') && window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = (e: MediaQueryListEvent) => {
        isDark = e.matches;
        document.documentElement.classList.toggle('dark', isDark);
      };
      mq.addEventListener?.('change', handler);
      
      cleanupMediaQuery = () => {
        mq.removeEventListener?.('change', handler);
      };
    }
    
    // Return the cleanup function
    return () => {
      if (subscription) subscription.unsubscribe();
      if (cleanupMediaQuery) cleanupMediaQuery();
    };
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
  
  async function handleLogout() {
    await supabase.auth.signOut();
    goto('/');
  }
</script>

<header class="topbar h-16" aria-label="Top navigation">
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
    {#if user}
      <div class="flex items-center gap-2 h-full">
        <span class="text-sm hidden md:inline">{user.email}</span>
        <button 
          on:click={handleLogout}
          class="flex items-center justify-center accent_color_button rounded hover:scale-105 h-[70%] px-4 transition-transform block"
        >
          Logout
        </button>
      </div>
    {:else}
      <a href="/login"
         class="flex items-center justify-center accent_color_button rounded hover:scale-105 h-[70%] px-4 transition-transform block">
        Login
      </a>
    {/if}

    <div class="controls flex items-center h-full">
      <button class="theme-toggle flex items-center justify-center rounded hover:scale-105 h-[70%] px-2"
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