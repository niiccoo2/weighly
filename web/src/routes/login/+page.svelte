<script lang="ts">
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let loading: boolean = false;
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
      console.log('Window location:', window.location.origin);

      if (signInError) throw signInError;
      
      // The user will be redirected to Google for authentication
    } catch (e) {
      error = typeof e === 'object' && e !== null && 'message' in e ? (e as { message: string }).message : String(e);
      console.error('Error signing in with Google:', e);
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Login - Weighly</title>
</svelte:head>

<Header />

<div class="flex items-center justify-center min-h-[70vh]">
  <div class="w-full max-w-md p-8 space-y-8 card rounded-xl shadow-lg">
    <div class="text-center">
      <h2 class="mt-6 text-3xl thick_text">Sign In to Weighly</h2>
      <p class="mt-2 text-sm text">Access your account or events</p>
    </div>

    {#if error}
      <div class="p-4 mb-4 bg-red-100 text-red-700 rounded">
        {error}
      </div>
    {/if}

    <div class="mt-8 space-y-6">
      <button 
        on:click={signInWithGoogle}
        disabled={loading}
        class="w-full flex items-center justify-center py-3 px-4 rounded-md shadow-sm accent_color_button hover:bg-gray-50 text-gray-700 font-medium hover:scale-105 transition-transform block"
      >
        <!-- <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google" class="h-5 w-5 mr-2" /> -->
        {loading ? 'Signing in...' : 'Sign in with Google'}
      </button>
    </div>
  </div>
</div>