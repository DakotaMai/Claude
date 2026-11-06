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
| Spark audit scores | Single Line | Spark audit |
| Spark start with | Single Line | Spark audit |
| Spark readiness | Single Line | Spark audit |
| Spark recommendation | Single Line | Spark audit |
| Spark plan status | Single Line | Spark audit |
| Spark one thing | Multi Line | Spark audit |

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

1. **Create a page** in GHL (for example `victorialewis.co.uk/spark-audit`) and paste `Ember-SparkAudit-GHL.html` into a Custom HTML/Code element.
2. **New workflow**, trigger **Inbound Webhook**. Copy the full URL with the copy icon and paste it into `LEAD_WEBHOOK_URL` near the top of the page script.
3. Submit the audit once yourself, then **Fetch Sample Requests**, pick it in **Mapping Reference** and save the trigger.
4. **Create/Update Contact**: first name `{{inboundWebhookRequest.first_name}}`, email `{{inboundWebhookRequest.email}}`, source `Spark Setup Audit`.
5. **Update Contact Field**:

| Field | Value |
| --- | --- |
| Spark audit answers | `{{inboundWebhookRequest.answers_summary}}` |
| Spark audit scores | `{{inboundWebhookRequest.scores}}` |
| Spark start with | `{{inboundWebhookRequest.start_with}}` |
| Spark readiness | `{{inboundWebhookRequest.readiness}} ({{inboundWebhookRequest.readiness_label}})` |
| Spark recommendation | `{{inboundWebhookRequest.recommendation}}` |
| Spark plan status | `{{inboundWebhookRequest.spark_status}}` |
| Spark one thing | `{{inboundWebhookRequest.one_thing}}` |

6. **Add Tag**: `spark-audit`.
7. **If/Else** on `{{inboundWebhookRequest.spark_status}}` **contains** `joined` (they're already a member):
    - **Yes:** add the tag `spark-load-snapshots` and **Send Internal Notification** to whoever loads accounts (you or your community manager), with their setup order and answers summary, so the right snapshots go in.
    - Then a second **If/Else** on `spark_status` **contains** `annual`: **Yes:** add the tag `spark-setup-plan` and send yourself an internal notification, so you can write their personal setup plan. The Ember Client Hub can draft it from their answers.
8. **Send Email** to the contact with their scores and setup order (ask me for the email template).
9. If `newsletter_opt_in` is `yes`, add your newsletter tag.

## Other fields the Spark audit sends

`quiz`, `team_size`, `score_back_office`, `score_signpost`, `score_shopfront`, `setup_order`, `first_steps`, `preference`, `tried`, `booking_link`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
