import string

# Estimate brute force time
def estimate_brute_force(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    total_combinations = charset ** len(password)
    guesses_per_second = 1e9  # Assume 1 billion guesses per second (modern GPU speed)
    seconds = total_combinations / guesses_per_second
    return seconds

# Human readable time format
def readable_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"

# Main
if __name__ == "__main__":
    password = input("Enter your password to analyze brute-force resistance: ")
    time_to_crack = estimate_brute_force(password)
    print(f"\nEstimated Time to Crack by Brute Force: {readable_time(time_to_crack)}")