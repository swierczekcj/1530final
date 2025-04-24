# Course Critic


A personalized, peer-driven course review platform built for Computer Science students at the University of Pittsburgh.

CourseCritic helps students make informed decisions when registering for classes by providing real-time feedback on courses and professors from fellow students. Developed as a final project for CS 1530, the platform bridges gaps left by legacy systems like RateMyProfessor and outdated departmental wikis.

---

## ✨ Features

- **Course & Professor Browsing**
  - Searchable course list
  - Dedicated course and professor pages

- **Review System**
  - Submit reviews including difficulty, workload, and written feedback
  - Associate reviews with specific professors

- **Voting System**
  - Upvote/downvote functionality for prioritizing helpful reviews

- **Statistics Display**
  - Average difficulty and workload displayed per course

- **Admin Portal**
  - Interface to create new courses manually

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (custom theme), Jinja2 Templates
- **Database:** SQLite with SQLAlchemy ORM
- **Architecture:** MVC (Model-View-Controller)

---

## 🏗️ System Architecture

- **View:** Web pages for home, course, professor, admin, and submission pages
- **Controller:** Flask routes manage user interaction logic and form processing
- **Model:** SQLAlchemy models for `Course`, `Professor`, and `Rating`

A deployment diagram and UML class models are included in the design documentation.

---

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/swierczekcj/1530final.git
   cd 1530final
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip3 install flask
   pip3 install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python3 -m flask --app course_critic.py run
   ```
   Visit `http://127.0.0.1:5000` in your browser.

---

## 🔍 Usage

- Navigate to the homepage to search or view all courses
- Click a course to see reviews, professor ratings, and submit your own
- Admins can add new courses via the `/admin` page
- No login is currently required to submit reviews or interact with the site

---

## 👩‍💼 Team & Roles

- **Scrum Master:** Gabrielle Martin
- **Product Owner:** Anita Kaul
- **Developers:** Maya Blackburn, Cameron Mickey, Cole Swierczek, Russell Kirkpatrick

---

## ⚡ Future Improvements

- Implement user authentication
- Enable review moderation
- Expand to departments beyond CS
- Mobile responsiveness

---

## 📁 Resources

- [Final Codebase on GitHub](https://github.com/swierczekcj/1530final)
- [CS 1530 Final Presentation](./CS%201530%20Final%20Presentation-2.pdf)
- [System Design & Team Docs](./CS1530%20Team%20Project%20-%20System%20Design.pdf)

---

## ✉ License

This project is for educational purposes only and is not licensed for commercial use.


