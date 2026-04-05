This is the second lab exercise on distributed systems for the course CSE_327 2026.
The subject of the lab is fault tolerance.
You are given a working implementation that needs improvement.

All information and instructions are in the /lab_documentation directory.

### Note on .env files

In this project, the .env file is intentionally ignored via .gitignore. This is standard practice because .env files typically contain environment-specific configuration such as API keys, database credentials, or other sensitive values that should not be committed to version control. Even in cases where no secrets are present (like in this lab), following this pattern helps build good habits early.

Instead, we provide a .env.example file. This file contains the required variable names and structure, but without any real or sensitive values. Students can copy this file to .env and fill in the appropriate values for their own environment. This approach keeps the repository clean, avoids accidental exposure of sensitive data, and ensures consistency across different setups.

Even though this lab does not include real secrets, using .env + .env.example reflects how real-world projects are structured and is considered a best practice.
