# System Design Ep-01 (URL Shortener)  
by - https://neetcode.io/  
reference - https://www.youtube.com/watch?v=qSJAvd5Mgio

---

## Problem Statement  
Design a URL Shortener like bit.ly;

---

## Process  
1. Gather Requirements  
2. API/DB Design  
3. High level design  
4. Deep dive  

---

## Functional Requirements  
1. URL Shortening - Get a unique short URL  
2. URL Redirection (must be quick and minimal latency)  
3. Link analytics (track the number of times each short URL is accessed - used for caching, can skip if you're a beginner)  

---

## Non-Functional Requirements  
1. Minimize redirect latency (related to #2 in functional requirements)  
2. Support 100 million+ daily active users  
3. Handle 1 billion read requests per day (~10k req/sec)  
4. Support 1-5 billion total lifetime URLs  

---

## API Design

- **POST /api/urls/shorten**  
  - Request: Long URL  
  - Result: Short URL  

- **GET /api/urls/{shortURL}**  
  - Request: No request body (shortURL passed as URL param)  
  - Result: Redirect 301 (with caching), 302 (no caching)  

---

## High Level Design  

We will store the data persistently on disk (DB server separate from URL service) to keep it loosely coupled  
<img width="873" height="282" alt="image" src="https://github.com/user-attachments/assets/633843ab-4cc6-4a53-bb73-bbd092b7b023" />

                                         
### Scalability Considerations  

Add an **API Gateway** for routing, which will also ease client-side interaction as system grows and more services are added:  
<img width="1026" height="448" alt="image" src="https://github.com/user-attachments/assets/2af58d2f-1ab3-45f4-a339-25c0d9a7831c" />


- Bit.ly uses **301 redirects** for permanent redirection (with caching, but minimal analytics)  

---

## URL Shortening Logic  

- Allowed characters for short URL: a-z, A-Z, 0-9 (Base62)  
- Assume length = 6 → 62^6 = 57 billion possible URLs  
- Length = 7 → 62^7 ≈ 3.5 trillion (very less collision chance)  

---

## DB Schema (Example):

| Field       | Type       | Description                      |
| ----------- | ---------- | ---------------------------------|
| shortUrl    | String     | The unique short URL string      |
| longUrl     | String     | The original long URL            |
| uid         | String     | Unique identifier (optional)     |
| createdAt   | Date       | Timestamp of creation            |
| usedCount   | Integer    | Number of times accessed         |

- Assume each row ~1KB; for 1B URLs, storage ~1TB  

---

## Key Design Considerations  

### Unique URL Generation Approaches:  

- Use random strings of fixed size (6 or 7 chars)  
  - Chance of collisions is low but possible  
  - To reduce collisions, increase length  
- Use hashing (MD5, SHA) with collision resolution  
- Generate sequential IDs and encode in Base62 (simple and collision-free)  

---

### Performance and Scaling  

- Use **Redis** as an in-memory cache for frequently accessed URLs to reduce DB load and latency  
- Redis is single-threaded but very fast, suitable for caching  
- Use **read replicas** on the DB to increase read throughput  
- Sharding can be applied when system scales beyond a certain threshold but adds complexity  

---

## Updated High-Level Design with Cache  

<img width="1222" height="691" alt="image" src="https://github.com/user-attachments/assets/d637a46f-267a-4d14-849d-b1ae09f1e0e3" />

---

## Analytics Architecture  

<img width="1305" height="570" alt="image" src="https://github.com/user-attachments/assets/e8648dd9-2813-4757-bdee-5d7b73298def" />

- Analytics service keeps counts in-memory (for performance)  
- Periodically (e.g., every 60 seconds) flushes count data to persistent DB (using a cron job or scheduling library) to prevent high memory usage  

---

# Summary  

- Functional and non-functional requirements defined for scale and performance  
- API endpoints for shortening and redirecting URLs  
- Base62 encoding with length 6 or 7 for short URLs ensures large space and low collision  
- Use cache (Redis) for minimizing latency on redirection  
- DB design supports 1B+ URLs with ~1TB size estimate  
- Analytics handled via in-memory counting with periodic flush to DB  
- API Gateway used to route traffic to specialized services, improves scalability and modularity  

---
