<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';
  import type { User } from '@supabase/supabase-js';
  import { browser } from '$app/environment';
  import { isDark } from '$lib/stores/theme';
  
  let isMobile = false; // Mobile detection
  let user: User | null = null;

  onMount(() => {
    if (!browser) return;

    const mq = window.matchMedia('(max-width: 640px)');
    const update = (e?: MediaQueryListEvent) => (isMobile = mq.matches);

    update(); // set initial value

    // Prefer modern addEventListener/removeEventListener if available.
    if ((mq as any).addEventListener) {
      (mq as any).addEventListener('change', update);
      return () => {
        (mq as any).removeEventListener('change', update);
      };
    }

    // Legacy fallback (older browsers)
    (mq as any).addListener(update);
    return () => {
      (mq as any).removeListener(update);
    };
  });

  onMount(() => {
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

    return () => {
      if (subscription) subscription.unsubscribe();
    };
  });

  async function handleLogout() {
    await supabase.auth.signOut();
    goto('/');
  }
</script>


<header class="topbar h-16" aria-label="Top navigation">
  <div class="brand">
    {#if $isDark}
      {#if isMobile}
        <a href="/"><img src="/weighly_dark_mode_small.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
      {:else}
        <a href="/"><img src="/weighly_dark_mode.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
      {/if}
    {:else}
      {#if isMobile}
        <a href="/"><img src="/weighly_light_mode_small.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
      {:else}
        <a href="/"><img src="/weighly_light_mode.png" alt="Weighly" style="height: 300%; max-height: 3rem; width: auto;"></a>
      {/if}
    {/if}
  </div>

  <nav aria-label="Main">
    <!-- Add links here -->
  </nav>

  <div class="flex items-center gap-3 h-full">
    {#if user}
      <div class="flex items-center gap-2 h-full">
        <!-- <span class="text-sm hidden md:inline">{user.email}</span> -->
        <a class="text-sm hidden md:inline hover:underline" href="/events">{user.email}</a>
        <button 
          on:click={handleLogout}
          class="flex items-center justify-center accent_color_button rounded hover:scale-105 h-[70%] px-4 transition-transform block cursor-pointer"
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
      <button class="theme-toggle flex items-center justify-center rounded hover:scale-105 h-[70%] px-2 transition-transform"
              on:click={() => isDark.update(v => !v)}>
        {#if $isDark}
          <img src="/light_mode.png" alt="Light Mode Icon" class="w-5 h-5">
        {:else}
          <img src="/dark_mode.png" alt="Dark Mode Icon" class="w-5 h-5">
        {/if}
      </button>
    </div>
  </div>
</header>