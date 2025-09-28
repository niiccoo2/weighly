<script lang="ts">
  export let error: Error;
  export let status: number;
</script>

<svelte:head>
  <title>{status} — {error?.message ?? 'Error'}</title>
</svelte:head>

<div class="error-page" style="min-height:80vh;display:flex;align-items:center;justify-content:center;">
  <div style="max-width:720px;padding:2rem;background:white;border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,0.12);text-align:center;">
    <h1 style="font-size:3rem;margin:0 0 0.5rem;">{status}</h1>
    <h2 style="margin:0 0 1rem;color:#333;">{error?.message ?? 'Something went wrong'}</h2>

    <p style="color:#666;margin-bottom:1rem;">
      The page you requested could not be found or an error occurred.
    </p>

    <div style="display:flex;gap:0.5rem;justify-content:center;">
      <a href="/" class="btn" style="padding:0.6rem 1rem;background:#0366d6;color:white;border-radius:6px;text-decoration:none;">Go home</a>
      <button on:click={() => history.back()} style="padding:0.6rem 1rem;border-radius:6px;">Go back</button>
    </div>

    {#if import.meta.env.DEV}
      <details style="margin-top:1rem;text-align:left;">
        <summary style="cursor:pointer;color:#999">Debug info</summary>
        <pre style="white-space:pre-wrap;margin-top:0.5rem;">{String(error?.stack ?? error)}</pre>
      </details>
    {/if}
  </div>
</div>