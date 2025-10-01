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

<Header />

<svelte:head>
	<title>Weighly Events</title>
</svelte:head>

<main>
  {#if events.length === 0}
    <p>No events yet…</p>
  {:else}
    <ul>
      {#each events as event}
        <li>
          <strong>{event.name}</strong> (id: {event.event_id})
        </li>
      {/each}
    </ul>
  {/if}
</main>