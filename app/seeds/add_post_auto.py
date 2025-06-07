from datetime import datetime
import random
from firebase_admin import firestore

db = firestore.client()


titles = [
    "My First Python App",
    "Mastering JavaScript Functions",
    "Exploring React Native",
    "Building a REST API with FastAPI",
    "Getting Started with Flutter",
    "Creating My First Website",
    "Intro to Full Stack Development",
    "Deploying with Firebase",
    "Using Git and GitHub Efficiently",
    "Fixing My First Bug",
    "Learning About Databases",
    "How I Built a To-Do App",
    "Understanding API Authentication",
    "Responsive Design with Flexbox",
    "Building a Portfolio Website",
    "Creating Dynamic Forms",
    "Styling with Tailwind CSS",
    "My Journey with Web Dev",
    "FastAPI vs Django: My Thoughts",
    "Working on a Team Project",
    "Handling User Input Securely",
    "Debugging Tips for Beginners",
    "Connecting Frontend to Backend",
    "Publishing My App Online",
    "Learning by Breaking Things",
    "Setting Up a Dev Environment",
    "Why I Love Programming",
    "How I Built My Blog",
    "Project Planning with Trello",
    "Building an API in 2 Hours"
]


contents = [
    "Today I built a simple Python app that prints out user input. It was a great learning experience.",
    "I finally understood how JavaScript functions work and how to pass callbacks.",
    "React Native is so powerful! I managed to make my first mobile UI.",
    "FastAPI makes API development super fast and fun. Highly recommended.",
    "Flutter's widget system is amazing once you get the hang of it.",
    "I just launched my first static website using HTML and CSS!",
    "Learning both frontend and backend is tough, but I’m getting there.",
    "I deployed my web app using Firebase Hosting. Smooth process!",
    "Git version control is essential. I learned how to resolve merge conflicts.",
    "Debugging my first code error made me appreciate good syntax.",
    "Exploring databases helped me understand how to store and retrieve data.",
    "I created a to-do app to help manage my tasks better.",
    "Authentication was tricky, but now I understand how tokens work.",
    "Flexbox made my layout so much cleaner and responsive!",
    "I designed my own portfolio to showcase my projects and skills.",
    "Creating dynamic forms with React was a great experience.",
    "Tailwind CSS made styling components quick and reusable.",
    "This post is about my progress in web development so far.",
    "I compared FastAPI and Django for a backend project—each has its pros.",
    "Team projects help you learn real-world collaboration and Git flow.",
    "I learned how to validate user input securely and prevent XSS.",
    "Sometimes bugs teach more than tutorials. I keep learning.",
    "Linking React with backend APIs was easier than I thought!",
    "I finally hosted my first app online. Feels amazing!",
    "Breaking things intentionally helped me understand how they work.",
    "I organized my tools for faster development and better structure.",
    "Programming makes me feel creative and logical at the same time.",
    "I built my own blog platform to share my dev journey.",
    "Using Trello really helped me plan and manage my project tasks.",
    "I created a mini API project in under 2 hours. Great practice!"
]


images_pool = [
    "https://images.unsplash.com/photo-1672922310200-fff31138251e?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1568716353609-12ddc5c67f04?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1522071901873-411886a10004?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1415&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1610018556010-6a11691bc905?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNzc3xlbnwwfHwwfHx8Mg%3D%3D",
    "https://images.unsplash.com/photo-1610018556010-6a11691bc905?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNzc3xlbnwwfHwwfHx8Mg%3D%3D",
    "https://images.unsplash.com/photo-1654375408506-d46c2b43308f?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGl0JTIwcHJvZ3JhbW1pbmd8ZW58MHx8MHx8fDA%3D",
    "https://images.unsplash.com/photo-1698919585693-191c51b66cde?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8aXQlMjBwcm9ncmFtbWluZ3xlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1614741118887-7a4ee193a5fa?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGl0JTIwcHJvZ3JhbW1pbmd8ZW58MHx8MHx8fDA%3D",
    "https://images.unsplash.com/photo-1555680510-34daedadbdb1?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fHdlYnxlbnwwfHwwfHx8Mg%3D%3D",
    "https://images.unsplash.com/photo-1599837565318-67429bde7162?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y3NzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1669023414166-a4cc7c0fe1f5?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y3NzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1493119508027-2b584f234d6c?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGNzc3xlbnwwfHwwfHx8Mg%3D%3D",
    "https://images.unsplash.com/photo-1610018556010-6a11691bc905?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNzc3xlbnwwfHwwfHx8Mg%3D%3D",
    "https://images.unsplash.com/photo-1610018556010-6a11691bc905?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNzc3xlbnwwfHwwfHx8Mg%3D%3D",
    "https://cdn.pixabay.com/photo/2016/03/26/13/09/workspace-1280538_640.jpg",
    "https://cdn.pixabay.com/photo/2019/07/14/16/27/pen-4337521_640.jpg",
    "https://cdn.pixabay.com/photo/2016/11/21/15/08/playstation-1845880_640.jpg",
    "https://cdn.pixabay.com/photo/2015/08/13/01/00/keyboard-886462_640.jpg",
    "https://cdn.pixabay.com/photo/2016/06/25/12/52/laptop-1478822_640.jpg",
    "https://cdn.pixabay.com/photo/2020/04/08/16/32/keyboard-5017973_640.jpg",
    "https://cdn.pixabay.com/photo/2021/08/04/13/06/software-developer-6521720_640.jpg",
    "https://cdn.pixabay.com/photo/2015/01/09/11/11/office-594132_640.jpg",
    "https://cdn.pixabay.com/photo/2019/07/14/16/29/pen-4337524_640.jpg",
    "https://cdn.pixabay.com/photo/2020/04/08/16/32/keyboard-5017973_640.jpg",
    "https://cdn.pixabay.com/photo/2016/01/19/15/05/computer-1149148_640.jpg",     
    "https://cdn.pixabay.com/photo/2015/08/13/01/00/keyboard-886462_640.jpg",
    "https://cdn.pixabay.com/photo/2019/07/14/16/29/pen-4337524_640.jpg",
    "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1415&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
]
tags = ["development", "learning", "experience", "journey", "coding", "programming", "webdev", "mobiledev", "api", "design", "portfolio", "project", "teamwork", "debugging", "authentication", "flexbox", "css", "html", "firebase", "git"]

shuffled_indexes = list(range(len(titles)))  # [0, 1, ..., 29]
random.shuffle(shuffled_indexes)  # Shuffle to randomize order

title_index = 0

for user_id in range(40, 87):  # 10 users
    for _ in range(1):  # 3 posts per user = 30 total
        idx = shuffled_indexes[title_index]
        title = titles[idx]
        content = contents[idx]
        title_index += 1

        tags_sample = random.sample(tags, k=random.randint(3, 5))
        images_sample = random.sample(images_pool, k=random.randint(1, 3))

        post_data = {
            "user_id": str(user_id),
            "title": title,
            "content": content,
            "tags": tags_sample,
            "images": images_sample,
            "created_at": datetime.utcnow(),
        }

        db.collection("posts").add(post_data)

        print(f"Added post {title_index}/30 for user {user_id}: {title}")
