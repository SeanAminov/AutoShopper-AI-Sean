# AutoShopper AI

AutoShopper AI is an autonomous shopping assistant that converts natural-language requests into real online actions.  
Given a user prompt (e.g., *“Find me an iced matcha with oat milk under $12 near 45 Fremont St”*), the system:

- Interprets the request  
- Navigates the web using an LLM-guided browser agent  
- Searches nearby cafés and delivery platforms  
- Evaluates options based on constraints such as price, distance, and rating  
- Builds the cart and prepares checkout  
- Returns a structured summary and an actionable checkout link  

The project demonstrates a practical, end-to-end autonomous web-navigation agent capable of completing real-world tasks.

---

## Features

### Autonomous Browser Agent
- Uses **Browser-Use** for LLM-guided automation  
- Interacts with Google Maps, DoorDash, UberEats, and vendor sites  

### End-to-End Task Execution
- Understands intent  
- Locates nearby vendors  
- Applies constraints  
- Builds order up to checkout (without submitting payment)

### Structured JSON Output
The backend returns predictable JSON containing:

- Restaurant name  
- Selected item  
- Total price  
- Estimated delivery time  
- Checkout link  
- Additional metadata  

### Modern Frontend Interface
- Fully responsive  
- Animated UI  
- 3D visuals using Three.js  
- Timeline showing agent progress  
- Clear result card with checkout link  

### API-Driven Architecture
- Frontend communicates with a lightweight REST API  
- Browser automation and decision logic run in the backend  

---

## Tech Stack

### Frontend
- HTML, CSS, JavaScript  
- Three.js  
- Glassmorphism & responsive design  

### Backend
- Python 3.10  
- FastAPI  
- Playwright (Chromium)  
- Browser-Use agent  

### Optional Integrations
- Sentry  
- `.env` configuration  
