<script lang="ts">
  import { onMount } from 'svelte';
  import '$lib/styles_lightmode.css';
  import { supabase } from '$lib/supabaseClient';
  export let data: { eventId: number };
  const { eventId } = data;

  async function addUserToEvent(event_id: string, email: string) {
    console.log("Sending POST request for new event");
    const { data: { session } } = await supabase.auth.getSession();
    let response;
    if (!session) return;

    const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/add_user_to_event", {
      method: "POST",
      headers: {
        apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ p_event_id: event_id, p_user_email: email })
    });

    response = await res.json();

    if (response != 0) {
      email_error = "Error adding user to event";

      console.log(`Error adding ${email} to event ${event_id}. Response:`, response);
      return;
    } else {
      save_success = "Saved successfully!";

      console.log(`Added ${email} to event ${event_id}. Response:`, response);

      setTimeout(() => {
        save_success = "";
      }, 3000);
    }}

    async function fetchEventUsers(event_id: string) {
      console.log("Fetching event users");
      const { data: { session } } = await supabase.auth.getSession();
      let response: any = [];
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/get_event_users", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id })
      });

      response = await res.json();

      if (response.error) {
        console.log(`Error fetching users for event ${event_id}. Response:`, response);
        return;
      } else {
        console.log(`Fetched users for event ${event_id}. Response:`, response);
        return response;
      }
    }

    async function removeUserFromEvent(event_id: string, email: string) {
      console.log("Sending POST request to remove user from event");
      const { data: { session } } = await supabase.auth.getSession();
      let response;
      if (!session) return;

      const res = await fetch("https://oifjrkxhjrtwlrancdho.supabase.co/rest/v1/rpc/remove_user_from_event", {
        method: "POST",
        headers: {
          apikey: "sb_publishable_DruCqbBOsfUmleFtZkKtxw_dTjPQwfz",
          Authorization: `Bearer ${session.access_token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ p_event_id: event_id, p_user_email: email })
      });

      response = await res.json();

      if (response != 0) {
        email_error = "Error removing user from event";

        console.log(`Error removing ${email} from event ${event_id}. Response:`, response);
        return;
      } else {
        save_success = "Removed successfully!";

        console.log(`Removed ${email} from event ${event_id}. Response:`, response);

        setTimeout(() => {
          save_success = "";
        }, 3000);
      }}
  
  let event_users: any[] = [];
  let loading_users = true;
  
  onMount(async () => {
    event_users = await fetchEventUsers(String(eventId));
    loading_users = false;
  });
  
  export let save_success = '';
  export let email_id = 'email';
  export let email_value = '';
  export let email_error = '';

</script>

<svelte:head>
	<title>Weighly</title>
</svelte:head>

<main class="flex flex-col items-center mt-8 w-full max-w-4xl mx-auto">
  <!-- Users -->
  <div class="w-full max-w-md p-4 card rounded-xl shadow-lg">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Users</p>
      <p class="text-center text-sm">Allow other users to add weights and administrate the event. Click on a user to remove them from the event.</p>

      {#if loading_users}
        <p>Loading users…</p>
      {:else if !event_users || event_users.length === 0}
        <p>No users added yet</p>
      {:else}
        <div class="w-full mt-2 space-y-1">
          {#each event_users as email}
            <button 
              on:click={() => { removeUserFromEvent(String(eventId), email); event_users = event_users.filter(e => e !== email); }}
              class="text-lg font-semibold text-center hover:underline w-full block cursor-pointer">
              {email}
            </button> 
          {/each}
        </div>
      {/if}


      <input
        id={email_id}
        bind:value={email_value}
        placeholder="Email"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1 mt-4"
        aria-invalid={email_error ? "true" : "false"}
        aria-describedby={email_error ? email_id + "-err" : undefined}
      />
      {#if email_error}
        <p id={email_id + "-err"} class="text-sm text-red-600 mt-1">{email_error}</p>
      {/if}
      {#if save_success}
        <p class="text-green-600 mt-2">{save_success}</p>
      {/if}

      <button 
      on:click={() => addUserToEvent(String(eventId), email_value)}
      class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer w-full mt-4 text-2xl">
      Add User
      </button>
    </div>
  </div>

  <!-- Custom URL -->
   <div class="w-full max-w-md p-4 card rounded-xl shadow-lg mt-8">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Custom URL</p>
      <p class="text-center text-sm">Set a custom slug for your event.</p>

      <p class="text-lg font-semibold text-center hover:underline w-full block cursor-pointer mt-2">test</p>


      <input
        id={email_id}
        bind:value={email_value}
        placeholder="Email"
        class="w-full rounded textbox focus:outline-none text-2xl thick_text px-2 py-1 mt-4"
        aria-invalid={email_error ? "true" : "false"}
        aria-describedby={email_error ? email_id + "-err" : undefined}
      />
      {#if email_error}
        <p id={email_id + "-err"} class="text-sm text-red-600 mt-1">{email_error}</p>
      {/if}
      {#if save_success}
        <p class="text-green-600 mt-2">{save_success}</p>
      {/if}

      <button 
      on:click={() => addUserToEvent(String(eventId), email_value)}
      class="accent_color_button rounded hover:scale-105 px-4 py-2 transition-transform cursor-pointer w-full mt-4 text-2xl">
      Add User
      </button>
    </div>
  </div>

  <!-- Save Weights Link -->
  <div class="w-full max-w-md p-4 card rounded-xl shadow-lg mt-8">
    <div class="flex flex-col items-center space-y-1">
      <p class="text-2xl font-semibold text-center">Save Weights</p>
      <p class="text-center text-sm">Go here to add weights to your event.</p>
      <a
        href="/{eventId}/add_weight"
        class="w-full max-w-md flex text-2xl items-center justify-center accent_color_button rounded hover:scale-105 px-4 py-2 leading-normal transition-transform block mt-4">
        Save Weights
      </a>
    </div>
  </div>
</main>