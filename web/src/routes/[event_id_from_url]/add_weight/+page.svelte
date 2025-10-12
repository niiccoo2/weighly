<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import '$lib/styles_lightmode.css';
  export let params;

  const eventId = parseInt(params.event_id_from_url);

  let apikey = "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz";

  let total: number | null = null;
  let save_success = "";

  async function saveWeight(name: string, weight: number , type: string | null) {
    console.log("Sending POST request to save weight");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/add_weight", {
      method: "POST",
      headers: {
        apikey: apikey,
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

  async function getAllowedEvents(): Promise<number[]> {
    console.log("Fetching allowed events");
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return [];

    const res = await fetch(
      "https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_allowed_events",
      {
        method: "POST",
        headers: {
          apikey: apikey,
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_id: session.user.id })
      }
    );

    if (!res.ok) {
      console.error("Failed to fetch allowed events:", await res.json());
      return [];
    }

    const events = await res.json();
    console.log("Fetched events:", events);

    // return an array of event IDs
    return events.map((e: any) => e.event_id);
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

    // Check if the user is allowed to save to this event
    const allowedEventIds = await getAllowedEvents();
    if (!allowedEventIds.includes(eventId)) {
      weight_error = "You are not allowed to add weights to this event.";
      return;
    }

    await saveWeight(name_value.trim(), weight_value, null);

    if (total) {
      console.log(`Weight saved successfully to ${eventId}`);
      // Reset form
      name_value = "";
      weight_value = null;
      weight_input = "";
      name_error = "";
      weight_error = "";

      save_success = "Saved successfully!";

      setTimeout(() => {
        save_success = "";
      }, 3000);
    } else {
      weight_error = "Failed to create event. Please try again.";
    }
  }


  export let name_value: string = "";
  export let name_id = "name_input";
  export let name_error = "";

  export let weight_input: string = "";
  export let weight_value: number | null = null;
  export let weight_id = "weight_input";
  export let weight_error = "";
</script>

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
      {#if save_success}
        <p class="text-green-600 mt-2">{save_success}</p>
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