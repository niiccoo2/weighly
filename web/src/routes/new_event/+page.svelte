<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';

  let event_id: number | null = null;

  async function makeEvent(name: string, type_options: string[] | null, custom_url: string | null) {
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
  
  async function makeEventAction() {
    if (!value.trim()) {
      error = "Event name cannot be empty.";
      return;
    }
    error = "";
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
      error = "You must be logged in to create an event.";
      return;
    }
    await makeEvent(value.trim(), null, null);
    if (event_id) {
      window.location.href = `/${event_id}`;
    } else {
      error = "Failed to create event. Please try again.";
    }
  }

  export let value: string = "";
  export let placeholder = "Name";
  export let id = "name_input";
  export let error = "";
</script>

<svelte:head>
	<title>New Event</title>
</svelte:head>

<main class="flex flex-col items-center mt-8">
  <div class="flex flex-col items-center space-y-4 p-6 card rounded-xl shadow-lg">
    <p class="text-2xl thick_text text-center">New event:</p>

    <div class="w-full max-w-md">
      <input
        id={id}
        bind:value
        placeholder={placeholder}
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1"
        aria-invalid={error ? "true" : "false"}
        aria-describedby={error ? id + "-err" : undefined}
      />
      {#if error}
        <p id={id + "-err"} class="text-sm text-red-600 mt-1">{error}</p>
      {/if}
    </div>

    <button 
      on:click={makeEventAction}
      class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer"
    >
      Create Event
    </button>
  </div>
</main>