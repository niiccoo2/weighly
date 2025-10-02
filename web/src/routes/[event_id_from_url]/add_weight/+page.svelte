<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import Header from '$lib/Header.svelte';
  import '$lib/styles_lightmode.css';
  export let params;

  const eventId = parseInt(params.event_id_from_url);


  let total: number | null = null;

  async function saveWeight(name: string, weight: number , type: string | null) {
    console.log("Sending POST request to save weight");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/add_weight", {
      method: "POST",
      headers: {
        apikey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pZmpya3hoanJ0d2xyYW5jZGhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNjQ4NDUsImV4cCI6MjA3NDY0MDg0NX0.dBUGNaqc6-hcYQzEEUKnwD9gPji6RxqHfRhDeUA6hto",
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ p_event_id: eventId,
                             p_name: name,
                             p_weight: Number(weight),
                             p_type: type
       })
    });

    total = await res.json();
    console.log("Fetched total:", total);
    }
  
  function handleInput(event: Event) {
    const input = event.target as HTMLInputElement;
    
    // Keep only digits and first dot
    let value = input.value.replace(/[^0-9.]/g, "").replace(/\.(?=.*\.)/g, "");
    weight_input = value; // update input string

    // Convert to number or null
    weight_value = value === "" || value === "." ? null : Number(value);

    // Validate
    weight_error = weight_value === null || isNaN(weight_value) ? "Invalid number" : "";
  }



  async function saveWeightAction() {
    if (!name_value.trim()) {
      name_error = "Event name cannot be empty.";
      return;
    }
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) {
      weight_error = "You must be logged in to save weights.";
      return;
    }
    if (weight_value === null || isNaN(weight_value)) {
      weight_error = "Weight must be a valid number.";
      return;
    }
    await saveWeight(name_value.trim(), weight_value, null);
    if (total) {
      console.log(`Weight saved successfully to ${eventId}`);
    } else {
      weight_error = "Failed to create event. Please try again.";
    }
    name_value = "";
    weight_value = null;
    name_error = "";
    weight_error = "";
  }

  export let name_value: string = "";
  export let name_id = "name_input";
  export let name_error = "";

  export let weight_input: string = "";
  export let weight_value: number | null = null;
  export let weight_id = "weight_input";
  export let weight_error = "";
</script>

<Header />

<svelte:head>
	<title>Add Weight</title>
</svelte:head>

<main class="flex flex-col items-center mt-8">
  <div class="flex flex-col items-center space-y-4 p-6 card rounded-xl shadow-lg">
    <p class="text-2xl thick_text text-center">Add Weight:</p>

    <!-- Name Input -->
    <div class="w-full max-w-md">
      <input
        id={name_id}
        bind:value={name_value}
        placeholder="Name"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1"
        aria-invalid={name_error ? "true" : "false"}
        aria-describedby={name_error ? name_id + "-err" : undefined}
      />
      {#if name_error}
        <p id={name_id + "-err"} class="text-sm text-red-600 mt-1">{name_error}</p>
      {/if}
    </div>

    <!-- Weight Input -->
    <div class="w-full max-w-md">
      <input
        id={weight_id}
        bind:value={weight_input}
        on:input={handleInput}
        placeholder="Weight"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1"
        aria-invalid={weight_error ? "true" : "false"}
        aria-describedby={weight_error ? weight_id + "-err" : undefined}
      />
      {#if weight_error}
        <p id={weight_id + "-err"} class="text-sm text-red-600 mt-1">{weight_error}</p>
      {/if}
    </div>

    <!-- Save Button -->
    <button 
      on:click={saveWeightAction}
      class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer"
    >
      Save Weight
    </button>
  </div>
</main>