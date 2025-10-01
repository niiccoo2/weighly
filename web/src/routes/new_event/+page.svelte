<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';

  let event_id: number | null = null;

  async function makeEvent(user_id: string, name: string, type_options: string[] | null, custom_url: string | null) {
    console.log("Sending POST request for new event");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/create_event", {
      method: "POST",
      headers: {
        apikey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pZmpya3hoanJ0d2xyYW5jZGhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNjQ4NDUsImV4cCI6MjA3NDY0MDg0NX0.dBUGNaqc6-hcYQzEEUKnwD9gPji6RxqHfRhDeUA6hto",
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ p_user_id: session.user.id,
                             p_name: name,
                             p_type_options: type_options,
                             p_custom_url: custom_url
       })
    });

    event_id = await res.json();
    console.log("Fetched events:", event_id);
    }
  
</script>

<Header />

<svelte:head>
	<title>Weighly Events</title>
</svelte:head>

<main class="flex flex-col items-center mt-8">
  <p class="text-xl font-semibold mb-4">Your Events:</p>
  {#if events.length === 0}
    <p>No events yet…</p>
  {:else}
    <div class="flex flex-col items-center space-y-4 w-full">
      {#each events as event}
        <a
          href="/{event.event_id}"
          class="w-full max-w-md p-4 card rounded-xl shadow-lg hover:scale-105 transition-transform block"
        >
          <div class="text-center">
            <p class="text-2xl thick_text">{event.name}</p>
          </div>
        </a>
      {/each}
    </div>
  {/if}
</main>
