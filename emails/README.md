# Systems Health Check emails

All of these are sent by **one GHL workflow**, triggered when someone clicks
"Email me my results" on the Health Check page.

| File | Track | When | Subject |
|---|---|---|---|
| `health-check-results.html` | Both | Immediately | Your Systems Health Check: {{inboundWebhookRequest.score}}/100 |
| `sequence/ignite-1-pressure-point.html` | Ignite & Build | Day 2 | The one I'd fix first, {{contact.first_name}} |
| `sequence/ignite-2-client-story.html` | Ignite & Build | Day 4 | From not bookable to fully booked |
| `sequence/ignite-3-how-ignite-works.html` | Ignite & Build | Day 7 | How Ignite works |
| `sequence/ignite-4-last-nudge.html` | Ignite & Build | Day 10 | Quick question |
| `sequence/inferno-1-pressure-point.html` | Inferno | Day 2 | The one I'd look at first, {{contact.first_name}} |
| `sequence/inferno-2-client-story.html` | Inferno | Day 4 | Tens of thousands a month, and no idea what was working |
| `sequence/inferno-3-how-the-audit-works.html` | Inferno | Day 7 | How an Inferno Audit works |
| `sequence/inferno-4-last-nudge.html` | Inferno | Day 10 | Quick question |

Preview text for each is in the comment at the top of its file. Prices only appear in
the Ignite & Build emails.

## Workflow

1. **Trigger:** Inbound Webhook. Paste its URL into `LEAD_WEBHOOK_URL` in
   `Ember-HealthCheck-GHL.html`, then submit one test result so GHL learns the fields.
2. **Create/Update Contact:** first name `{{inboundWebhookRequest.first_name}}`,
   email `{{inboundWebhookRequest.email}}`.
3. **Add Tag:** `health-check`.
4. **Send Email:** `health-check-results.html`.
5. **If/Else** on `{{inboundWebhookRequest.track}}`:
   - is `Ignite & Build` → tag `hc-ignite`, then: Wait 2 days → ignite-1 → Wait 2 days →
     ignite-2 → Wait 3 days → ignite-3 → Wait 3 days → ignite-4
   - otherwise → tag `hc-inferno`, then the same waits with the inferno-1 to 4 emails
6. **Goal / exit:** add a Goal event "Appointment booked" on the Disco Call calendar, so anyone
   who books a call drops out of the sequence straight away.
7. Optional: If/Else on `{{inboundWebhookRequest.newsletter_opt_in}}` is `yes` → tag `newsletter`.

Publish the workflow, then run a test with your own email for each track.

## Notes

- The Day 2 emails reuse the person's top pressure point from the webhook
  (`pressure_1_area`, `pressure_1_title`, `pressure_1_body`). If those come through blank
  after the Wait steps, save them to contact custom fields in step 2 and swap the merge
  tags to `{{contact.<field>}}`.
- `ignite-2-client-story.html` names Debs, Heather and Mike. Check the details and that
  they're happy to be named before it goes live.
