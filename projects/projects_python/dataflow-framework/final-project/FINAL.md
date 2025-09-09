Final Project Reflection
1. Design Decisions
I built the project by separating key parts: file watching, data processing, and a dashboard. This made it easier to manage and update each part. Decided to use basic HTML+CSS and JS to create the frontend for the dashboard for simplicity.
2. Tradeoffs
I have tried to keep the project simple but at some places, one may find some inconsistencies. Like previously I refrained from using regex but have used in some places. Current limitations would be no restricted write access to output.
3. Scalability
If input grew 100 times, we would require an evolved version of the DAG or State based Routing Implementation.
4. Extensibility & Security
To run for real users, secure file upload and proper user authentication would be needed. Also, limiting upload size and protecting data in transit and at rest would improve safety. The dashboard APIs should require login and secure connections. To protect the output write permissions to the output folder can be restricted.
