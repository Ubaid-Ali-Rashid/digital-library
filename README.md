# Digital Library System

A centralized digital library application that gives students easy access to semester PDFs (current and previous) from a single platform. Built with **Python** and the **KivyMD** library, with **SQLite** for data storage and a full client/admin login system.

## Features

- **Centralized PDF access** — all current and previous semester PDFs are stored in one place, accessible to any registered student.
- **Dual login system:**
  - **Client (student)** — can browse and access available PDFs.
  - **Admin** — has full control over content and user management.
- **Admin capabilities:**
  - Add new PDFs to the library
  - Add new semesters
  - View all registered client accounts
  - Block any client account at any time
- **Persistent storage** — all PDFs, accounts, and semester data are stored in SQLite.
- **Modern mobile-style UI** — built with KivyMD for a clean, Material Design–inspired interface.

## Tech Stack

- **Python** — core application logic
- **KivyMD** — UI framework (Material Design components on top of Kivy)
- **SQLite** — storage for PDFs, semesters, and user accounts

## How It Works

1. Users either log in as a **client** or an **admin**.
2. **Clients** see a browsable list of semesters and can open/view any PDF stored under them.
3. **Admins** get an additional management view where they can:
   - Upload new PDF documents under a chosen semester
   - Create new semester categories as the curriculum progresses
   - See a list of all client accounts that have registered
   - Block a client's account, instantly revoking their access
4. All data — PDF files, semester structure, and account records — is persisted in a local SQLite database.

## Key Concepts Demonstrated

- Role-based access control (client vs. admin)
- GUI development with KivyMD (screens, navigation, Material components)
- CRUD operations against SQLite (PDFs, semesters, accounts)
- Account management features (registration tracking, blocking/access control)
- File handling for storing and retrieving PDF documents

## Possible Future Improvements

- Add search/filter functionality across PDFs by subject, semester, or keyword.
- Add download progress indicators and offline caching for frequently accessed PDFs.
- Migrate from SQLite to a cloud-hosted database for multi-device sync across students.

## Author

**Ubaid Ali** — Computer Engineering student, UET Lahore.
