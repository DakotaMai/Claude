# Saving quiz answers in GHL

Both quizzes now send a full summary of every answer, plus their results, to a GHL inbound webhook. Follow these steps so the answers are saved on the contact. The Ember Client Hub can then import them with its **Find in GHL** button.

## 1. Create the custom fields

Go to **Settings → Custom Fields**, click **Add Field**, choose the type below and put them all in a new folder called **Quizzes**.

| Field name | Type | Filled by |
| --- | --- | --- |
| Health Check answers | Multi Line | Health Check |
| Health Check score | Number | Health Check |
| Health Check track | Single Line | Health Check |
| Health Check pressure points | Single Line | Health Check |
| Spark audit answers | Multi Line | Spark audit |
| Spark audit scores | Multi Line | Spark audit |
| Spark top three | Single Line | Spark audit |
| Spark roadmap | Multi Line | Spark audit |
| Spark plan | Single Line | Spark audit |
| Spark admin hours | Single Line | Spark audit |
| Spark priorities | Single Line | Spark audit |
| Spark one thing | Multi Line | Spark audit |
| Spark tried already | Multi Line | Spark audit |

## 2. Health Check workflow (already live)

Open your Health Check workflow. After the **Create/Update Contact** step, add an **Update Contact Field** action with these values:

| Field | Value |
| --- | --- |
| Health Check answers | `{{inboundWebhookRequest.answers_summary}}` |
| Health Check score | `{{inboundWebhookRequest.score}}` |
| Health Check track | `{{inboundWebhookRequest.track}}` |
| Health Check pressure points | `{{inboundWebhookRequest.pressure_1_area}}, {{inboundWebhookRequest.pressure_2_area}}` |

Paste the updated Health Check code into the page first, then use **Fetch Sample Requests** on the trigger after one test run, so `answers_summary` shows up in the list.

## 3. Spark audit workflow (new)

The Spark Setup Audit is for members. Send it from your welcome email with their details in the link, so their answers land on the right contact:

- Monthly: `https://victorialewis.co.uk/spark-audit?email={{contact.email}}&contact_id={{contact.id}}&first_name={{contact.first_name}}&plan=monthly`
- Spark Plus (annual): the same link ending `&plan=annual`
- Filling it in together on a call: add `&mode=call`, so the roadmap comes to you instead of them.

If someone opens the page without those details, it asks for their name and email on the results page before sending anything.

1. **Create a page** (for example `/spark-audit`) and paste `Ember-SparkAudit-GHL.html` into a full-width Custom Code element. Fill in `UPGRADE_URL` (Spark Plus checkout) and `VIDEOS_URL` (course page) at the top of the script.
2. **New workflow**, trigger **Inbound Webhook**. Copy the full URL with the copy icon and paste it into `WEBHOOK_URL`.
3. Complete the audit once yourself using a link with your own email, then **Fetch Sample Requests**, pick it in **Mapping Reference** and save the trigger.
4. **Create/Update Contact**: email `{{inboundWebhookRequest.email}}`, first name `{{inboundWebhookRequest.first_name}}`.
5. **Update Contact Field**:

| Field | Value |
| --- | --- |
| Spark audit answers | `{{inboundWebhookRequest.answers_summary}}` |
| Spark audit scores | `{{inboundWebhookRequest.scores_text}}` |
| Spark top three | `{{inboundWebhookRequest.top_three}}` |
| Spark roadmap | `{{inboundWebhookRequest.roadmap}}` |
| Spark plan | `{{inboundWebhookRequest.plan_name}}` |
| Spark admin hours | `{{inboundWebhookRequest.admin_hours}}` |
| Spark priorities | `{{inboundWebhookRequest.priorities}}` |
| Spark one thing | `{{inboundWebhookRequest.most_want_sorted}}` |
| Spark tried already | `{{inboundWebhookRequest.tried_already}}` |

6. **Add Tags**: `spark-audit` and `spark-load-snapshots`, then **Send Internal Notification** to whoever loads accounts (you or your community manager) with their top three and roadmap, so the right snapshots go in.
7. **If/Else** on `{{inboundWebhookRequest.plan}}` **is** `annual`: add the tag `spark-setup-plan` and send yourself an internal notification, so you can write their personal setup plan. The Ember Client Hub can draft it from their answers.
8. **If/Else** on `{{inboundWebhookRequest.send_results_to}}` **is** `client`: **Send Email** with their roadmap (ask me for the template). If it's `viki`, it was a call, so the notification to you is enough.

## Other fields the Spark audit sends

`quiz`, `contact_id`, `mode`, `score_lm`, `score_nur`, `score_enq`, `score_book`, `score_fol`, `score_pipe`, `score_prop`, `score_onb`, `score_inv`, `score_upd`, `score_rev`, `score_past` (each out of 100), plus `scores` and `answers` as nested data for anything that reads JSON.
