# 🍽️ Foodie Tour Generator

Welcome to the **Foodie Tour Generator** – an AI-powered project that crafts fun and flavourful one-day food adventure plans based on **location**, **real-time weather**, **iconic dishes**, and **top-rated restaurants**!

---

## 📝 Project Description

This system uses weather data and local culinary knowledge to create a personalized, full-day food tour (breakfast, lunch, dinner) for any city. The generated stories feel like something out of a travel magazine – detailed, vivid, and tailored to the day’s weather.

---

## 🔧 Features

- ☁️ Fetches real-time weather using **OpenWeatherMap API**
- 🍛 Finds **3 iconic local dishes** using Brave search
- 🍽️ Recommends **top restaurants** for those dishes
- ✍️ Generates a delightful foodie story with mood and weather vibes
- 🧭 Adds hidden gem suggestions and travel vibes

---

## 💡 Use-Case

Planning a trip? Want a foodie guide that knows the **weather** and local **must-eats**? This tool gives you a **1-day food itinerary** that feels personal and exciting!

---

## 🔗 Inputs

| Input | Type   | Description                         |
|-------|--------|-------------------------------------|
| `location` | string | City for the food adventure |

---

## 🛠️ Tools & APIs Used

| Tool Name         | Purpose                            |
|------------------|------------------------------------|
| `weather_check`  | Pulls weather from OpenWeatherMap  |
| `dish_finder`    | Finds iconic dishes using Brave API|
| `restaurant_finder` | Finds top restaurants with Brave API |
| `Julep Agent`    | Converts results into story format |

---

## 🧠 Prompt Flow (YAML Overview)

```yaml
name: Foodie Tour Generator
description: Creates a 1-day foodie tour using weather, local dishes, and top restaurants

input_schema:
  type: object
  properties:
    location:
      type: string
      description: The city to generate the food tour for

tools:
  - name: weather_check
    type: integration
    integration:
      provider: weather
      method: get
      setup:
        openweathermap_api_key: "YOUR_API_KEY"

  - name: dish_finder
    type: integration
    integration:
      provider: brave
      method: search
      setup:
        brave_api_key: "YOUR_API_KEY"

  - name: restaurant_finder
    type: integration
    integration:
      provider: brave
      method: search
      setup:
        brave_api_key: "YOUR_API_KEY"

main:
  - tool: weather_check
    arguments:
      location: $ steps[0].input.location
    as: weather_data

  - tool: dish_finder
    arguments:
      query: $ "3 iconic local dishes of " + steps[0].input.location

  - tool: restaurant_finder
    arguments:
      query: $ "best restaurants serving [popular dishes] in " + steps[0].input.location
    as: restaurants

  - prompt:
    - role: system
      content: |
        You are a food-loving travel writer who creates delightful one-day food tours...
    - role: user
      content: |
        Create a 1-day food tour for {steps[0].input.location}...
