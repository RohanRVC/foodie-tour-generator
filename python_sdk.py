from julep import Julep
import time
import yaml

def get_weather_prediction(location):
    client = Julep(api_key="your_keyys")

    agent = client.agents.create(
        name="Writing Assistant",
        model="claude-3.5-sonnet",
        about="A helpful AI assistant that specializes in writing and editing."
    )

    API_KEY_w = "your_keys"

    task_definition = yaml.safe_load("""
    name: Weather Request

    tools:
      - name: weather_call
        type: integration
        integration:
          provider: weather
          method: get
          setup:
            openweathermap_api_key: "your_keys"

    main:
    - tool: weather_call
      arguments:
        location: '{steps[0].input.Location}'
    """)

    task = client.tasks.create(
        agent_id=agent.id,
        **task_definition # Unpack the task definition
    )

    execution = client.executions.create(
        task_id=task.id,
        input={"Location": location}
    )

    # Wait for the execution to complete
    while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
        time.sleep(1)

    if result.status == "succeeded":
        weather_data = result.output['result']
        weather_dict= weather_output_to_dict(weather_data,location)
        return weather_dict
        # return analyze_weather_for_games(weather_dict)
    else:
        return f"Error: {result.error}"


def weather_output_to_dict(weather_output,location):
    """Convert the weather output string to a flat dictionary of weather metrics"""
    weather_dict = {}
    
    # Split the output into lines
    lines = weather_output.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.endswith(':'):  # Skip empty lines and section headers
            continue
            
        # Handle key-value pairs
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lstrip('-').strip()  # Remove hyphens and whitespace
            value = value.strip()
            
            if key in ['Wind speed', 'Humidity', 'Cloud cover', 
                      'Current', 'High', 'Low', 'Feels like']:
                num_value = ''.join(c for c in value if c.isdigit() or c == '.')
                weather_dict[key] = float(num_value) if num_value else value
            elif value == '{}':
                weather_dict[key] = {}
            else:
                weather_dict[key] = value
    
    return analyze_weather_for_games(weather_dict)

def analyze_weather_for_games(weather_data):
    try:
        temp = weather_data['Current']
        feels_like = weather_data['Feels like']
        humidity = weather_data['Humidity']
        wind_speed = weather_data['Wind speed']
        status = weather_data['Detailed status'].lower()
        
        good_outdoor_conditions = (
            (15 <= temp <= 30) and  
            (humidity < 80) and      # Not too humid
            (wind_speed < 10) and    # Not too windy
            ('rain' not in status) and 
            ('storm' not in status) and
            ('haze' not in status) and
            ('fog' not in status)
        )
        
        if good_outdoor_conditions:
            return "The weather is perfect for outdoor dining."
        else:
            reasons = []
            if temp < 15 or temp > 30:
                reasons.append(f"temperature ({temp}°C) is outside the comfortable range (15-30°C)")
            if humidity >= 80:
                reasons.append(f"high humidity ({humidity}%)")
            if wind_speed >= 10:
                reasons.append(f"high wind speed ({wind_speed} m/s)")
            if any(x in status for x in ['rain', 'storm', 'haze', 'fog']):
                reasons.append(f"poor atmospheric conditions ({status})")

            recommendation = "The weather is better suited for indoor meals due to:\n"
            recommendation += "\n".join(f"- {reason}" for reason in reasons)
            
            return recommendation
            
    except KeyError as e:
        return f"Error: Missing weather data field - {str(e)}"



def food_predictor(location,weather_update):
    client = Julep(api_key="your_keys")

    agent = client.agents.create(
        name="Writing Assistant",
        model="claude-3.5-sonnet",
        about="A helpful AI assistant that specializes in writing and editing."
    )


    task_definition = yaml.safe_load("""
name: Foodie Tour Generator
description: Creates a 1-day foodie tour for a city using weather, local dishes, and top restaurants
main:
  - prompt:
      - role: system
        content: You are a food-loving travel writer who makes fun, tasty, and weather-friendly one-day food tour plans.
      - role: user
        content:  |
            Create a foodie tour for {steps[0].input.locations} and weather is {steps[0].input.weather}.

         
            Write a full-day food trip plan (breakfast, lunch, dinner) using these dishes, restaurants, and weather. Make it feel like a fun short story.
            Ideal comfort food for a rainy or chilly evening inside.
            Sit at a rooftop or open air spot to end the day right.
    """)

    task = client.tasks.create(
        agent_id=agent.id,
        **task_definition 
    )

    execution = client.executions.create(
        task_id=task.id,
        input={"locations": location,'weather':weather_update}
    )

    while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
        pass

    if result.status == "succeeded":
        return result.output['choices'][0]['message']['content']
        # print(type(result.output['choices']))
    else:
        print(f"Error: {result.error}")


def all_locations_food_predictor(location):
    weather_condition=get_weather_prediction(location)
    print(f'Location is {location} and {weather_condition}\n\n',food_predictor(location,weather_condition))

# for i in ['Goa']:
#     all_locations_food_predictor(i)
#     print('\n*******************************************************************\n'*5)


print(food_predictor('abbeville',get_weather_prediction('Abbeville')))