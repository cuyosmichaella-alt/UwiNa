import streamlit as st
from datetime import datetime, time, timedelta

st.set_page_config(
    page_title="UwiNa — Reassurance Without Surveillance",
    page_icon="🟢",
    layout="centered",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F7FBFA 0%, #EEF7F5 100%);
    }
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(135deg, #0F766E, #14B8A6);
        color: white;
        padding: 28px;
        border-radius: 24px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(15,118,110,.18);
    }
    .hero h1 { margin: 0; font-size: 2.3rem; }
    .hero p { margin: 8px 0 0; opacity: .92; font-size: 1.05rem; }
    .card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        margin: 12px 0;
        border: 1px solid #DDEDEA;
        box-shadow: 0 5px 18px rgba(15,118,110,.07);
    }
    .status {
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        margin: 12px 0;
        font-size: 1.05rem;
    }
    .green { background:#E8F7EF; border:1px solid #B9E4CB; color:#166534; }
    .yellow { background:#FFF8DF; border:1px solid #F4D98A; color:#854D0E; }
    .orange { background:#FFF0DD; border:1px solid #F4C58A; color:#9A3412; }
    .red { background:#FDECEC; border:1px solid #F2B8B8; color:#991B1B; }
    .privacy {
        background:#F0FDFA;
        border-left:5px solid #14B8A6;
        padding:14px 16px;
        border-radius:10px;
        margin:12px 0;
    }
    .small { color:#64748B; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
defaults = {
    "plan": None,
    "status": "green",
    "reason": "Your outing is on plan.",
    "history": [],
    "show_help": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🟢 UwiNa</h1>
    <p><b>Reassurance without surveillance.</b><br>
    Let them know you're okay — without showing them everywhere you go.</p>
</div>
""", unsafe_allow_html=True)

st.caption("A prototype of a privacy-first outing safety system.")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🔐 Privacy Controls")
    st.write("UwiNa follows a **minimum necessary disclosure** approach.")
    st.write("Your exact location is **not automatically shared**.")
    st.divider()
    st.write("**Disclosure ladder**")
    st.write("🟢 Level 0 — Status only")
    st.write("🟡 Level 1 — Confirmation needed")
    st.write("🟠 Level 2 — Plan changed")
    st.write("🔴 Level 3 — Safety unconfirmed")
    st.write("🚨 Level 4 — User requests help")
    st.divider()
    if st.button("↩️ Reset prototype", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

# ---------- Main ----------
tab1, tab2, tab3 = st.tabs(["📝 Safety Plan", "📊 My Status", "👨‍👩‍👧 Family View"])

with tab1:
    st.subheader("Create a Safety Plan")
    st.write("Instead of sharing your live location, tell UwiNa what your outing is supposed to look like.")

    with st.form("plan_form"):
        destination = st.text_input("📍 Destination", placeholder="e.g., SM North EDSA")
        return_time = st.time_input("🏠 Expected return time", value=time(22, 0))
        transport = st.selectbox(
            "🚌 Transportation",
            ["Commute", "Private vehicle", "Ride-hailing", "Walking", "Other"]
        )
        contact = st.text_input("👤 Family contact", value="Mom")
        st.write("**Safety conditions**")
        update_change = st.checkbox("Ask me to confirm if my plans change", value=True)
        late_check = st.checkbox("Ask me to confirm if I am significantly late", value=True)
        low_battery = st.checkbox("Warn me if my battery may not last until my return time", value=True)
        escalation = st.checkbox("Allow escalation after repeated missed confirmations", value=True)

        submitted = st.form_submit_button("🔒 Create Safety Plan", use_container_width=True)

    if submitted:
        if not destination.strip():
            st.error("Please enter a destination.")
        else:
            st.session_state.plan = {
                "destination": destination.strip(),
                "return_time": return_time.strftime("%I:%M %p"),
                "transport": transport,
                "contact": contact.strip() or "Family",
                "update_change": update_change,
                "late_check": late_check,
                "low_battery": low_battery,
                "escalation": escalation,
            }
            st.session_state.status = "green"
            st.session_state.reason = "Your outing is on plan."
            st.session_state.history = ["Safety plan created."]
            st.success("Safety plan created. Your family does not receive your exact location.")

    if st.session_state.plan:
        p = st.session_state.plan
        st.markdown("### Current plan")
        st.markdown(f"""
        <div class="card">
            <b>📍 Destination:</b> {p["destination"]}<br>
            <b>🏠 Expected return:</b> {p["return_time"]}<br>
            <b>🚌 Transportation:</b> {p["transport"]}<br>
            <b>👤 Family contact:</b> {p["contact"]}
        </div>
        """, unsafe_allow_html=True)

with tab2:
    if not st.session_state.plan:
        st.info("Create a Safety Plan first.")
    else:
        status = st.session_state.status
        labels = {
            "green": ("🟢", "You're okay", "green"),
            "yellow": ("🟡", "Confirmation needed", "yellow"),
            "orange": ("🟠", "Plan changed", "orange"),
            "red": ("🔴", "Safety unconfirmed", "red"),
            "emergency": ("🚨", "HELP MODE ACTIVE", "red"),
        }
        icon, title, css = labels[status]

        st.markdown(
            f'<div class="status {css}"><div style="font-size:2rem">{icon}</div>'
            f'<b style="font-size:1.35rem">{title}</b><br>{st.session_state.reason}</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="privacy">
        <b>🔐 Privacy check:</b> Exact location is NOT being shared.
        UwiNa is communicating your <b>safety status</b>, not continuously tracking you.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🎮 Simulate an outing")
        c1, c2 = st.columns(2)

        with c1:
            if st.button("🟢 Everything is on plan", use_container_width=True):
                st.session_state.status = "green"
                st.session_state.reason = "Your outing is on plan."
                st.session_state.history.append("User confirmed: everything is on plan.")
                st.rerun()

            if st.button("🟡 Plans changed", use_container_width=True):
                st.session_state.status = "yellow"
                st.session_state.reason = "Your plans appear to have changed. Please confirm you're okay."
                st.session_state.history.append("System detected a possible plan change.")
                st.rerun()

            if st.button("🟠 Low battery warning", use_container_width=True):
                st.session_state.status = "orange"
                st.session_state.reason = "Battery may not last until the expected return time."
                st.session_state.history.append("System detected a low-battery risk.")
                st.rerun()

        with c2:
            if st.button("🔴 Missed confirmations", use_container_width=True):
                st.session_state.status = "red"
                st.session_state.reason = "UwiNa could not confirm your safety after repeated missed confirmations."
                st.session_state.history.append("Repeated confirmations were missed.")
                st.rerun()

            if st.button("🚨 I NEED HELP", use_container_width=True):
                st.session_state.status = "emergency"
                st.session_state.reason = "You requested help. Your chosen emergency information can now be disclosed."
                st.session_state.history.append("USER REQUESTED HELP.")
                st.rerun()

        st.divider()
        st.subheader("Respond to the alert")

        if status == "yellow":
            a, b, c = st.columns(3)
            with a:
                if st.button("✅ I'm okay"):
                    st.session_state.status = "green"
                    st.session_state.reason = "You confirmed that you're okay."
                    st.session_state.history.append("User confirmed safety.")
                    st.rerun()
            with b:
                if st.button("✏️ Update plan"):
                    st.session_state.status = "orange"
                    st.session_state.reason = "Plan updated. Family receives the updated safety status, not your live location."
                    st.session_state.history.append("User updated the outing plan.")
                    st.rerun()
            with c:
                if st.button("🚨 Need help"):
                    st.session_state.status = "emergency"
                    st.session_state.reason = "You requested help."
                    st.session_state.history.append("User requested help.")
                    st.rerun()

        if status in ["red", "emergency"]:
            st.warning("UwiNa has reached a higher disclosure level.")
            st.write("Choose what information may be shared:")
            share = st.radio(
                "Disclosure option",
                ["Status only", "General area (approximate)", "Exact location"],
                index=0,
            )
            st.info(f"Selected disclosure: **{share}**")
            if st.button("↩️ Confirm I'm safe"):
                st.session_state.status = "green"
                st.session_state.reason = "You confirmed you're safe."
                st.session_state.history.append(f"User confirmed safety; disclosure selected: {share}.")
                st.rerun()

        st.divider()
        st.subheader("🧾 Activity history")
        for item in reversed(st.session_state.history[-6:]):
            st.write("• " + item)

with tab3:
    if not st.session_state.plan:
        st.info("Create a Safety Plan first.")
    else:
        p = st.session_state.plan
        status = st.session_state.status

        status_info = {
            "green": ("🟢", "You're okay", "Your outing is going according to plan.", "green"),
            "yellow": ("🟡", "Confirmation needed", "UwiNa needs you to confirm your safety.", "yellow"),
            "orange": ("🟠", "Plan changed", "The outing plan has changed.", "orange"),
            "red": ("🔴", "Safety unconfirmed", "UwiNa could not confirm your safety.", "red"),
            "emergency": ("🚨", "HELP MODE ACTIVE", "The user requested help.", "red"),
        }
        icon, title, message, css = status_info[status]

        # App-style family header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg,#0F766E,#14B8A6);
            color:white;
            padding:22px 24px;
            border-radius:22px 22px 0 0;
            margin-top:10px;">
            <div style="font-size:.82rem;opacity:.85;letter-spacing:1px;">UWINA FAMILY</div>
            <div style="font-size:1.65rem;font-weight:700;">Family Safety Dashboard</div>
            <div style="opacity:.9;">Reassurance, without continuous tracking.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background:white;
            padding:22px;
            border:1px solid #DDEDEA;
            border-top:0;
            box-shadow:0 8px 25px rgba(15,118,110,.08);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-size:.8rem;color:#64748B;">SAFETY STATUS</div>
                    <div style="font-size:1.55rem;font-weight:700;">{icon} {title}</div>
                </div>
                <div style="text-align:right;color:#64748B;font-size:.85rem;">
                    Last update<br><b>Just now</b>
                </div>
            </div>
            <hr style="border:none;border-top:1px solid #E2E8F0;">
            <div style="font-size:1rem;"><b>{message}</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Trip card
        st.markdown(f"""
        <div class="card">
            <div class="small">CURRENT OUTING</div>
            <h3 style="margin:5px 0 15px;">📍 {p["destination"]}</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div style="background:#F8FAFC;padding:12px;border-radius:12px;">
                    <div class="small">EXPECTED RETURN</div>
                    <b>🏠 {p["return_time"]}</b>
                </div>
                <div style="background:#F8FAFC;padding:12px;border-radius:12px;">
                    <div class="small">TRANSPORT</div>
                    <b>🚌 {p["transport"]}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # The key differentiator
        st.markdown("""
        <div class="privacy" style="margin-top:18px;">
        <div style="font-size:1.05rem;"><b>🔐 Privacy-first update</b></div>
        <div style="margin-top:7px;">
        You are receiving a <b>safety status</b>, not a live location.
        </div>
        <div style="margin-top:10px;font-size:.9rem;">
        ✅ Safety status &nbsp;&nbsp; ✅ Plan status &nbsp;&nbsp; ❌ Live GPS &nbsp;&nbsp; ❌ Location history
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Disclosure level
        level_map = {
            "green": ("Level 0", "Status only"),
            "yellow": ("Level 1", "Confirmation needed"),
            "orange": ("Level 2", "Plan changed"),
            "red": ("Level 3", "Safety unconfirmed"),
            "emergency": ("Level 4", "User requested help"),
        }
        level, level_desc = level_map[status]

        st.markdown(f"""
        <div class="card">
            <div class="small">PRIVACY LADDER</div>
            <h3 style="margin:5px 0;">{level}</h3>
            <div>{level_desc}</div>
            <div style="margin-top:12px;background:#E2E8F0;height:8px;border-radius:10px;">
                <div style="width:{(int(level.split()[1])/4)*100 if level.split()[1].isdigit() else 100}%;
                background:#14B8A6;height:8px;border-radius:10px;"></div>
            </div>
            <div class="small" style="margin-top:8px;">
                UwiNa reveals only the minimum information needed for the current safety concern.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if status in ["red", "emergency"]:
            st.warning("⚠️ A higher safety level has been reached.")
            st.write("The user's pre-set disclosure rules determine what additional information can be shared.")
            share = st.radio(
                "What information is currently permitted?",
                ["Status only", "General area (approximate)", "Exact location"],
                index=0,
                key="family_disclosure",
            )
            st.info(f"Current permitted disclosure: **{share}**")

        st.markdown("""
        <div class="card">
            <div class="small">WHAT WOULD YOU RECEIVE?</div>
            <p style="margin-bottom:8px;">Instead of:</p>
            <div style="color:#991B1B;">❌ “Here is their exact location.”</div>
            <p style="margin:12px 0 8px;">UwiNa provides:</p>
            <div style="color:#166534;">✅ “They are okay.”</div>
            <div style="color:#854D0E;">🟡 “Their plans changed. Confirmation is needed.”</div>
            <div style="color:#9A3412;">🟠 “Their plan was updated.”</div>
            <div style="color:#991B1B;">🔴 “Their safety could not be confirmed.”</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("Demo only — UwiNa does not send real notifications or contact emergency services.")

st.divider()
st.caption("UwiNa is an academic prototype for an STS project. It does not provide real emergency services or real GPS tracking.")
