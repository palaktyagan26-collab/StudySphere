
import streamlit as st
from datetime import date, datetime
import database as db
import timer
import plotly.express as px

# Initialize the database and create tables if they don't exist
db.init_db()

# 1. Page settings
st.set_page_config(
    page_title="StudySphere",
    page_icon="🎓",
    layout="wide"
)

# 2. Dashboard design
st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F7F5EF;
    color: #263746;
}

/* Main headings */
h1, h2, h3 {
    color: #172B3A !important;
    font-weight: 700 !important;
}

/* Normal text */
p, li, label {
    color: #263746;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #172B3A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #263746 !important;
    -webkit-text-fill-color: #263746 !important;
    border: 1px solid #C8C3B7 !important;
    border-radius: 7px !important;
    caret-color: #172B3A !important;
}

/* Dropdowns */
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #263746 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #E1DDD3;
}

[data-testid="stMetricValue"] {
    color: #172B3A !important;
}

/* Buttons */
.stButton button, .stFormSubmitButton button {
    background-color: #E8D5AE !important;
    color: #172B3A !important;
    -webkit-text-fill-color: #172B3A !important;
    border: 1px solid #B18A4A !important;
    border-radius: 7px;
    font-weight: 700;
}

.stButton button:hover, .stFormSubmitButton button:hover {
    background-color: #B18A4A !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #B18A4A !important;
}
.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #B18A4A !important;
    border-color: #B18A4A !important;
    color: #FFFFFF !important;
}

/* Forms and expanders */
[data-testid="stForm"],
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #E1DDD3;
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #D9D3C7 !important;
}

</style>
""", unsafe_allow_html=True)


# 3. Sidebar navigation
st.sidebar.title("🎓 StudySphere")
st.sidebar.caption("Your Personal Study Manager")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Subjects", "Tasks", "Timetable",
     "Study Timer", "Notes", "Analytics"]
)


# 4. Dashboard

if page == "Dashboard":

    st.title("🎓 Welcome to StudySphere!")
    st.write("Your personal student productivity dashboard.")

    st.divider()

    # Get data from database
    subjects = db.get_subjects()
    tasks = db.get_tasks()

    # Calculate task statistics
    total_subjects = len(subjects)
    total_tasks = len(tasks)

    completed = sum(
        1 for task in tasks if task[5] == "Completed"
    )

    pending = total_tasks - completed

    if total_tasks > 0:
        progress = completed / total_tasks
    else:
        progress = 0

    # Overview cards
    st.subheader("📊 Your Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Subjects", total_subjects)
    col2.metric("📝 Total Tasks", total_tasks)
    col3.metric("✅ Completed", completed)
    col4.metric("⏳ Pending", pending)

    st.divider()

    # Progress section
    st.subheader("🎯 Your Study Progress")

    st.progress(progress)

    st.write(
        f"You have completed {progress * 100:.1f}% of your tasks."
    )

    st.divider()

    # Upcoming and overdue tasks
    st.subheader("📅 Deadline Overview")

    today = date.today().isoformat()

    overdue_tasks = [
        task for task in tasks
        if task[3] and task[3] < today and task[5] != "Completed"
    ]

    upcoming_tasks = [
        task for task in tasks
        if task[3] and task[3] >= today and task[5] != "Completed"
    ]

    if overdue_tasks:
        st.warning(
            f"You have {len(overdue_tasks)} overdue task(s)."
        )

        for task in overdue_tasks:
            st.write(f"🔴 {task[1]} - Deadline: {task[3]}")

    else:
        st.success("You have no overdue tasks!")

    if upcoming_tasks:

        st.write("**Upcoming deadlines:**")

        for task in upcoming_tasks[:5]:
            st.write(
                f"📌 {task[1]} | {task[2]} | Due: {task[3]}"
            )

    else:
        st.info("No pending upcoming deadlines.")

    st.divider()

    # Recent tasks
    st.subheader("📝 Your Recent Tasks")

    if tasks:

        for task in tasks[:5]:

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**{task[1]}**")
                st.caption(
                    f"Subject: {task[2] or 'Not assigned'}"
                )
                st.caption(f"Deadline: {task[3]}")

            with col2:

                if task[5] == "Completed":
                    st.success("Completed")
                else:
                    st.warning("Pending")

            st.divider()

    else:
        st.info(
            "You haven't added any tasks yet. "
            "Visit the Tasks page to get started."
        )

    st.caption("StudySphere | Your learning, organised.")

# 5. Subject Management
elif page == "Subjects":

    st.title("📚 Subject Management")

    st.write("Add and manage your college subjects.")

    with st.form("subject_form"):

        subject_name = st.text_input("Subject Name")
        teacher_name = st.text_input("Teacher Name")

        submitted = st.form_submit_button("Add Subject")

        if submitted:

            if subject_name.strip():

                db.add_subject(
                    subject_name.strip(),
                    teacher_name.strip()
                )

                st.success("Subject added successfully!")
                st.rerun()

            else:
                st.warning("Please enter a subject name.")

    st.divider()

    st.subheader("Your Subjects")

    subjects = db.get_subjects()

    if subjects:

        for subject in subjects:

            col1, col2 = st.columns([4, 1])

            col1.write(
                f"**{subject[1]}** — "
                f"{subject[2] or 'Teacher not specified'}"
            )

            if col2.button("Delete", key=f"subject_{subject[0]}"):

                db.delete_subject(subject[0])
                st.success("Subject deleted!")
                st.rerun()

    else:
        st.info("No subjects added yet.")


# 6. Task Management
elif page == "Tasks":

    st.title("📝 Task Management")

    st.write("Manage your assignments and deadlines.")

    subjects = db.get_subjects()

    if subjects:

        subject_options = {
            subject[1]: subject[0]
            for subject in subjects
        }

        with st.form("task_form"):

            task_title = st.text_input("Task Name")

            selected_subject = st.selectbox(
                "Select Subject",
                list(subject_options.keys())
            )

            deadline = st.date_input(
                "Deadline",
                value=date.today()
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"]
            )

            submitted = st.form_submit_button("Add Task")

            if submitted:

                if task_title.strip():

                    db.add_task(
                        task_title.strip(),
                        subject_options[selected_subject],
                        deadline.isoformat(),
                        priority
                    )

                    st.success("Task added successfully!")
                    st.rerun()

                else:
                    st.warning("Please enter a task name.")

    else:
        st.warning("Please add a subject before creating a task.")

    st.divider()

    st.subheader("📋 All Tasks")

    tasks = db.get_tasks()

    if tasks:

        for task in tasks:

            st.write(f"**{task[1]}**")
            st.caption(
                f"Subject: {task[2] or 'None'} | "
                f"Deadline: {task[3]} | "
                f"Priority: {task[4]}"
            )

            col1, col2, col3 = st.columns([2, 2, 1])

            current_status = task[5]

            status_options = ["Pending", "Completed"]

            selected_status = col1.selectbox(
                "Task Status",
                status_options,
                index=status_options.index(current_status),
                key=f"status_{task[0]}"
            )

            if col2.button("Update Status", key=f"update_{task[0]}"):

                db.update_task_status(
                    task[0],
                    selected_status
                )

                st.success("Status updated!")
                st.rerun()

            if col3.button("Delete", key=f"delete_{task[0]}"):

                db.delete_task(task[0])
                st.success("Task deleted!")
                st.rerun()

            st.divider()

    else:
        st.info("No tasks available. Add your first task!")
# 7. Timetable Management

elif page == "Timetable":

    st.title("📅 My Weekly Timetable")
    st.write("Manage your weekly classes and study sessions.")

    subjects = db.get_subjects()

    if not subjects:
        st.warning("Please add subjects first from the Subjects page.")

    else:
        subject_names = [subject[1] for subject in subjects]

        st.subheader("Add a New Session")

        with st.form("timetable_form"):

            day = st.selectbox(
                "Select Day",
                [
                    "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"
                ]
            )

            subject = st.selectbox(
                "Select Subject",
                subject_names
            )

            start_time = st.time_input(
                "Start Time",
                value=datetime.strptime("09:00", "%H:%M").time()
            )

            end_time = st.time_input(
                "End Time",
                value=datetime.strptime("10:00", "%H:%M").time()
            )

            submit = st.form_submit_button("Add to Timetable")

            if submit:

                if end_time <= start_time:
                    st.error("End time must be later than start time.")

                else:
                    db.add_timetable(
                        day,
                        subject,
                        str(start_time),
                        str(end_time)
                    )

                    st.success("Subject added to timetable!")
                    st.rerun()

    st.divider()

    st.subheader("My Weekly Schedule")

    timetable = db.get_timetable()

    if timetable:

        for entry in timetable:

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**{entry[1]} – {entry[2]}**")
                st.write(f"{entry[3]} to {entry[4]}")

            with col2:
                if st.button("Delete", key=f"delete_time_{entry[0]}"):
                    db.delete_timetable(entry[0])
                    st.rerun()

            st.divider()

    else:
        st.info("Your timetable is empty. Add your first session above.")
#8. Timer Management

elif page == "Study Timer":
    timer.study_timer()

#9. Notes Management

elif page == "Notes":

    st.title("📝 My Study Notes")
    st.write("Create and manage your study notes.")

    subjects = db.get_subjects()

    subject_names = ["General"] + [
        subject[1] for subject in subjects
    ]

    st.subheader("Create a New Note")

    with st.form("notes_form"):

        title = st.text_input("Note Title")

        subject = st.selectbox(
            "Select Subject",
            subject_names
        )

        content = st.text_area(
            "Write Your Notes",
            height=180
        )

        submit = st.form_submit_button("Save Note")

        if submit:

            if title.strip() == "" or content.strip() == "":
                st.error("Please enter both title and content.")

            else:
                db.add_note(title, subject, content)

                st.success("Note saved successfully!")
                st.rerun()

    st.divider()

    st.subheader("My Saved Notes")

    notes = db.get_notes()

    if notes:

        for note in notes:

            with st.expander(f"📖 {note[1]}"):

                st.write(f"**Subject:** {note[2]}")
                st.caption(f"Created: {note[4]}")
                st.write(note[3])

                st.divider()

                with st.form(f"edit_note_{note[0]}"):

                    new_title = st.text_input(
                        "Edit Title",
                        value=note[1]
                    )

                    new_subject = st.selectbox(
                        "Edit Subject",
                        subject_names,
                        index=subject_names.index(note[2])
                        if note[2] in subject_names else 0
                    )

                    new_content = st.text_area(
                        "Edit Content",
                        value=note[3],
                        height=150
                    )

                    update = st.form_submit_button("Update Note")

                    if update:

                        if new_title.strip() == "" or new_content.strip() == "":
                            st.error("Title and content cannot be empty.")

                        else:
                            db.update_note(
                                note[0],
                                new_title,
                                new_subject,
                                new_content
                            )

                            st.success("Note updated!")
                            st.rerun()

                if st.button("🗑️ Delete Note", key=f"delete_note_{note[0]}"):

                    db.delete_note(note[0])
                    st.success("Note deleted!")
                    st.rerun()

    else:
        st.info("No notes saved yet. Create your first note!")


# 10. Analystics and Insights

elif page == "Analytics":

    st.title("📊 StudySphere Analytics")
    st.write("Track your academic tasks and productivity.")

    # Fetch database information
    subjects = db.get_subjects()
    tasks = db.get_tasks()

    # Calculate statistics
    total_subjects = len(subjects)
    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task[5] == "Completed"
    )

    pending_tasks = total_tasks - completed_tasks

    # Calculate completion percentage
    if total_tasks > 0:
        completion = (completed_tasks / total_tasks) * 100
    else:
        completion = 0

    # Display overview cards
    st.subheader("📌 Overall Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Subjects", total_subjects)
    col2.metric("Total Tasks", total_tasks)
    col3.metric("Completed", completed_tasks)
    col4.metric("Pending", pending_tasks)

    st.divider()

    # Progress section
    st.subheader("🎯 Task Completion Progress")

    st.progress(completion / 100)

    st.write(f"**{completion:.1f}%** of your tasks completed.")

    st.divider()

    if total_tasks > 0:

        # Task status chart
        st.subheader("📈 Completed vs Pending Tasks")

        status_chart = px.pie(
            names=["Completed", "Pending"],
            values=[completed_tasks, pending_tasks],
            hole=0.5,
            title="Task Status Distribution"
        )

        st.plotly_chart(
            status_chart,
            use_container_width=True
        )

        st.divider()

        # Subject-wise analysis
        st.subheader("📚 Subject-wise Task Distribution")

        subject_counts = {}

        for task in tasks:

            subject_name = task[2] or "No Subject"

            subject_counts[subject_name] = (
                subject_counts.get(subject_name, 0) + 1
            )

        subject_chart = px.bar(
            x=list(subject_counts.keys()),
            y=list(subject_counts.values()),
            labels={
                "x": "Subject",
                "y": "Number of Tasks"
            },
            title="Tasks Assigned to Each Subject"
        )

        st.plotly_chart(
            subject_chart,
            use_container_width=True
        )

        st.divider()

        # Priority analysis
        st.subheader("⚡ Task Priority Analysis")

        priority_counts = {}

        for task in tasks:

            priority = task[4] or "Not Set"

            priority_counts[priority] = (
                priority_counts.get(priority, 0) + 1
            )

        priority_chart = px.bar(
            x=list(priority_counts.keys()),
            y=list(priority_counts.values()),
            labels={
                "x": "Priority",
                "y": "Number of Tasks"
            },
            title="Tasks by Priority"
        )

        st.plotly_chart(
            priority_chart,
            use_container_width=True
        )

    else:

        st.info(
            "No tasks available yet. Add tasks to see your analytics."
        )

    st.divider()

    st.caption(
        "StudySphere Analytics | Data is calculated from your saved tasks."
    )

st.divider()

st.caption("StudySphere | Created using Python")
