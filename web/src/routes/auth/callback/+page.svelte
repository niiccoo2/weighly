<script lang="ts">
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let loading = false;
  let error: string | null = null;

  async function signInWithGoogle() {
    try {
      loading = true;
      
      // Configure redirect with the current origin
      const { data, error: signInError } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });
      
      if (signInError) throw signInError;
      
      // The user will be redirected to Google for authentication
    } catch (e) {
      error = (e instanceof Error) ? e.message : String(e);
      console.error('Error signing in with Google:', e);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    // check if already signed in and redirect
    supabase.auth.getSession().then(({ data }) => {
      if (data.session) {
        goto('/events');
      }
    });
  });
</script>

<svelte:head>
  <title>Login - Weighly</title>
</svelte:head>

<Header />

<div class="flex items-center justify-center min-h-[70vh]">
  <div class="w-full max-w-md p-8 space-y-8 card rounded-xl shadow-lg">
    
  </div>
</div>