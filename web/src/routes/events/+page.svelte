<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';

  interface Event {
    name: string;
    event_id: number;
    created_at: string;
    custom_url: string | null;
    type_options: string | null;
  }

  let events: Event[] = [];

  onMount(async () => {
    console.log("Fetching allowed events");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_allowed_events", {
      method: "POST",
      headers: {
        apikey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pZmpya3hoanJ0d2xyYW5jZGhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNjQ4NDUsImV4cCI6MjA3NDY0MDg0NX0.dBUGNaqc6-hcYQzEEUKnwD9gPji6RxqHfRhDeUA6hto",
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_id: session.user.id })
    });

    events = await res.json();
    console.log("Fetched events:", events);
  });
</script>

<svelte:head>
	<title>Weighly Events</title>
</svelte:head>

<main class="flex flex-col items-center mt-8">
  <p class="text-xl font-semibold mb-4">Your Events:</p>
  {#if events.length === 0}
    <p>No events yet. Are you signed in?</p>
  {:else}
    <div class="flex flex-col items-center space-y-4 w-full">
      {#each events as event}
        <div class="relative w-full max-w-md">
          <a
            href="/{event.event_id}"
            class="block p-4 card rounded-xl shadow-lg hover:scale-105 transition-transform"
          >
            <div class="text-center">
              <p class="text-2xl thick_text">{event.name}</p>
            </div>
          </a>

          <button
            class="absolute top-1/2 right-3 -translate-y-1/2 bg-blue-500 text-white px-3 py-1 rounded-md hover:bg-blue-600"
          >
            Edit
          </button>
        </div>

      {/each}
      
    </div>
  {/if}
  <a
          href="/new_event"
          class="w-full max-w-md p-4 card rounded-xl shadow-lg hover:scale-105 transition-transform block mt-4"
        >
          <div class="text-center">
            <p class="text-2xl thick_text">New Event</p>
          </div>
        </a>
</main>