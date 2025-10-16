import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
  return { eventId: Number(params.event_id_from_url) };
};