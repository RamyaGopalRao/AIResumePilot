# AIResumePilot

**AIResumePilot** is an innovative AI-powered resume parser and job shortlisting application built with **Django**, **OpenAI**, and a user-friendly UI designed with **HTML** and **Telerik Controls**. This platform automates the recruitment process by extracting key information from resumes, analyzing candidate qualifications, and intelligently matching them to job listings.

---

## Features
1. **Resume Upload**:
   - Upload single resumes or bulk resumes (as a folder) via a clean and responsive web interface.
   - Supports `.pdf` and `.docx` file formats.
2. **Multiprocessing for Bulk Processing**:
   - Processes multiple resumes concurrently for faster handling of bulk uploads.
3. **Text Extraction**:
   - Utilizes `PyPDF2` and `python-docx` for extracting content from resumes.
4. **OpenAI Integration**:
   - Sends extracted resume content to OpenAI's API for parsing and extracting:
     - Name, Email, Phone
     - Skills
     - Education (degree, specialization, institution, year)
     - Experience (position, company, duration)
5. **Database Integration**:
   - Stores extracted resume data in Django models:
     - `Resume`
     - `Education`
     - `Experience`
     - `Skill`
   - Flags duplicate resumes based on email and phone fields.
6. **Skill and Job Listings**:
   - Admins or users can add and manage:
     - Skills
     - Job listings (required skills, description, experience, etc.)
7. **Job Matching**:
   - Matches resumes to job listings based on skillsets and experience.
8. **UI with Telerik Controls**:
   - Offers interactive grids, tables, and controls for adding, viewing, and managing resumes, jobs, and skillsets efficiently.

---

## Architecture Overview

### Workflow
1. **Upload**:
   - Users upload single or multiple resumes via the HTML-based web interface with Telerik-enhanced form controls.
   - Uploaded files are saved in the `media/uploads/` directory for processing.

2. **Resume Processing**:
   - For single files, text is extracted and processed sequentially.
   - For folders, multiprocessing is applied to process multiple resumes concurrently.

3. **AI-Powered Parsing**:
   - Extracted resume content is sent to OpenAI for structured data parsing.
   - Returns resume details in JSON format.

4. **Database Operations**:
   - Parsed data is stored in the database:
     - `Resume`, `Education`, `Experience`, `Skill`.
   - Duplicate resumes are identified and flagged.

5. **Job Matching**:
   - Compares job requirements (skills) with parsed resume data.
   - Returns a list of matching resumes for each job listing.

6. **Responsive UI**:
   - Users can manage resumes, job listings, and skillsets via Telerik-powered grids and tables.
   - Offers interactive sorting, filtering, and editing for an enhanced user experience.

---

### Architecture Diagram

```plaintext
+--------------------------+        +----------------------------+        +-----------------------------+
|   User Uploads Resumes   | -----> |       File Handler         | -----> |       Resume Parser          |
|  (Single/Multiple Files) |        | (Save & Multiprocessing)  |        | (AI-Powered Parsing via OpenAI) |
+--------------------------+        +----------------------------+        +-----------------------------+
                                                                               |
                                                                               v
+---------------------------+        +----------------------------+        +-----------------------------+
|       Database Layer      | <-----|   Parsed Resume Details    | -----> |      Job Matching Engine     |
| (Resumes, Jobs, Skills)   |        | (Structured JSON Data)     |        | (Skill & Experience Matching)|
+---------------------------+        +----------------------------+        +-----------------------------+
                                                                               |
                                                                               v
+---------------------------+        +----------------------------+        +-----------------------------+
|       Telerik UI Layer    | <-----|  User Interaction via Web  | -----> |   Grids, Tables, and Forms   |
|  (HTML + Telerik Controls)|        |     (Data Management)     |        | (Manage Resumes & Job Listings)|
+---------------------------+        +----------------------------+        +-----------------------------+
