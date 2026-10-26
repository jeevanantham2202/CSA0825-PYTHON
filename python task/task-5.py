# TASK 5 - Read Input and Convert Types

def process_clerk_entry():
    # Reading input from the clerk
    user_input = input("Enter litres or value (e.g., 8.5): ")
    
    # Check if the input is a valid number using string methods or try-except
    try:
        # Using float conversion inside try-except (Alternative Concept approach)
        value = float(user_input.strip())
        print(f"Valid numeric input received: {value}")
        
        # Demonstrating aligned results using f-strings with width and precision
        amount = 33400.3
        print(f"Formatted Amount: {amount:10.2f}")
        
    except ValueError:
        print(f"Error: Invalid input '{user_input}' cannot be converted to a float. Please enter a valid number.")

# Run the function
process_clerg_entry() if 'process_clerg_entry' in locals() else process_clerk_entry()
