# AutoShopper-AI

AutoShopper AI

AutoShopper AI is an autonomous shopping assistant that converts natural-language requests into real online actions.
Given a user prompt (e.g., “Find me an iced matcha with oat milk under $12 near 45 Fremont St”), the system:

Interprets the request

Navigates the web using an LLM-guided browser agent

Searches nearby cafés and delivery platforms

Evaluates options based on constraints (price, distance, rating)

Builds the cart and prepares checkout

Returns a structured summary and actionable checkout link

The goal is to demonstrate a practical, fully autonomous web-navigation agent capable of completing real-world tasks end-to-end.

Features
Autonomous Browser Agent

Uses Browser-Use (LLM-guided automation) to search, click, extract data, and follow links.

Interacts with Google Maps, DoorDash, UberEats, or direct ordering sites.

End-to-End Task Execution

Understands user intent

Locates nearby vendors

Selects the best option based on constraints

Builds the order up to final checkout (without submitting payment)

Structured JSON Output

The backend returns a predictable JSON response containing:

Restaurant name

Item selected

Total price

Estimated delivery time

Checkout link

Any relevant metadata

This makes the results easy to use in front-end applications or external integrations.

Modern Frontend Interface

Responsive layout

Animated UI with 3D background elements

Timeline to visualize the agent’s progress

Clear result display with checkout link

API-Driven Architecture

Frontend communicates with a lightweight REST API

All computation and browser automation occurs on the backend

Tech Stack
Frontend

HTML, CSS, JavaScript

Three.js for 3D visuals

Responsive layout with glassmorphism style

Backend

Python 3.10

FastAPI

Playwright (Chromium automation)

Browser-Use agent (LLM-powered control)

Optional Integrations

Sentry for monitoring

Environment-based configuration via .env
