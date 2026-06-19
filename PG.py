import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. THE GAME DATASET (5 CYBERSECURITY SCENARIOS) ---
scenarios = [
    {
        "level": 1,
        "is_phishing": True,
        "sender_name": "PayPal Security Team",
        "sender_email": "alerts@paypaI-security.com",  # Look closely: Capital 'I' instead of 'l'
        "subject": "Security Alert: Unauthorized access detected",
        "body": "We detected suspicious login activity from an unknown IP address. To secure your funds, you must verify your identity within 1 hour or your account will be permanently locked.",
        "cta_text": "[ Secure My Account Now ]",
        "hidden_url": "http://paypaI-security.com/webscr/login",
        "clue": "Inspect the spelling of the sender's domain letter-by-letter, and look for an intense time limit.",
        "options": [
            "Typosquatting: The domain uses a capital 'I' instead of a lowercase 'l' (paypaI).",
            "The email uses a fake tracking number.",
            "The email asks you to download a malicious PDF invoice attachment."
        ],
        "correct_option_idx": 0,
        "explanation": "This is a classic Typosquatting attack. The attacker registered a domain name that looks identical to PayPal at a quick glance. They combine this with extreme time-based urgency (1 hour) to bypass your logical reasoning."
    },
    {
        "level": 2,
        "is_phishing": True,
        "sender_name": "Netflix Billing",
        "sender_email": "no-reply@services-netflix.com",
        "subject": "Action Required: Update your payment method",
        "body": "Your subscription could not be renewed because your financial institution rejected the automated charge. Click below to update your credit card credentials to avoid immediate service suspension.",
        "cta_text": "[ Update Billing Details ]",
        "hidden_url": "https://services-netflix.com/login/auth.php",
        "clue": "Check if Netflix utilizes generic external domains like 'services-netflix.com' for official billing updates.",
        "options": [
            "The email body contains grammatical mistakes.",
            "An external domain structure combined with a standard subscription-loss scare tactic.",
            "The email demands a direct cryptocurrency transaction."
        ],
        "correct_option_idx": 1,
        "explanation": "Attackers exploit services you use daily. Official updates come from 'netflix.com', not tracking subdomains like 'services-netflix.com'. This is designed to harvest credit card data."
    },
    {
        "level": 3,
        "is_phishing": True,
        "sender_name": "Office of the CEO",
        "sender_email": "ceo-office@company-urgent-request.com",
        "subject": "CONFIDENTIAL: Immediate assistance required",
        "body": "Likhith, I am currently in a highly confidential board meeting and cannot take calls. I need you to purchase 5 Apple Gift Cards ($100 each) for an executive client presentation right away. Email me the voucher codes directly. I will have HR reimburse you by tomorrow morning. Do not mention this to your team.",
        "cta_text": "[ View Presentation Details ]",
        "hidden_url": "http://company-urgent-request.com/ceo/memo",
        "clue": "Look at the combination of an external domain, an unusual command, and an explicit demand for secrecy.",
        "options": [
            "The email uses an attachment that triggers an immediate macro virus download.",
            "The email uses a lookalike website mimicking a bank portal login.",
            "An Authority-based Spearphishing play targeting an employee to bypass financial safeguards."
        ],
        "correct_option_idx": 2,
        "explanation": "This is Spearphishing leveraging the psychology of 'Authority.' Attackers impersonate senior executives using external lookalike domains to bypass normal corporate payment processes, demanding gift cards or wire transfers under the guise of confidentiality."
    },
    {
        "level": 4,
        "is_phishing": True,
        "sender_name": "IT Identity Access Management",
        "sender_email": "no-reply@verification-portal-okta.com",
        "subject": "CRITICAL: Multi-Factor Authentication (MFA) Reset",
        "body": "Our security team has initialized a mandatory synchronization protocol for all corporate Okta MFA profiles. Failure to re-authenticate your endpoint device within 12 hours will decouple your access keys from the corporate network framework.",
        "cta_text": "[ Sync MFA Token ]",
        "hidden_url": "https://verification-portal-okta.com/oauth2/sign-in",
        "clue": "Look at the destination URL. Does it belong to your official corporate identity portal domain?",
        "options": [
            "Credential Harvesting through a simulated identity provider portal (Okta mimicry).",
            "A standard malware delivery vector hidden inside an image file.",
            "An open-redirect exploit vulnerability bypassing standard browser headers."
        ],
        "correct_option_idx": 0,
        "explanation": "This is an advanced Credential Harvesting vector. By mimicking single sign-on providers like Okta, attackers capture both your primary passwords and secondary active MFA session tokens simultaneously using a reverse-proxy phishing framework."
    },
    {
        "level": 5,
        "is_phishing": True,
        "sender_name": "PyPI Package Security",
        "sender_email": "package-updates@pypi-security.org",
        "subject": "URGENT: Critical Zero-Day Vulnerability in PyTorch Library",
        "body": "A critical remote code execution (RCE) vulnerability has been identified within the foundational PyTorch wheel configuration files. All Data Science infrastructure environments must instantly force a manual patch deployment by running the terminal command: pip install torch-security-patch --index-url http://pypi-security.org/simple",
        "cta_text": "[ View Vulnerability CVE Report ]",
        "hidden_url": "http://pypi-security.org/cve/torch-patch",
        "clue": "Think like an offensive security analyst. Look closely at the custom registry URL parameter specified in the installation script command.",
        "options": [
            "A standard credit card scam disguised as a system optimization prompt.",
            "An adversarial Supply Chain Attack vector utilizing dependency confusion to inject backdoors into developer environments.",
            "A brute-force script designed to overwhelm internal database storage servers."
        ],
        "correct_option_idx": 1,
        "explanation": "This is a sophisticated Supply Chain Dependency Confusion attack. It explicitly targets technical developers and data scientists. By hosting a malicious package named 'torch-security-patch' on an external lookalike registry, the attacker forces your local terminal to pull a malicious exploit script into your secure network environment."
    }
]

df = pd.DataFrame(scenarios)

# --- 2. MULTI-LEVEL GAME STATE ENGINE ---
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = "briefing"  # 'briefing', 'playing', 'level_up', 'game_over'
if 'current_level' not in st.session_state:
    st.session_state.current_level = 1
if 'level_phase' not in st.session_state:
    st.session_state.level_phase = "classification"  # 'classification', 'identification', 'debrief'
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'level_points_potential' not in st.session_state:
    st.session_state.level_points_potential = 5
if 'clue_used_this_level' not in st.session_state:
    st.session_state.clue_used_this_level = False
if 'phase1_correct' not in st.session_state:
    st.session_state.phase1_correct = False

st.set_page_config(page_title="Inbox Defender Pro", layout="wide")

# --- STAGE 1: LEVEL 0 INTERACTIVE TRAINING (ZOOM ANIMATION) ---
if st.session_state.game_stage == "briefing":
    st.title("🛡️ Level 0: Cyber Intelligence Briefing")
    st.subheader("Use the Investigative Controls below to isolate threat vector markers.")
    
    # Custom HTML/CSS/JS for the Investigative Zoom Engine
    zoom_html = """
    <div style="font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; background-color: #0e1117; color: #ffffff; padding: 15px; border-radius: 8px;">
        
        <div style="display: flex; gap: 10px; margin-bottom: 20px; justify-content: center;">
            <button onclick="zoomTo('sender')" style="padding: 10px 14px; background-color: #262730; color: white; border: 1px solid #464855; border-radius: 4px; cursor: pointer; font-weight: bold;">🔍 1. Inspect Sender Domain</button>
            <button onclick="zoomTo('body')" style="padding: 10px 14px; background-color: #262730; color: white; border: 1px solid #464855; border-radius: 4px; cursor: pointer; font-weight: bold;">🧠 2. Analyze Emotional Tone</button>
            <button onclick="zoomTo('link')" style="padding: 10px 14px; background-color: #262730; color: white; border: 1px solid #464855; border-radius: 4px; cursor: pointer; font-weight: bold;">🔗 3. Examine Link Target</button>
            <button onclick="zoomTo('reset')" style="padding: 10px 14px; background-color: #ff4b4b; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">🔄 Reset Camera</button>
        </div>

        <div style="width: 100%; height: 240px; border: 2px solid #464855; border-radius: 6px; overflow: hidden; position: relative; background-color: #1a1c23;">
            <div id="emailCanvas" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; padding: 20px; box-sizing: border-box; transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1); transform-origin: top left;">
                
                <div id="senderSection" style="margin-bottom: 12px; padding: 4px; border-radius: 4px;">
                    <strong>From:</strong> Microsoft Security Alert <span style="color: #ff4b4b; background-color: rgba(255,75,75,0.1); padding: 2px 4px; border-radius: 3px;">admin@microsft-support-portal.com</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <strong>Subject:</strong> CRITICAL: Security perimeter breach identified!
                </div>
                <hr style="border: 0; border-top: 1px solid #464855; margin-bottom: 15px;">
                <div id="bodySection" style="margin-bottom: 15px; font-size: 14px; line-height: 1.4; padding: 4px; border-radius: 4px;">
                    Our database engine detected an illicit system entry configuration mismatch. You must re-authenticate your active workspace session <span style="color: #ff4b4b; font-weight: bold; text-decoration: underline;">within 15 minutes</span> or your deployment instance keys will be completely purged.
                </div>
                <div id="linkSection" style="display: inline-block; padding: 8px 16px; background-color: #262730; color: #00ff00; border: 1px solid #00ff00; font-family: monospace; font-size: 13px; border-radius: 4px;">
                    🔗 [ Re-Verify Session Token ]
                </div>
            </div>
        </div>

        <div id="analysisFeed" style="margin-top: 20px; padding: 15px; background-color: #1a1c23; border-left: 4px solid #00ff00; border-radius: 0 4px 4px 0; min-height: 80px;">
            <strong style="color: #00ff00;">Operational Radar Status:</strong> Select an analytical parameter indicator node above to initialize camera focus and threat deconstruction logs.
        </div>
    </div>

    <script>
        function zoomTo(target) {
            var canvas = document.getElementById('emailCanvas');
            var feed = document.getElementById('analysisFeed');
            
            // Reset borders
            document.getElementById('senderSection').style.border = "none";
            document.getElementById('bodySection').style.border = "none";
            document.getElementById('linkSection').style.border = "1px solid #00ff00";
            
            if (target === 'sender') {
                canvas.style.transform = "scale(1.5) translate(-10px, -10px)";
                document.getElementById('senderSection').style.border = "2px dashed #ff4b4b";
                feed.innerHTML = "<strong style='color: #ff4b4b;'>⚠️ DOMAIN DECONSTRUCTION LOG:</strong> Look closely at <code>microsft-support-portal.com</code>. The missing letter 'o' in 'microsoft' is an intentional Typosquatting trap. Attackers buy lookalike domains to slip past quick inspection routines.";
            } else if (target === 'body') {
                canvas.style.transform = "scale(1.4) translate(-20px, -40px)";
                document.getElementById('bodySection').style.border = "2px dashed #ff4b4b";
                feed.innerHTML = "<strong style='color: #ff4b4b;'>⚠️ PSYCHOLOGICAL PROFILE LOG:</strong> Notice the artificial deadline threat: <code>'within 15 minutes'</code>. Attackers utilize high panic and urgency triggers intentionally to cloud your technical troubleshooting frameworks and force errors.";
            } else if (target === 'link') {
                canvas.style.transform = "scale(1.6) translate(-20px, -85px)";
                document.getElementById('linkSection').style.border = "2px dashed #ff4b4b";
                feed.innerHTML = "<strong style='color: #00ff00;'>💡 HYPERLINK INTEGRITY LOG:</strong> While text anchors can read cleanly, hovering reveals the actual technical payload pointer routing vector. In the defense grid, never click links before verifying the underlying endpoint architecture.";
            } else {
                canvas.style.transform = "scale(1) translate(0px, 0px)";
                feed.innerHTML = "<strong style='color: #00ff00;'>Operational Radar Status:</strong> Interface frame camera configuration reset. System tracking normal.";
            }
        }
    </script>
    """
    
    components.html(zoom_html, height=560)
    
    st.write("---")
    if st.button("🚀 Initialization Complete: Launch Defensive Grid Matrix", type="primary", use_container_width=True):
        st.session_state.game_stage = "playing"
        st.session_state.current_level = 1
        st.session_state.level_phase = "classification"
        st.rerun()

# --- STAGE 2: LEVEL UP CELEBRATION MILESTONE ---
elif st.session_state.game_stage == "level_up":
    st.balloons()  # Visual celebration feedback trigger
    st.title("🌟 Level Clearance Confirmed!")
    
    # Calculate previous level completed
    prev_level = st.session_state.current_level - 1
    
    st.success(f"Congratulations! You have successfully neutralized all tactical vulnerabilities inside Level {prev_level}.")
    st.markdown(f"### Current Security Clearance Level Accountabilities: **{st.session_state.total_score} Points Accumulated**")
    st.info("The automated threat vectors will now elevate configuration tracking thresholds. Prepare for highly complex payloads.")
    
    next_btn_label = f"Unlock Level {st.session_state.current_level} Operations 🔓"
    if st.button(next_btn_label, type="primary", use_container_width=True):
        st.session_state.game_stage = "playing"
        st.session_state.level_phase = "classification"
        st.session_state.level_points_potential = 5
        st.session_state.clue_used_this_level = False
        st.session_state.phase1_correct = False
        st.rerun()

# --- STAGE 3: MULTI-LEVEL CORE GAME LOOP ---
elif st.session_state.game_stage == "playing":
    current_email = df[df['level'] == st.session_state.current_level].iloc[0]
    
    st.title(f"🎮 Level {st.session_state.current_level} / 5: Perimeter Defense Grid")
    
    # Telemetry HUD
    hud_col1, hud_col2, hud_col3 = st.columns(3)
    with hud_col1:
        st.metric("Total Cumulative Score", f"{st.session_state.total_score} pts")
    with hud_col2:
        st.metric("Current Level Max Value", f"{st.session_state.level_points_potential} / 5 pts")
    with hud_col3:
        status_label = "Active Assessment" if st.session_state.level_phase != "debrief" else "Analysis Mode"
        st.write(f"**System Status:** `{status_label}`")
        
    st.divider()
    
    col1, col2 = st.columns([1.6, 1.2])
    
    # LEFT PANEL: Interactive Simulated Email Node
    with col1:
        st.subheader("📩 Inbound Message Frame")
        with st.container(border=True):
            st.markdown(f"**Sender Identity:** `{current_email['sender_name']}`")
            st.markdown(f"**Sender Routing Address:** `<{current_email['sender_email']}>`")
            st.markdown(f"**Subject Line:** `{current_email['subject']}`")
            st.divider()
            st.write(current_email['body'])
            st.write("")
            
            hover_link = f"<a href='#' title='Inspection Engine URL Target Routing: {current_email['hidden_url']}' style='display:inline-block; padding:12px 24px; background-color:#1e1e1e; color:#00FF00; text-decoration:none; border-radius:4px; border: 1px solid #00FF00; font-family:monospace;'>🔗 {current_email['cta_text']}</a>"
            st.markdown(hover_link, unsafe_allow_html=True)
            st.caption("💡 SECURITY ENGINE ALERT: Hover cursor over link object to inspect real target routing metadata.")

    # RIGHT PANEL: Decision Architecture Panel
    with col2:
        st.subheader("🕹️ Analysis Control Console")
        
        # --- PHASE 1: BINARY CLASSIFICATION ---
        if st.session_state.level_phase == "classification":
            st.info("🎯 **Phase 1 Assessment:** Determine the structural authenticity of this payload.")
            
            if not st.session_state.clue_used_this_level:
                if st.button("🔍 Deploy Intelligence Clue (-1 Point Penalty)", use_container_width=True):
                    st.session_state.clue_used_this_level = True
                    st.session_state.level_points_potential -= 1
                    st.rerun()
            else:
                st.warning(f"💡 **Intelligence Data Feed:** {current_email['clue']}")
            
            st.write("---")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚨 QUARANTINE / REPORT", type="primary", use_container_width=True):
                    st.session_state.phase1_correct = current_email['is_phishing']
                    st.session_state.level_phase = "identification"
                    st.rerun()
            with c2:
                if st.button("✅ TRUST / AUTHORIZE", use_container_width=True):
                    st.session_state.phase1_correct = not current_email['is_phishing']
                    st.session_state.level_phase = "identification"
                    st.rerun()

        # --- PHASE 2: THREAT IDENTIFICATION ---
        elif st.session_state.level_phase == "identification":
            if st.session_state.phase1_correct:
                st.success("🎯 Phase 1 Match Verified! (+2 Points Earned)")
            else:
                st.error("❌ Phase 1 Match Failed! (0 Points Allocated)")
                
            st.write("---")
            st.info("🎯 **Phase 2 Assessment:** Isolate the exact active flaw signature inside this payload module to score remaining point fields.")
            
            selected_option = st.radio(
                "Identify primary threat signature parameter vector configuration:",
                options=current_email['options'],
                index=0
            )
            
            if st.button("Submit Structural Analysis Data", use_container_width=True, type="primary"):
                selected_idx = current_email['options'].index(selected_option)
                
                points_scored = 0
                if st.session_state.phase1_correct:
                    points_scored += 2
                if selected_idx == current_email['correct_option_idx']:
                    points_scored += 3
                    
                if st.session_state.clue_used_this_level:
                    points_final = min(points_scored, st.session_state.level_points_potential)
                else:
                    points_final = points_scored
                    
                st.session_state.total_score += points_final
                st.session_state.level_phase = "debrief"
                st.rerun()

        # --- PHASE 3: METRIC DEBRIEF AND STATE ROUTING ---
        elif st.session_state.level_phase == "debrief":
            st.subheader("📊 Incident Resolution Breakdown Log")
            st.warning(f"**Threat Signature Parameters:** {current_email['explanation']}")
            
            st.write("---")
            if st.session_state.current_level < 5:
                if st.button("Proceed to Milestone Validation Verification Matrix ➡️", use_container_width=True, type="primary"):
                    st.session_state.current_level += 1
                    st.session_state.game_stage = "level_up"  # Direct to Level Up celebration state
                    st.rerun()
            else:
                if st.button("Compile Deployment Telemetry Output 🏆", use_container_width=True, type="primary"):
                    st.session_state.game_stage = "game_over"
                    st.rerun()

# --- STAGE 4: GRADUATION AND ANALYTICS LOGS ---
elif st.session_state.game_stage == "game_over":
    st.title("🏆 Deployment Evaluation Complete")
    st.subheader("System Perimeter Audit Infrastructure Analysis")
    
    max_total_possible = 25
    accuracy_percentage = int((st.session_state.total_score / max_total_possible) * 100)
    
    col_score, col_status = st.columns(2)
    with col_score:
        st.metric(label="Defensive Security Metric Value", value=f"{st.session_state.total_score} / {max_total_possible} Points", delta=f"{accuracy_percentage}% Accuracy Profile")
    with col_status:
        if accuracy_percentage == 100:
            st.success("Rank Assigned: Tier 3 Elite Incident Responder")
        elif accuracy_percentage >= 80:
            st.success("Rank Assigned: Security Operations Center Analyst Tier 1")
        elif accuracy_percentage >= 60:
            st.warning("Rank Assigned: Systems Operator Perimeter Assistant")
        else:
            st.error("Rank Assigned: Mandatory Red Team Remediations Protocol Triggered")
            
    st.write("---")
    st.markdown("""
    ### 🛡️ Post-Deployment Capability Metrics Breakdown
    * **Visual Threat Validation Modules:** Evaluates rapid mitigation tracking workflows across character swaps and domain structures.
    * **Behavioral Countermeasures Matrix:** Evaluates response validation structures against trust profiles and urgency exploits.
    * **Reverse Proxy Detection Engines:** Focuses on tracking parameters deployed by modern proxy collection frames mimicking identity provider points.
    * **Supply Chain Dependency Vulnerability Analysis:** Focuses on evaluation loops managing pipeline registries and configuration terminal calls.
    """)
    
    if st.button("Flush Cache Parameters and Re-Initialize Defense Environment"):
        st.session_state.game_stage = "briefing"
        st.session_state.current_level = 1
        st.session_state.level_phase = "classification"
        st.session_state.total_score = 0
        st.session_state.level_points_potential = 5
        st.session_state.clue_used_this_level = False
        st.session_state.phase1_correct = False
        st.rerun()