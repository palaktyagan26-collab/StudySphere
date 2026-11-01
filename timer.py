
import streamlit as st
import time

def study_timer():

    st.title("⏱️ Study Timer")
    st.write("Stay focused and manage your study sessions.")

    # Timer settings
    study_minutes = st.selectbox(
        "Select Study Duration",
        [15, 25, 30, 45, 60],
        index=1
    )

    break_minutes = st.selectbox(
        "Select Break Duration",
        [5, 10, 15],
        index=0
    )

    # Initialize session state
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "timer_end" not in st.session_state:
        st.session_state.timer_end = 0

    if "timer_duration" not in st.session_state:
        st.session_state.timer_duration = 0

    if "timer_type" not in st.session_state:
        st.session_state.timer_type = "Study"

    # Start timer
    if st.button("▶ Start Study Session"):

        st.session_state.timer_duration = study_minutes * 60
        st.session_state.timer_end = time.time() + study_minutes * 60
        st.session_state.timer_type = "Study"
        st.session_state.timer_running = True

    # Start break
    if st.button("☕ Start Break"):

        st.session_state.timer_duration = break_minutes * 60
        st.session_state.timer_end = time.time() + break_minutes * 60
        st.session_state.timer_type = "Break"
        st.session_state.timer_running = True

    # Reset timer
    if st.button("↺ Reset Timer"):

        st.session_state.timer_running = False
        st.session_state.timer_end = 0
        st.session_state.timer_duration = 0

    st.divider()

    # Display timer
    if st.session_state.timer_running:

        remaining = max(
            0,
            int(st.session_state.timer_end - time.time())
        )

        minutes = remaining // 60
        seconds = remaining % 60

        st.subheader(f"{st.session_state.timer_type} Session")

        st.title(f"{minutes:02d}:{seconds:02d}")

        if remaining == 0:

            st.session_state.timer_running = False

            if st.session_state.timer_type == "Study":
                st.success("🎉 Study session completed! Take a break.")
            else:
                st.success("Break completed! Ready to study again?")

        else:
            time.sleep(1)
            st.rerun()

    else:
        st.info("Choose your duration and start your session.")
