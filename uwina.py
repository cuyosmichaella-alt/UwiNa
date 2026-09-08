
import streamlit as st
from datetime import time

# ============================================================
# UwiNa
# Reassurance Without Surveillance
# STS Module Exam 1 - Individual Prototype
# ============================================================

st.set_page_config(
    page_title="UwiNa",
    page_icon="🏠",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main-title {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        color: #666666;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    .status-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin: 10px 0px;
        text-align: center;
    }

    .green-status {
        background-color: #eaf7ea;
        border: 1px solid #9bd49b;
    }

    .yellow-status {
        background-color: #fff8dc;
        border: 1px solid #e4cf65;
    }

    .red-status {
        background-color: #fdecec;
        border: 1px solid #e0a0a0;
    }

    .privacy-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #f4f4f4;
        margin: 15px 0px;
    }

    .small-text {
        color: #666666;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "outing_started": False,
    "status": "setup",
    "destination": "",
    "departure": time(17, 0),
    "return_time": time(22, 0),
    "transportation": "Commute",
    "family_contact": "",
    "new_destination": "",
    "check_in_count": 0,
    "last_action": "",
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_app():

    for key, value in defaults.items():
        st.session_state[key] = value

    st.rerun()


def start_outing():

    st.session_state.outing_started = True
    st.session_state.status = "normal"
    st.session_state.last_action = "Outing started."


def simulate_change():

    st.session_state.status = "check_in"
    st.session_state.last_action = "Unexpected change detected."


def confirm_safe():

    st.session_state.status = "safe"
    st.session_state.check_in_count = 0
    st.session_state.last_action = "User confirmed that they are safe."


def update_plan():

    st.session_state.destination = st.session_state.new_destination
    st.session_state.status = "updated"
    st.session_state.check_in_count = 0
    st.session_state.last_action = "User updated their outing plan."


def request_help():

    st.session_state.status = "emergency"
    st.session_state.last_action = "User requested help."


def simulate_missed_checkin():

    st.session_state.check_in_count += 1

    if st.session_state.check_in_count >= 2:

        st.session_state.status = "emergency"
        st.session_state.last_action = (
            "Multiple check-ins were missed."
        )

    else:

        st.session_state.status = "check_in"
        st.session_state.last_action = (
            "First check-in was missed."
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏠 UwiNa</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Reassurance without surveillance.</div>',
    unsafe_allow_html=True
)

st.write(
    "UwiNa helps families know when reassurance may be needed "
    "without requiring continuous location tracking."
)

st.divider()


# ============================================================
# SETUP SCREEN
# ============================================================

if st.session_state.status == "setup":

    st.header("📍 Create Your Outing")

    st.write(
        "Tell UwiNa what your expected plans are before you leave."
    )

    destination = st.text_input(
        "Where are you going?",
        placeholder="Example: SM North"
    )

    departure = st.time_input(
        "Expected departure",
        value=time(17, 0)
    )

    return_time = st.time_input(
        "Expected return",
        value=time(22, 0)
    )

    transportation = st.selectbox(
        "How are you getting there?",
        [
            "Commute",
            "Private vehicle",
            "Ride-hailing",
            "Walking",
            "Other"
        ]
    )

    family_contact = st.text_input(
        "Family contact",
        placeholder="Example: Mom"
    )

    st.divider()

    if st.button(
        "🚀 Start Outing",
        use_container_width=True,
        type="primary"
    ):

        if destination.strip() == "":
            st.warning("Please enter your destination.")

        elif family_contact.strip() == "":
            st.warning("Please enter a family contact.")

        else:

            st.session_state.destination = destination
            st.session_state.departure = departure
            st.session_state.return_time = return_time
            st.session_state.transportation = transportation
            st.session_state.family_contact = family_contact

            start_outing()

            st.rerun()


# ============================================================
# ACTIVE OUTING
# ============================================================

else:

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.header("⚙️ UwiNa Controls")

        st.write(
            "These controls simulate situations for the prototype."
        )

        st.divider()

        st.caption("Demo scenarios")

        if st.button(
            "🟢 Normal",
            use_container_width=True
        ):

            st.session_state.status = "normal"
            st.session_state.last_action = "Normal outing."

            st.rerun()

        if st.button(
            "🟡 Unexpected Change",
            use_container_width=True
        ):

            simulate_change()

            st.rerun()

        if st.button(
            "🔴 Simulate Missed Check-ins",
            use_container_width=True
        ):

            simulate_missed_checkin()

            st.rerun()

        st.divider()

        if st.button(
            "🔄 Reset Prototype",
            use_container_width=True
        ):

            reset_app()


    # ========================================================
    # OUTING INFORMATION
    # ========================================================

    st.header("📋 Your Outing")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📍 Destination",
            st.session_state.destination
        )

    with col2:

        st.metric(
            "🚗 Transportation",
            st.session_state.transportation
        )

    col3, col4 = st.columns(2)

    with col3:

        st.write("🕐 **Departure**")

        st.write(
            st.session_state.departure.strftime("%I:%M %p")
        )

    with col4:

        st.write("🏠 **Expected Return**")

        st.write(
            st.session_state.return_time.strftime("%I:%M %p")
        )

    st.divider()


    # ========================================================
    # NORMAL STATUS
    # ========================================================

    if st.session_state.status == "normal":

        st.markdown(
            """
            <div class="status-card green-status">

            <h2>🟢 Everything is Normal</h2>

            <p>You are following your planned outing.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "UwiNa does not need to constantly track your exact location."
        )

        st.divider()

        st.subheader("👨‍👩‍👧 Family Reassurance")

        st.info(
            f"**{st.session_state.family_contact}** can see that "
            "your outing is proceeding normally."
        )

        st.write(
            "Status: 🟢 Safe — Following planned outing"
        )

        st.divider()

        st.subheader("🧪 Demonstrate the Invention")

        st.write(
            "For this prototype, simulate an unexpected change "
            "to show how UwiNa responds."
        )

        if st.button(
            "⚠️ Simulate Unexpected Change",
            use_container_width=True,
            type="primary"
        ):

            simulate_change()

            st.rerun()


    # ========================================================
    # CHECK-IN
    # ========================================================

    elif st.session_state.status == "check_in":

        st.markdown(
            """
            <div class="status-card yellow-status">

            <h2>🟡 Check-in Requested</h2>

            <p>Something appears to be different from your planned outing.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "Your plans appear to have changed."
        )

        st.write(
            "UwiNa is checking in because your current situation "
            "does not match the plan you provided."
        )

        st.warning(
            "Are you okay?"
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "✅ I'm Okay",
                use_container_width=True
            ):

                confirm_safe()

                st.rerun()

        with col2:

            if st.button(
                "🔄 Update Plans",
                use_container_width=True
            ):

                st.session_state.status = "update"

                st.rerun()

        with col3:

            if st.button(
                "🆘 I Need Help",
                use_container_width=True
            ):

                request_help()

                st.rerun()

        st.divider()

        st.subheader("👨‍👩‍👧 Family View")

        st.write(
            f"🟡 **{st.session_state.family_contact}** "
            "has been informed that a check-in is needed."
        )

        st.caption(
            "The system asks the user first instead of immediately "
            "sharing their exact location."
        )


    # ========================================================
    # SAFE CONFIRMATION
    # ========================================================

    elif st.session_state.status == "safe":

        st.markdown(
            """
            <div class="status-card green-status">

            <h2>🟢 You're Safe</h2>

            <p>You confirmed that everything is okay.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Your family has been reassured."
        )

        st.write(
            f"**Family notification:** "
            f"{st.session_state.family_contact} knows that you are safe."
        )

        st.divider()

        st.subheader("🔐 Privacy")

        st.markdown(
            """
            <div class="privacy-box">

            UwiNa focuses on your <b>safety status</b>, not
            continuously displaying your exact location.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        if st.button(
            "⚠️ Simulate Another Change",
            use_container_width=True
        ):

            simulate_change()

            st.rerun()


    # ========================================================
    # UPDATE PLAN
    # ========================================================

    elif st.session_state.status == "update":

        st.header("🔄 Update Your Plans")

        st.write(
            "Plans can change. UwiNa allows you to update them "
            "instead of treating every change as an emergency."
        )

        new_destination = st.text_input(
            "New destination",
            value=st.session_state.destination
        )

        new_return = st.time_input(
            "New expected return",
            value=st.session_state.return_time
        )

        st.divider()

        if st.button(
            "💾 Save New Plan",
            use_container_width=True,
            type="primary"
        ):

            if new_destination.strip() == "":

                st.warning("Please enter a destination.")

            else:

                st.session_state.new_destination = new_destination
                st.session_state.return_time = new_return

                update_plan()

                st.rerun()


    # ========================================================
    # UPDATED PLAN
    # ========================================================

    elif st.session_state.status == "updated":

        st.markdown(
            """
            <div class="status-card green-status">

            <h2>🟢 Plan Updated</h2>

            <p>Your family has been reassured.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "Your new outing information has been recorded."
        )

        st.write(
            f"📍 **New destination:** "
            f"{st.session_state.destination}"
        )

        st.write(
            f"🏠 **New expected return:** "
            f"{st.session_state.return_time.strftime('%I:%M %p')}"
        )

        st.success(
            f"{st.session_state.family_contact} has been reassured "
            "that your plans changed."
        )

        st.divider()

        st.subheader("🔐 Privacy Reminder")

        st.info(
            "The goal is to communicate a safety status "
            "without requiring continuous location sharing."
        )

        st.divider()

        if st.button(
            "🔴 Simulate Missed Check-ins",
            use_container_width=True
        ):

            st.session_state.check_in_count = 0

            simulate_missed_checkin()

            st.rerun()


    # ========================================================
    # EMERGENCY
    # ========================================================

    elif st.session_state.status == "emergency":

        st.markdown(
            """
            <div class="status-card red-status">

            <h2>🔴 Possible Emergency</h2>

            <p>UwiNa recommends contacting the user's family contact.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.error(
            "UwiNa could not receive confirmation after "
            "multiple unusual conditions."
        )

        st.write(
            f"**Recommended action:** Contact "
            f"{st.session_state.family_contact}."
        )

        st.divider()

        st.subheader("Why did UwiNa escalate?")

        st.write(
            "The system does not treat one unexpected change "
            "as an emergency."
        )

        st.write(
            "Escalation occurs only after the system cannot "
            "receive confirmation from the user."
        )

        st.divider()

        st.subheader("👨‍👩‍👧 Family View")

        st.warning(
            f"{st.session_state.family_contact}: "
            "UwiNa recommends checking on the user."
        )

        st.divider()

        if st.button(
            "✅ User Confirmed Safe",
            use_container_width=True
        ):

            confirm_safe()

            st.rerun()


# ============================================================
# PRIVACY / STS SECTION
# ============================================================

st.divider()

with st.expander("🔐 Why UwiNa is different"):

    st.write(
        "Traditional location-sharing systems focus on answering:"
    )

    st.markdown(
        "**“Where is this person right now?”**"
    )

    st.write(
        "UwiNa focuses on a different question:"
    )

    st.markdown(
        "**“Is everything going according to the plan we agreed on?”**"
    )

    st.write(
        "This creates a balance between safety, family reassurance, "
        "privacy, and personal independence."
    )


with st.expander("🧠 UwiNa's Core Mechanism"):

    st.write(
        "Expected Plan"
    )

    st.write("↓")

    st.write(
        "Detect Deviation"
    )

    st.write("↓")

    st.write(
        "Ask User"
    )

    st.write("↓")

    st.write(
        "Update Status"
    )

    st.write("↓")

    st.write(
        "Escalate Only When Necessary"
    )


with st.expander("🎓 STS Connection"):

    st.write(
        "UwiNa explores how technology can improve safety while "
        "respecting privacy and personal independence."
    )

    st.write(
        "The invention raises an important Science, Technology, "
        "and Society question:"
    )

    st.markdown(
        "**“How can technology provide safety without turning "
        "care into surveillance?”**"
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "UwiNa Prototype • GED 104: Science, Technology, and Society"
)
