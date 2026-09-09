# Food Waste Management System
### Academic Data Structures & Algorithms (DSA) Web Application (MCA Project)

A complete, full-stack web application designed to manage surplus food distribution, donors, recipient shelters, and logistics routes while **demonstrating 14 core Data Structures and Algorithms** in pure Python without using standard library shortcuts.

---

## 1. Project Purpose & Academic Relevance

Surplus food redistribution requires solving real-world challenges:
* How to manage dynamically growing food batches? (**Linked List**)
* How to ensure fair, chronological processing of recipient requests? (**FIFO Queue**)
* How to maintain audit logs with Undo capability? (**LIFO Stack**)
* How to model logistics routes between kitchens and shelters? (**Graph & BFS/DFS**)
* How to quickly locate specific food inventory? (**Linear & Binary Search**)
* How to sort food batches by quantity/urgency? (**Merge Sort**)
* How to quickly solve emergency shortages? (**Greedy Algorithm**)
* How to mathematically maximize societal priority benefit under budget limits? (**Dynamic Programming - 0/1 Knapsack**)
* How to assign donors to collection centers without violating capacities? (**Backtracking**)

---

## 2. Technology Stack

* **Frontend**: HTML5, Vanilla CSS3 (modern responsive design, canvas graphics), Vanilla JavaScript (AJAX, Canvas API).
* **Backend**: Python 3.x, Flask framework.
* **Database**: MySQL (with auto-fallback to SQLite for zero-setup execution).
* **Development Environment**: Visual Studio Code / Terminal.

---

## 3. DSA Mapping & Time Complexity Table

| # | DSA Concept | Custom Python File | Real-World Application in System | Time Complexity | Space Complexity |
|---|---|---|---|---|---|
| 1 | **Singly Linked List** | `dsa/linked_list.py` | Dynamic food inventory storage via `FoodNode` pointers | Insert: `O(1)`, Search/Delete: `O(n)` | `O(n)` |
| 2 | **Stack (LIFO)** | `dsa/stack.py` | Operational activity history & 1-Click Undo | Push/Pop/Peek: `O(1)` | `O(n)` |
| 3 | **Queue (FIFO)** | `dsa/queue.py` | Sequential processing of food requests in arrival order | Enqueue/Dequeue: `O(1)` | `O(n)` |
| 4 | **Binary Search Tree** | `dsa/bst.py` | Key-indexed searching & Inorder sorted traversal | Search/Insert: `O(log n)` avg, `O(n)` worst | `O(n)` |
| 5 | **Binary Tree** | `dsa/binary_tree.py` | Level-order tree representation & traversals | Traversals: `O(n)` | `O(n)` |
| 6 | **Graph (Adj List)** | `dsa/graph.py` | City hubs, collection centers, and shelter network | Add Edge/Vertex: `O(1)` | `O(V + E)` |
| 7 | **Breadth-First Search** | `dsa/graph.py` | Level-by-level route exploration using Queue | `O(V + E)` | `O(V)` |
| 8 | **Depth-First Search** | `dsa/graph.py` | Deep route branch exploration via recursion | `O(V + E)` | `O(V)` |
| 9 | **Linear Search** | `dsa/searching.py` | Sequential inspection on unsorted food items | `O(n)` | `O(1)` |
| 10 | **Binary Search** | `dsa/searching.py` | Divide-and-conquer on pre-sorted food batches | `O(log n)` | `O(1)` |
| 11 | **Merge Sort** | `dsa/sorting.py` | Divide-and-conquer sorting by quantity/expiry | `O(n log n)` | `O(n)` |
| 12 | **Greedy Algorithm** | `dsa/greedy.py` | Urgent-first heuristic allocation for quick relief | `O(n log n)` | `O(n)` |
| 13 | **Dynamic Programming** | `dsa/dynamic_programming.py` | 0/1 Knapsack optimal priority maximization | `O(n * W)` | `O(n * W)` |
| 14 | **Backtracking** | `dsa/backtracking.py` | Donor-to-center assignment with capacity pruning | `O(K^M)` worst case | `O(M)` |

---

## 4. Project Directory Structure

```
food-waste-management/
├── app.py                      # Flask Application Entry Point & Dashboard
├── config.py                   # App & Database Configuration
├── requirements.txt            # Python Dependencies
├── database.sql                # MySQL Schema & Initial Realistic Seed Data
├── README.md                   # Project Documentation & Viva Guide
│
├── dsa/                        # Pure Python Custom DSA Implementations
│   ├── linked_list.py          # FoodNode & FoodLinkedList
│   ├── stack.py                # StackNode & OperationsStack
│   ├── queue.py                # QueueNode & RequestQueue
│   ├── binary_tree.py          # TreeNode & BinaryTree
│   ├── bst.py                  # BSTNode & BinarySearchTree
│   ├── graph.py                # Graph (Adjacency List, BFS, DFS)
│   ├── searching.py            # Linear Search & Binary Search
│   ├── sorting.py              # Merge Sort, Quick Sort, Bubble Sort
│   ├── greedy.py               # Greedy Food Distribution
│   ├── dynamic_programming.py  # 0/1 Knapsack DP Allocation
│   └── backtracking.py         # Donor-Center Assignment with Backtracking
│
├── models/                     # Database Models
│   ├── food.py
│   ├── donor.py
│   ├── recipient.py
│   └── request.py
│
├── database/
│   └── db.py                   # Unified DB Connector (MySQL + SQLite fallback)
│
├── routes/                     # Modular Blueprints
│   ├── food_routes.py
│   ├── donor_routes.py
│   ├── recipient_routes.py
│   ├── request_routes.py
│   ├── location_routes.py
│   └── algorithm_routes.py
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Master Layout & Sidebar
│   ├── index.html              # Dashboard with Metrics & Stack Preview
│   ├── food.html               # Food Inventory & Linked List Canvas
│   ├── donors.html             # Donors Directory
│   ├── recipients.html         # Recipients & Urgency Levels
│   ├── requests.html           # Request Management & FIFO Queue Train
│   ├── locations.html          # Location Graph & BFS/DFS Runner
│   ├── algorithms.html         # Greedy vs DP vs Backtracking Playground
│   └── dsa_visualizer.html     # Dedicated 11-in-1 DSA Visualizer
│
└── static/
    ├── css/
    │   └── style.css           # Modern Responsive CSS
    └── js/
        └── script.js           # AJAX, Canvas Visualizer & Animation Engine
```

---

## 5. Setup & Installation Guide

### Step 1: Create and Activate Virtual Environment
```bash
# Windows (Command Prompt / PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup (MySQL)
1. Open MySQL Workbench, phpMyAdmin, or MySQL CLI:
   ```bash
   mysql -u root -p < database.sql
   ```
2. In `config.py`, verify your MySQL username and password:
   ```python
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'your_password'
   MYSQL_DB = 'food_waste_db'
   ```
*(Note: If MySQL is not running on your machine, the system automatically initializes a local SQLite database with all sample records so the application never crashes during demonstration).*

### Step 4: Run the Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/login
```

---

## 6. Multi-Role Login Credentials & Permissions

| Role | Username | Password | Dashboard & Permissions |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | **Full Admin Access**: System metrics, Food inventory CRUD, Requests FIFO queue dequeueing, Stack Undo, Location network editing, Greedy & DP Optimizer, and 11-in-1 DSA Visualizer. |
| **Food Donor (User)** | `ramesh` | `donor123` | **Donor Portal (`/donor/portal`)**: View own donated food batches, submit new surplus food donations, view urgent recipient demand, view nearby collection hubs. |
| **Food Receiver (Shelter)** | `thomas` | `receiver123` | **Receiver Portal (`/receiver/portal`)**: Enqueue food requests into the FIFO Queue, track request statuses, view available surplus food in the network. |
| **Self Registration** | *(Sign up)* | *(Custom)* | Visit `/register` to create a new Donor or Receiver account. |

*(Note: The login page includes 1-Click "Viva Demo Fill" buttons for all 3 roles to make viva demonstration effortless).*

---

## 6. How to Demonstrate During College MCA Viva

1. **Dashboard (`/`)**: Show live metrics, food expiring today alert banner, and the **LIFO Stack recent operations list**.
2. **Food Inventory (`/food`)**:
   - Demonstrate the **Linked List visualizer** (`HEAD -> Node 1 -> Node 2 -> ... -> NULL`).
   - Add a new food item; show pointer creation.
   - Run **Linear Search** (inspect comparison steps).
   - Run **Binary Search** and **Merge Sort** (show `O(n log n)` comparison count).
3. **Requests & Queue (`/requests`)**:
   - Show the **FIFO Queue visual train** (`FRONT -> ... -> REAR`).
   - Click **"Process Next Request"**; observe the front item dequeuing in $O(1)$ time.
4. **Stack Undo Demo (Top Bar)**:
   - Click **"Stack Undo (LIFO)"**; demonstrate that the last action is popped from the top of the stack and reversed.
5. **Location Graph (`/locations`)**:
   - Show the interactive graph canvas and adjacency list table.
   - Click **"Run BFS"** to demonstrate level-order queue traversal.
   - Click **"Run DFS"** to demonstrate deep recursive branch exploration.
6. **Algorithm Playground (`/algorithms`)**:
   - **Greedy**: Allocate food to requests by urgency; view step-by-step decision log.
   - **Dynamic Programming**: Enter food capacity $W$; inspect the optimal selection and the memoized 2D matrix $DP[i][w]$.
   - **Backtracking**: Run donor assignment; observe state exploration, constraint checks, and backtrack undo steps.
7. **DSA Visualizer (`/dsa-visualizer`)**:
   - Explore the 11 dedicated visualizer tabs and explain time/space complexities.

---

## 7. Faculty Viva Q&A Cheat Sheet

* **Q: Why use a custom Linked List instead of a Python list?**
  * *A:* Python's `list` is a dynamic array with contiguous memory reallocation. A custom Linked List demonstrates explicit node pointer manipulation (`node.next`), offering $O(1)$ insertion at the head and dynamic growth.
* **Q: Difference between Greedy and Dynamic Programming here?**
  * *A:* Greedy makes locally optimal choices (highest priority first) at each step and never backtracks ($O(n \log n)$). Dynamic Programming considers overlapping subproblems, guaranteeing the mathematical global maximum priority benefit ($O(n \cdot W)$).
* **Q: How does BFS differ from DFS in our supply chain graph?**
  * *A:* BFS uses a FIFO Queue to find nearest neighboring collection hubs level-by-level (optimal for shortest hop routes). DFS uses recursion/stack to explore a continuous logistics corridor from start to finish before backtracking.
