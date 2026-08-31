# Mira MVP: GTM and funnels

Mira is currently marketed exclusively at IG shop operators, people who run their shops on IG. If Mira is successful, it becomes an extension of the capabilities that IG offers this group of people.

This post places Mira within the context of the platforms it runs on and the implications for onboarding new customers.

## Platforms

Our MVP currently has a web-based signup and onboarding wizard. This approach serves users who arrive to Mira from the open web: Google search and other browser-first (contrasted with app-first) venues.

We would like to add an additional route targeted specifically at sellers who originate on IG. This approach represents our observation that Mira lives on existing platforms and beginning to intentionally design for these platforms.

## Current onboarding flow

Our web onboarding currently does the following:

* connects a professional IG account
* starts ingest of page posts and product extraction and storage (in the background)
* collects where to send human in the loop notifications to the operator
* collects shop delivery and payment details
* sets up a test account
* take user into dashboard

Each of these steps represents a potential exit point. According to our hypothesis, the current onboarding flow has another critical risk: a large part of the onboarding takes place off-platform.

## Problems

The main issues with the current onboarding are:

* long, tedious flows have typically poor funnel conversions
* asking prospects to go off-platform is bad for funnel conversions

In short:

* it takes too long for a prospect to make it through the onboarding funnel
* the funnel asks for too much information upfront
* there are two branches present in the funnel, 1 avoidable: connect IG account and send test DM

## Hypotheses

Our central hypothesis is that adopting a [platform-native service approach](https://blog.bymonolith.com/platform-native-risks-opportunities) is better for our short-run goals than requiring new users to run the gauntlet of off-platform onboarding.

The goal of onboarding is singular: presenting Mira in the [right way](https://blog.bymonolith.com/what-is-mira), at the [most opportune moment](https://blog.bymonolith.com/shop-owner-micro-moments), to the [right target](https://blog.bymonolith.com/mira-icp) and driving the flow to enable the target to experience what Mira can do for their shop as quickly as possible. 

This blog post targets the last step in this flow: identifying the hurdles and bottlenecks in the way of user onboarding and eliminating them.

Our hypothesis supports this goal by compressing time to first value, the amount of time it takes a shop operator from encountering Mira on IG or the web to realising first [tangible value](https://blog.bymonolith.com/tangible-value-mira) with Mira.

Things we want to learn during this experiment:

* offering a fully platform-native service experience is superior to the existing split approach as measured by funnel metrics
* removing payment and delivery from onboarding may shorten time to first value
* most Instagram pages may contain enough product, payment and delivery information to reduce seller input to account and handoff input
* progressive configuration may work when owner responses are fast enough
* it is better to show what Mira can do upfront
* it is better to show what Mira can do multiple times throughout the onboarding
* it is better to have a Mira agent that the shop operator can interact with i.e. shop operators prefer operating and configuring their shops through an agent chat in a DM

## Onboarding v2

To test our hypotheses, we are adding a platform-native onboarding flow for IG shop operators. 

The proposed onboarding for platform-native users is shown in the video below:

```html
<iframe
  src="https://drive.google.com/file/d/1VC2ZymeQRDGSSyQgKrhHFYL_J3dVu97E/preview"
  width="100%"
  height="550"
  allow="fullscreen"
></iframe>
```



*Proposed onboarding (**[MIN-245](https://linear.app/deepspacemuse/issue/MIN-245/epic-dm-first-onboarding-set-up-mira-from-instagram)**) walkthrough: It shows the current payment and delivery setup steps; this article proposes moving those steps out of required onboarding.*

### Boarding gates for IG and web

![](assets/9Lb6dThOGeBxA3QOOcHBpCRl1BrSMCiliS99kR2wxPc=.svg)

Instead of one boarding gate as pertains now, we will offer two boarding gates:

* "DM to get started" is the primary onboarding surface for IG-led acquisition
* [Web onboarding](https://app.withmira.co) serves web-led acquisition and sellers who prefer a browser interface

Web targeting uses well known `utm_*` sources for origination attribution. 

Meta supports ads that open Instagram Direct, and its messaging webhook can carry referral and ad context. This allow us to track origination attribution for IG as well.

### Similar onboarding experiences

Although we offer two boarding gates for the different top-of-funnel sources, the onboarding experience is meant to be similar. 

Both gates should offer fast, distraction-free, pain-free, frustration-free, resumable means to get started with Mira.

The new onboarding flows collapses to three main stages:

* connect a professional IG account
* select handoff IG account
* experience Mira

### Early learning

Mira should begin collecting and learning shop content as soon as the seller connects Instagram.

The current application already does this: when an IG account connects, Mira pulls its posts and runs product discovery and storage.

We need to add a second dimension to this content ingestion and learning process such that Mira does two things with shop posts:

![](assets/43LegLdkBiYArEnlZ2gcqhyj9Ww6GgEmve7FYWVI_3E=.svg)

**Product discovery:** decide whether the post contains a product, extract it when present and write through the normal commerce model.

**Payment and delivery discovery:** inspect shop posts for payment details, pickup locations, delivery areas and fees, free-delivery thresholds, timing or courier instructions.

[MIN-246](https://linear.app/deepspacemuse/issue/MIN-246/extract-payment-and-delivery-details-from-instagram-content) addresses this feature.

The new onboarding flow should optimise for time to first value, the gap in time between when a user starts onboarding till they have their first experience of Mira being useful.

In the context of onboarding, value can be shown by:

* showing products that have been discovered
* showing payment details discovered
* showing delivery details discovered
* sharing early shop review and analysis based on comments, post interactions, etc

Every opportunity needs to be taken when present to show value early, clearly and frequently to shop operators to help establish and differentiate brand and product.

### Simplify test account and handoff

Currently, handoff options include:

* IG
* WhatsApp
* Email

Given that Mira targets IG accounts exclusively, we could make gains by:

* eliminating WhatsApp and Email as handoff options
* mandating another IG account as the only handoff option

Then for the IG boarding gate, the originating account becomes the default handoff option.

For the web boarding gate, the handoff account becomes the test account.

### Defer payment and delivery options

The current web wizard collects payment and delivery details before completion.

We propose removing both from the required onboarding sequence for IG and web.

Shop operators can configure payment and delivery details in the web dashboard or by chatting directly with Mira via DM.

The more likely scenario is that a shop operator will not add payment and delivery options unprompted. Mira delays the collection of this information until a customer conversation needs it.

![](assets/SZoqi0h_d4VlyQ8SkTw1w6QoKeH-685eJ8WSKlkTH38=.svg)

This approach has a few advantages:

* it shows Mira can do useful stuff
* shortens onboarding time

How does this work? During a shopper conversation, Mira finds that it needs to share payment or delivery information. It looks in the shop details and finds no such information available.

Mira raises a request with the shop operator:

"John wants to pay KES 5,450 for Khamrah Qahwa and Palmer's Cocoa Butter Lotion 250ml. I can't find any payment info. What details should share with him?"

If Mira found payment or delivery details while processing shop posts, the request to the shop operator can look like:



“John wants to pay KES 5,450 for Khamrah Qahwa and Palmer's Cocoa Butter Lotion 250ml. I found Till 123456 in one of your posts. Is that still the right Till?”

Mira parses the shop operator response and persists the data so that it can use it next time.

Mira then closes the loop with the shopper:

"Please hold on a minute, John, I don't have the payment details. I've asked and will get right back to you. Thanks!"

Since multiple users may request the same information at the same time, care needs to be taken with how this outreach is designed. 

A simple approach may use queues that have the following semantics:

* only 1 consumer
* only 1 message processed at a time
* consumer holds on to message until shop operator response 
* consumer drops all waiting messages on that queue

While it is mandatory to send only 1 such request to a shop operator, it might be beneficial to test whether letting the operator know that multiple such requests are pending would lead to better metrics.

### Test mode

Once onboarding is completed, the shop is placed in test mode, in which it only processes messages from the test account and drops all others.

This is a safe and soft landing for new shops: experience Mira immediately by yourself and turn the firehose on only when you're comfortable.

This behaviour remains.

For shop operators entering via the IG DM boarding gate, the IG account that sets up the shop is the default test account.

Shop operators who use the web boarding gate specify their test account and send the test code to Mira for activation.

## Key event funnel and metrics

The onboarding changes above are intended to shorten the path between a shop operator encountering Mira and experiencing Mira doing something useful for their shop.

The main measure is **time to first value**. We also need to know where prospects leave the onboarding funnel and what proportion make it through each step.

For each funnel step we track:

* **step conversion** — percentage of prospects who complete the next step after reaching the current step
* **step abandonment** — percentage of prospects who reach a step but do not complete the next step
* **step time** — elapsed time between the two events, measured at p50 and p90
* **onboarding conversion** — percentage of onboarding starts that reach test mode
* **successful test conversion** — percentage of onboarding starts that reach a successful test
* **go-live conversion** — percentage of onboarding starts that reach go-live
* **time to test mode** — elapsed time from onboarding start to entering test mode
* **time to successful test** — elapsed time from onboarding start to successful test
* **time to go-live** — elapsed time from onboarding start to go-live

### Time to first value

The time to first value metrics measures the time between when onboarding starts to the time at the first point at which Mira shows the shop operator something useful that Mira has learned from their shop.

This is our money shot moment! This is what the shop operator has run the gauntlet for and needs to be clearly identified and shown off to the user prominently.

Examples include:

* a product discovered from the shop's posts
* payment information found in a post
* delivery information found in a post
* an early observation about the shop based on its content or interactions

**Time to first value** is:

`first_value_shown_at - onboarding_started_at`

We measure p50 and p90 time to first value.

We also measure **first value conversion**:

`shops with first_value_shown / onboarding starts`

This tells us how often Mira manages to show useful shop-specific value during onboarding.

### IG onboarding funnel

The IG funnel starts when a shop operator starts onboarding in the Mira DM.

The key events are:

* `ig_onboarding_started`
* `instagram_connection_started`
* `instagram_connected`
* `instagram_dm_resumed`
* `first_value_shown`
* `test_mode_entered`
* `test_started`
* `successful_test`
* `shop_went_live`
* `first_live_customer_value`

The main funnel measurements are:

* IG onboarding start → IG connection started
* IG connection started → IG connected
* IG connected → Mira DM resumed
* onboarding start → first value shown
* onboarding start → test mode
* test mode → test started
* test started → successful test
* successful test → go-live
* go-live → first live customer value

The OAuth round trip needs its own measurements:

* **OAuth start rate** — IG connection starts / IG onboarding starts
* **OAuth completion rate** — IG connections completed / IG connection starts
* **DM return rate** — Mira DMs resumed / IG connections completed
* **OAuth round-trip time** — elapsed time from `instagram_connection_started` to `instagram_dm_resumed`

### Web onboarding funnel

The web funnel starts when a shop operator starts onboarding on the Mira web product.

The key events are:

* `web_onboarding_started`
* `instagram_connection_started`
* `instagram_connected`
* `handoff_account_selected`
* `test_account_activated`
* `first_value_shown`
* `test_mode_entered`
* `test_started`
* `successful_test`
* `shop_went_live`
* `first_live_customer_value`

The main funnel measurements are:

* web onboarding start → IG connection started
* IG connection started → IG connected
* IG connected → handoff account selected
* handoff account selected → test account activated
* onboarding start → first value shown
* onboarding start → test mode
* test mode → test started
* test started → successful test
* successful test → go-live
* go-live → first live customer value

### Test metrics

`test_started` is triggered by the first message from the authorised test account to Mira while the shop is in test mode.

`successful_test` is the first test conversation in which Mira:

* responds to the test account as if it was a real customer
* uses product information learned from the shop
* progresses through the normal commerce path far enough to create an order

We measure:

* test mode → test started conversion
* test started → successful test conversion
* time from test mode to first test
* time from first test to successful test
* onboarding start → successful test conversion
* onboarding start → successful test time

### Early learning metrics

Mira starts learning as soon as the professional IG account connects.

We measure:

* time from IG connection to first product discovered
* time from IG connection to first value shown
* posts scanned during initial learning
* products discovered
* percentage of connected shops with at least one usable product
* payment information discovery rate
* delivery information discovery rate
* percentage of shops where Mira can show useful learned information before test mode

For payment and delivery discovery:

`discovery rate = shops where information was found / connected shops`

For usable products:

`usable product rate = shops with at least one usable product / connected shops`

### Deferred payment and delivery metrics

When Mira needs payment or delivery information during a shopper conversation, we record:

* whether confirmed information already exists
* whether information was discovered during page learning
* whether Mira asks the shop operator
* shop operator response time
* whether the information is persisted
* whether the shopper conversation resumes
* whether the shopper leaves while waiting
* whether Mira asks for the same information again after it has already been provided

The main measurements are:

* **configuration coverage** — shopper requests where required information already exists / shopper requests requiring that information
* **learning assist rate** — missing configurations where page learning found a useful candidate / missing configurations
* **operator request rate** — requests requiring operator input / requests requiring payment or delivery information
* **operator response time** — elapsed time between Mira asking and the operator responding
* **conversation resume rate** — paused shopper conversations successfully resumed / shopper conversations paused for missing information
* **shopper abandonment while waiting** — shoppers who leave before the information is supplied / shopper conversations paused for missing information
* **repeat request rate** — requests for information that the operator has previously supplied / operator information requests

### Live value

`shop_went_live` records the point at which the shop operator enables Mira for real customer conversations.

We keep the following events separate:

* `first_live_customer_value`
* `first_live_order`
* `first_paid_order`

`first_live_customer_value` is the first useful outcome Mira creates in a real customer conversation after go-live.

`first_live_order` is the first real customer order created after go-live.

`first_paid_order` is the first real customer order that reaches confirmed payment.

We measure:

* go-live → first live customer value
* go-live → first live order
* go-live → first paid order
* onboarding start → first live customer value
* onboarding start → first live order
* onboarding start → first paid order

For paid acquisition, source, campaign, ad and creative attribution should be carried through these events so that we can measure:

* cost per onboarding start
* cost per connected shop
* cost per first value shown
* cost per successful test
* cost per live shop
* cost per first live customer value
* cost per first live order
* cost per first paid order

## Side effects

* Product Engineering 

## References

* [MIN-245 — DM-first onboarding](https://linear.app/deepspacemuse/issue/MIN-245/epic-dm-first-onboarding-set-up-mira-from-instagram)
* [MIN-246 — Extract payment and delivery details from Instagram content](https://linear.app/deepspacemuse/issue/MIN-246/extract-payment-and-delivery-details-from-instagram-content)
* [Meta — Ads that click to message](https://www.facebook.com/business/ads/click-to-message-ads)
* [Meta Instagram API — Messaging webhook](https://www.postman.com/meta/instagram/request/23987686-95cce6f6-b811-41dc-b560-d43741c5002a)
* [Meta Instagram API — Quick replies](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api?entity=request-23987686-af579d08-121e-4897-8f45-5fd41ace49df)
