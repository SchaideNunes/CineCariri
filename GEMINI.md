# Project Rules

1. **Incremental Development**: We will build the project one feature at a time.
2. **Test-Driven Development (TDD)**: 
   - For every new feature or function, we MUST write a test FIRST.
   - We run the test (it should fail).
   - We write the implementation to make the test pass.
   - If the implementation fails, we try again until it passes.
3. **Technology Stack**:
   - **Backend**: Python (FastAPI), SQLAlchemy (ORM), Pytest (for testing).
   - **Database**: Relational Database (PostgreSQL).
   - **Frontend**: React (Vite) with Vanilla CSS (No Tailwind unless explicitly requested).
4. **Design Aesthetic**:
   - The frontend must be visually stunning, using rich colors, modern typography, glassmorphism, and dynamic animations. 
   - It should resemble the reference image provided by the user (Orient Cinemas style).
5. **Data Model Integrity**:
   - Careful consideration of relationships between Users, Movies, Showtimes, and Reservations.
   - Robust handling of overbooking (concurrency control when reserving seats).
6. **Documentation**:
   - Keep this file updated if new rules are established.
7. **Version Control**:
   - Commit code to GitHub after every major feature implementation (e.g., after endpoints and tests are completed for an entity) rather than waiting for the entire phase to end, providing an accurate view of progress.
