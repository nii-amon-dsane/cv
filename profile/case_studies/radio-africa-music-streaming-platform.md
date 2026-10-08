# Radio Africa Music Streaming Platform — Production Architecture Case Study

**Company:** Radio Africa Group  
**Role:** Group Head of Development  
**Period:** Jun 2016 – Oct 2018  
**Location:** Nairobi, Kenya  
**Status:** Canonical career evidence. Reuse for application, interview and profile material.

## Why this system was complex

Radio Africa was building a music-streaming platform while moving from traditional media towards digital products. The system had to ingest, normalize, secure, publish and account for catalogues from multiple rights and content providers.

Providers included Universal Music Group, Sony, Africori, MCSK and a number of smaller providers.

There was no common provider contract for catalogue delivery:

- providers supplied assets in different formats and at different quality levels;
- transport and availability mechanisms differed by provider;
- metadata and media completeness varied;
- some catalogues included album artwork while others did not;
- the product required artwork for every song even when the provider did not supply it.

The ingestion layer therefore had to do more than move files. It needed a strong intake and normalization boundary covering missing-asset detection, quality control and backfilling. Missing artwork and other assets could require a combination of web search and manual asset provision before a catalogue item was publishable.

## Greenfield architecture

There was no single ingestion product that could be integrated to solve the problem end to end. Music streaming and the surrounding tooling were still relatively immature, and few open-source components covered all of the capabilities required.

The team therefore had to architect the platform from first principles using a combination of open-source software, commercial products and custom-built components. Several capabilities had to be built de novo.

The difficult engineering work was not only building individual services. It was repeatedly resolving integration problems between independently developed pieces of software with different assumptions, interfaces and operational characteristics.

Technologies used across the platform included Java, later Kotlin, Akka, RabbitMQ / AMQP, Python, FFmpeg, AWS Lambda, microservices and serverless infrastructure. Billing and payments were integrated with Safaricom services and mobile money.

## Security, commercial and reporting requirements

The architecture also had to satisfy requirements that affected the design from the start rather than being added later.

### Content protection

Music had to be delivered with DRM and access controls so that having media files present on a user's local device did not allow playback outside an active entitlement or subscription.

### Playback attribution and rights reporting

Playback had to be attributable and reliably accounted for. This was required so usage could be reported and artists / rights holders could be compensated for their contribution to playback.

### Partner service levels

Once a provider supplied a catalogue, Radio Africa had partner expectations around how quickly the catalogue would be processed and made available on the platform.

Ingestion capacity therefore had to be elastic. The system needed to process ordinary catalogue flow economically while scaling up for large catalogue deliveries without requiring permanently provisioned infrastructure sized for peak demand.

## What broke in the first production design

The first major stress test came with large catalogue dumps from Sony.

The original ingestion design was effectively a single mainline pipeline. A media item was picked up and all required quality renditions were generated within that same processing path.

This created several problems:

- a large catalogue burst could overwhelm the available processing capacity;
- FFmpeg processing was memory intensive and could fail when configuration or workload caused memory pressure / OOM conditions;
- failure late in the pipeline meant the entire media item could need to be processed again;
- already completed renditions were repeated unnecessarily;
- the architecture coupled otherwise independent stages of work;
- fixed infrastructure made peak capacity expensive even when that capacity was not needed.

The Sony catalogue exposed that the prototype architecture could process normal flows but did not have the failure isolation, elasticity or recoverability required for large production catalogue ingestion.

## The redesign

### Asynchronous processing

The ingestion system was redesigned around asynchronous processing using Kotlin, Akka and RabbitMQ.

Instead of running all work as one synchronous mainline pipeline, processing stages became independently queued work. This allowed processing capacity to be configured and scaled without coupling ingestion directly to every downstream task.

### Mainline task with fan-out

Each catalogue item had one mainline ingestion task that could fan out into separate jobs for the required quality renditions.

This decomposed the work so that one failed rendition did not invalidate every successful rendition.

### Idempotent recovery

Processing was made idempotent at the rendition/task level.

If a run failed partway through — commonly because an FFmpeg process exhausted memory — the same item could be retried without regenerating quality levels that had already completed successfully.

This changed recovery from "repeat the whole pipeline" to "continue/retry only incomplete work."

### Elastic serverless capacity

The processing architecture was moved away from reserved AWS instances towards AWS Lambda for suitable workloads.

Instead of maintaining large standing servers to handle catalogue peaks, processing capacity could scale up by spawning functions as catalogue demand increased and scale back down after the work completed.

This materially reduced the cost of idle capacity while providing the elasticity needed for subsequent large catalogues, including Universal Music Group.

### Polyglot service decomposition

Message queues also made it easier to separate components by responsibility and use the appropriate implementation language.

Python could be used for parts of the pipeline that were better served by its ecosystem, while Java and later Kotlin were used for core business processes.

The queue boundary reduced the need for every subsystem to share one runtime or execution model.

## Team and organisational work

The technical redesign also exceeded the experience level of parts of the existing young team.

As Group Head of Development, the work therefore included organisational scaling and an explicit upskilling programme alongside the platform redesign.

Training sessions covered topics including:

- dependency injection;
- background and asynchronous processing;
- scalability;
- idempotency;
- distributed processing and failure recovery.

The objective was not only to deliver the architecture but to build enough engineering capability inside the team to operate and extend it.

## Result

The redesign produced an ingestion architecture with:

- normalization across heterogeneous provider catalogues;
- explicit handling of missing and low-quality assets;
- DRM-aware processing and access requirements;
- playback attribution and reporting for commercial / rights obligations;
- asynchronous, independently retryable processing;
- idempotent rendition generation;
- configurable processing capacity;
- elastic serverless execution for burst workloads;
- lower standing infrastructure cost;
- stronger failure isolation;
- a team better equipped to operate distributed production systems.

## Reusable interview angles

### Most complex system taken from prototype to production
Use the full story: fragmented provider inputs → greenfield architecture → Sony catalogue failure → asynchronous/idempotent/serverless redesign.

### Production incident / system that broke
Lead with the first large Sony catalogue dump overwhelming the single mainline ingestion design and FFmpeg/OOM failures forcing expensive reruns.

### Scaling architecture
Lead with partner catalogue SLAs, bursty workloads, RabbitMQ fan-out, configurable processing capacity and the move from reserved instances to Lambda.

### Reliability / idempotency
Lead with independent quality-rendition jobs and retrying only incomplete work after FFmpeg failures.

### Cost optimization
Lead with removing large standing processing servers and scaling Lambda capacity with catalogue demand.

### Technical leadership
Lead with simultaneously rearchitecting the platform and upskilling a young team in dependency injection, background processing, scalability and idempotency.

### Integration complexity
Lead with Universal, Sony, Africori, MCSK and smaller providers delivering different formats, qualities, assets and transport mechanisms, plus the absence of a single end-to-end ingestion product.

## Source

User-confirmed detail supplied on 2026-10-08. Treat these facts as authoritative career evidence unless superseded by a later user correction.
