import requests

def query_ollama(prompt):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {"model": "HI-ML", "prompt": prompt}

    try:
        response = requests.post(url, headers=headers, json=data)
        # Debugging: Print the raw response content
        print("Raw Response Text:", response.text)

        # Attempt to parse the response as JSON
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        # Handle JSON parsing errors
        print("JSON Decode Error:", str(e))
        print("Raw Response:", response.text)
        return {"error": "Invalid response from the server"}
    except requests.exceptions.RequestException as e:
        # Handle general request exceptions
        print("Request Error:", str(e))
        return {"error": "Failed to connect to the server"}

# Main script
if __name__ == "__main__":
    # Define your prompt
    prompt = "Hello, how can I assist you?"

    # Query the Ollama server
    response = query_ollama(prompt)

    # Print the result
    print("Response from Ollama:", response)
