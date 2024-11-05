import os
import base64
import subprocess
import random
from datetime import datetime, timedelta

# Configuration
commit_file = "lyrics_base64.txt"  # File to commit
lyrics = """When sky blue gets dark enough
To see the colors of the city lights
A trail of ruby red and diamond white
Hits her like a sunrise
She comes and goes and comes and goes
Like no one can
Tonight she's out to lose herself
And find a high on Peachtree Street
From mixed drinks to techno beats it's always
Heavy into everything
She comes and goes and comes and goes
Like no one can
She comes and goes and no one knows
She's slipping through my hands
She's always buzzing just like
Neon, neon
Neon, neon
Who knows how long, how long, how long
She can go before she burns away
I can't be her angel now
You know it's not my place to hold her down
And it's hard for me to take a stand
When I would take her anyway I can
She comes and she goes
Like no one can
She comes and she goes
She's slipping through my hands
She's always buzzing just like
Neon, neon
Neon, neon
Who knows how long, how long, how long
She can go before she burns away, away
She comes and she goes
Like no one can
She comes and she goes
She's slipping through my hands
She's always buzzing just like
Neon, neon
Neon, neon
Who knows how long, how long, how long
She can go before she burns away, away
"""

# Encode lyrics to Base64
encoded_lyrics = base64.b64encode(lyrics.encode('utf-8')).decode('utf-8')

# Split encoded lyrics into chunks (for example, 50 characters at a time)
chunk_size = 20
chunks = [encoded_lyrics[i:i + chunk_size] for i in range(0, len(encoded_lyrics), chunk_size)]

# Define the start and end date for the past year
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Create a set of unique random dates within the past year
unique_dates = {
    start_date + timedelta(days=random.randint(0, 365))
    for _ in range(len(chunks))
}

# Create random commits for each chunk using the unique random dates
for date in sorted(unique_dates):
    chunk = chunks.pop(0)  # Get the next chunk to commit

    # Write the chunk to the file
    with open(commit_file, "a") as f:
        f.write(f"{chunk}\n")
    
    # Add and commit the changes with the specified date
    subprocess.run(["git", "add", commit_file])
    commit_message = f"Add Base64 chunk committed on {date.strftime('%Y-%m-%d')}"
    commit_date = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Use Git environment variables to set the date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date
    env["GIT_COMMITTER_DATE"] = commit_date
    subprocess.run(["git", "commit", "-m", commit_message], env=env)

# Push to GitHub
subprocess.run(["git", "push", "--force", "origin", "main"])


