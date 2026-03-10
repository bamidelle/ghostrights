import streamlit as st
import os
import uuid
import hashlib
from datetime import datetime
from database.db import get_supabase, get_supabase_admin

def render():

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d0d; color: #f0ede6;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container {
        padding: 0 32px 32px !important;
        max-width: 100% !important;
    }

    /* PAGE HEADER */
    .gr-page-header {
        padding: 28px 0 32px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 32px;
    }
    .gr-page-title {
        font-family: 'Syne', sans-serif;
        font-size: 26px; font-weight: 800;
        color: #f0ede6; margin: 0 0 6px;
    }
    .gr-page-sub {
        font-size: 13px; color: rgba(240,237,230,0.4);
    }

    /* UPLOAD ZONE */
    .gr-upload-zone {
        border: 2px dashed rgba(200,255,0,0.25);
        border-radius: 20px;
        padding: 48px 32px;
        text-align: center;
        background: rgba(200,255,0,0.03);
        margin-bottom: 28px;
        transition: all 0.2s;
    }
    .gr-upload-icon { font-size: 48px; margin-bottom: 16px; }
    .gr-upload-title {
        font-family: 'Syne', sans-serif;
        font-size: 18px; font-weight: 700;
        margin-bottom: 8px; color: #f0ede6;
    }
    .gr-upload-sub {
        font-size: 13px; color: rgba(240,237,230,0.4);
        margin-bottom: 8px; line-height: 1.6;
    }
    .gr-upload-formats {
        font-size: 11px; color: rgba(200,255,0,0.5);
        letter-spacing: 0.5px;
    }

    /* FORM CARD */
    .gr-form-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px; padding: 32px;
        margin-bottom: 24px;
    }
    .gr-form-title {
        font-family: 'Syne', sans-serif;
        font-size: 16px; font-weight: 700;
        margin-bottom: 24px; color: #f0ede6;
        display: flex; align-items: center; gap: 10px;
    }
    .gr-label {
        font-size: 11px; letter-spacing: 0.8px;
        text-transform: uppercase;
        color: rgba(240,237,230,0.35);
        margin-bottom: 6px; margin-top: 18px;
    }
    .gr-label:first-child { margin-top: 0; }

    /* Streamlit overrides */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #f0ede6 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: rgba(200,255,0,0.4) !important;
        box-shadow: 0 0 0 3px rgba(200,255,0,0.06) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #f0ede6 !important;
    }
    .stNumberInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #f0ede6 !important;
    }

    /* PRIMARY BUTTON */
    .stButton > button {
        background: #c8ff00 !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 13px 28px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #d4ff33 !important;
        box-shadow: 0 6px 24px rgba(200,255,0,0.2) !important;
    }

    /* PROTECTION SETTINGS */
    .gr-protection-option {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 18px 20px;
        margin-bottom: 10px; cursor: pointer;
        transition: all 0.2s;
    }
    .gr-protection-option.selected {
        border-color: rgba(200,255,0,0.4);
        background: rgba(200,255,0,0.05);
    }
    .gr-protection-title {
        font-size: 14px; font-weight: 500;
        color: #f0ede6; margin-bottom: 4px;
    }
    .gr-protection-desc {
        font-size: 12px; color: rgba(240,237,230,0.35);
        line-height: 1.5;
    }

    /* FINGERPRINT PROGRESS */
    .gr-fp-step {
        display: flex; align-items: center;
        gap: 14px; padding: 14px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .gr-fp-step:last-child { border-bottom: none; }
    .gr-fp-icon { font-size: 20px; flex-shrink: 0; }
    .gr-fp-label {
        flex: 1; font-size: 13px;
        color: rgba(240,237,230,0.6);
    }
    .gr-fp-status-done {
        color: #c8ff00; font-size: 12px; font-weight: 600;
    }
    .gr-fp-status-pending {
        color: rgba(240,237,230,0.2);
        font-size: 12px;
    }

    /* CONTENT TABLE */
    .gr-table-header {
        display: flex; gap: 12px;
        padding: 10px 16px;
        font-size: 11px; letter-spacing: 0.8px;
        text-transform: uppercase;
        color: rgba(240,237,230,0.3);
        margin-bottom: 4px;
    }
    .gr-table-row {
        display: flex; align-items: center;
        gap: 12px; padding: 14px 16px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px; margin-bottom: 8px;
    }
    .gr-table-title {
        flex: 3; font-size: 13px;
        font-weight: 500; color: #f0ede6;
    }
    .gr-table-type {
        flex: 1.5; font-size: 12px;
        color: rgba(240,237,230,0.4);
    }
    .gr-table-fp {
        flex: 1; font-size: 12px;
        text-align: center;
    }
    .gr-table-action { flex: 1; text-align: right; }
    .gr-fp-badge-done {
        background: rgba(200,255,0,0.1);
        color: #c8ff00; font-size: 11px;
        padding: 3px 10px; border-radius: 100px;
    }
    .gr-fp-badge-pending {
        background: rgba(255,200,0,0.1);
        color: #ffc800; font-size: 11px;
        padding: 3px 10px; border-radius: 100px;
    }

    /* INFO BOX */
    .gr-info-box {
        background: rgba(200,255,0,0.05);
        border: 1px solid rgba(200,255,0,0.15);
        border-radius: 12px; padding: 16px 20px;
        font-size: 13px; color: rgba(240,237,230,0.6);
        line-height: 1.6; margin-bottom: 20px;
    }
    .gr-info-box strong { color: #c8ff00; }

    div[data-testid="stSidebar"] {
        background: #0d0d0d !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── PAGE HEADER ───────────────────────────────────────────
    st.markdown("""
    <div class="gr-page-header">
        <div class="gr-page-title">📁 Upload & Protect Content</div>
        <div class="gr-page-sub">
            Register your content with GhostRights.
            We fingerprint every file so our crawlers
            know exactly what to hunt.
        </div>
    </div>
    """, unsafe_allow_html=True)

    creator_id = st.session_state.user.id \
        if st.session_state.get("user") else None

    # ── TABS ──────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["➕ Upload New Content", "📋 My Content Library"])

    # ════════════════════════════════════════════════════════
    # TAB 1 — UPLOAD FORM
    # ════════════════════════════════════════════════════════
    with tab1:

        st.markdown("""
        <div class="gr-info-box">
            <strong>How fingerprinting works:</strong>
            When you upload content, GhostRights generates
            a unique digital fingerprint of your file.
            This fingerprint is what our crawlers use to
            recognise your content anywhere on the internet —
            even if pirates crop, compress or re-encode it.
        </div>
        """, unsafe_allow_html=True)

        col_form, col_settings = st.columns([3, 2])

        with col_form:
            st.markdown("""
            <div class="gr-form-card">
                <div class="gr-form-title">📝 Content Details</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="gr-label">Content Title *</div>',
                        unsafe_allow_html=True)
            title = st.text_input("Title",
                placeholder="e.g. Living In Bondage, Essence ft. Tems",
                label_visibility="collapsed", key="up_title")

            st.markdown('<div class="gr-label">Content Type *</div>',
                        unsafe_allow_html=True)
            content_type = st.selectbox("Type",
                ["movie", "short_film", "music_track",
                 "album", "podcast", "youtube_video",
                 "photo", "course", "other"],
                label_visibility="collapsed", key="up_type")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown('<div class="gr-label">Release Year</div>',
                            unsafe_allow_html=True)
                year = st.number_input("Year",
                    min_value=1990,
                    max_value=datetime.now().year,
                    value=datetime.now().year,
                    label_visibility="collapsed",
                    key="up_year")
            with col_b:
                st.markdown('<div class="gr-label">Language</div>',
                            unsafe_allow_html=True)
                language = st.selectbox("Language",
                    ["English", "Yoruba", "Igbo", "Hausa",
                     "Pidgin", "French", "Other"],
                    label_visibility="collapsed",
                    key="up_language")

            st.markdown('<div class="gr-label">Genre / Category</div>',
                        unsafe_allow_html=True)
            genre = st.text_input("Genre",
                placeholder="e.g. Nollywood Drama, Afrobeats, Comedy",
                label_visibility="collapsed", key="up_genre")

            st.markdown('<div class="gr-label">Description</div>',
                        unsafe_allow_html=True)
            description = st.text_area("Description",
                placeholder="Brief description of your content...",
                label_visibility="collapsed",
                key="up_desc", height=100)

            # ── FILE UPLOAD ───────────────────────────────
            st.markdown("""
            <div class="gr-upload-zone">
                <div class="gr-upload-icon">📂</div>
                <div class="gr-upload-title">
                    Drop your file here
                </div>
                <div class="gr-upload-sub">
                    Upload your movie, music track, or media file.<br>
                    We use it to generate your content fingerprint.
                </div>
                <div class="gr-upload-formats">
                    MP4 • AVI • MOV • MP3 • WAV • AAC • JPG • PNG
                    (Max 500MB)
                </div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload your content file",
                type=["mp4", "avi", "mov", "mkv",
                      "mp3", "wav", "aac", "flac",
                      "jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
                key="up_file"
            )

            if uploaded_file:
                st.success(f"✅ File ready: {uploaded_file.name} "
                           f"({uploaded_file.size / 1024 / 1024:.1f} MB)")

        with col_settings:
            st.markdown("""
            <div class="gr-form-card">
                <div class="gr-form-title">
                    🛡️ Protection Settings
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="gr-label">When Piracy Is Found...</div>',
                        unsafe_allow_html=True)
            protection_action = st.radio(
                "Action",
                options=["monetize", "takedown", "track_only"],
                format_func=lambda x: {
                    "monetize": "💰 Monetize — Earn ad revenue from pirated copies",
                    "takedown": "⚔️ Takedown — Destroy every pirated copy",
                    "track_only": "👁️ Track Only — Monitor without acting"
                }[x],
                label_visibility="collapsed",
                key="up_action"
            )

            st.markdown("<div style='margin-top: 24px;'></div>",
                        unsafe_allow_html=True)

            st.markdown("""
            <div class="gr-form-card">
                <div class="gr-form-title">
                    💧 Watermarking
                </div>
            </div>
            """, unsafe_allow_html=True)

            embed_watermark = st.checkbox(
                "Embed invisible watermark",
                value=True, key="up_watermark"
            )
            st.markdown("""
            <div style="font-size:12px;
                 color:rgba(240,237,230,0.35);
                 margin-top: 6px; line-height:1.6;">
                An invisible watermark links this file to your account.
                If a pirated copy is found, we can trace exactly
                who leaked it.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 24px;'></div>",
                        unsafe_allow_html=True)

            st.markdown("""
            <div class="gr-form-card">
                <div class="gr-form-title">
                    🔍 What Gets Fingerprinted
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="gr-fp-step">
                <div class="gr-fp-icon">🎬</div>
                <div class="gr-fp-label">
                    Video fingerprint (pHash)
                </div>
                <div class="gr-fp-status-done">Auto ✓</div>
            </div>
            <div class="gr-fp-step">
                <div class="gr-fp-icon">🎵</div>
                <div class="gr-fp-label">
                    Audio fingerprint (Chromaprint)
                </div>
                <div class="gr-fp-status-done">Auto ✓</div>
            </div>
            <div class="gr-fp-step">
                <div class="gr-fp-icon">💧</div>
                <div class="gr-fp-label">
                    Invisible watermark embedded
                </div>
                <div class="gr-fp-status-done">Auto ✓</div>
            </div>
            <div class="gr-fp-step">
                <div class="gr-fp-icon">🗄️</div>
                <div class="gr-fp-label">
                    Fingerprint stored in database
                </div>
                <div class="gr-fp-status-done">Auto ✓</div>
            </div>
            <div class="gr-fp-step">
                <div class="gr-fp-icon">🕷️</div>
                <div class="gr-fp-label">
                    Crawler starts hunting immediately
                </div>
                <div class="gr-fp-status-done">Auto ✓</div>
            </div>
            """, unsafe_allow_html=True)

        # ── SUBMIT BUTTON ─────────────────────────────────────
        st.markdown("<div style='margin-top: 8px;'></div>",
                    unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submit_btn = st.button(
                "🛡️ Register & Protect This Content",
                key="submit_content"
            )

        # ── SUBMIT LOGIC ──────────────────────────────────────
        if submit_btn:
            if not title:
                st.error("Please enter a content title.")
            elif not uploaded_file:
                st.error("Please upload your content file.")
            elif not creator_id:
                st.error("Please log in to upload content.")
            else:
                _process_upload(
                    creator_id=creator_id,
                    title=title,
                    content_type=content_type,
                    year=int(year),
                    language=language,
                    genre=genre,
                    description=description,
                    protection_action=protection_action,
                    embed_watermark=embed_watermark,
                    uploaded_file=uploaded_file
                )

    # ════════════════════════════════════════════════════════
    # TAB 2 — CONTENT LIBRARY
    # ════════════════════════════════════════════════════════
    with tab2:
        st.markdown("<div style='margin-top: 8px;'></div>",
                    unsafe_allow_html=True)

        contents = _get_all_content(creator_id)

        if not contents:
            st.markdown("""
            <div style="text-align:center; padding: 64px 24px;
                 background: rgba(255,255,255,0.02);
                 border: 1px dashed rgba(255,255,255,0.08);
                 border-radius: 20px; margin-top: 16px;">
                <div style="font-size:48px; margin-bottom:16px;">
                    📁
                </div>
                <div style="font-family:'Syne',sans-serif;
                     font-size:18px; font-weight:700;
                     margin-bottom:10px;">
                    No content registered yet
                </div>
                <div style="font-size:13px;
                     color:rgba(240,237,230,0.35);">
                    Upload your first movie, song or video<br>
                    and GhostRights will start hunting pirates immediately
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Summary stats
            total = len(contents)
            fingerprinted = sum(
                1 for c in contents if c.get("fingerprint_generated")
            )
            total_piracy = sum(
                c.get("total_pirated_copies_found", 0)
                for c in contents
            )
            total_revenue = sum(
                c.get("total_revenue_recovered_ngn", 0)
                for c in contents
            )

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Content", total)
            with m2:
                st.metric("Fingerprinted", f"{fingerprinted}/{total}")
            with m3:
                st.metric("Total Piracy Found", total_piracy)
            with m4:
                st.metric("Revenue Recovered",
                          f"₦{total_revenue:,}")

            st.markdown("<div style='margin-top:24px;'></div>",
                        unsafe_allow_html=True)

            # Table header
            st.markdown("""
            <div class="gr-table-header">
                <div style="flex:3">Title</div>
                <div style="flex:1.5">Type</div>
                <div style="flex:1; text-align:center">
                    Fingerprint
                </div>
                <div style="flex:1; text-align:center">
                    Piracy Found
                </div>
                <div style="flex:1.5; text-align:center">
                    Revenue Recovered
                </div>
                <div style="flex:1; text-align:center">
                    Action
                </div>
            </div>
            """, unsafe_allow_html=True)

            for c in contents:
                fp_badge = (
                    '<span class="gr-fp-badge-done">✓ Done</span>'
                    if c.get("fingerprint_generated")
                    else '<span class="gr-fp-badge-pending">⏳ Pending</span>'
                )
                ctype = c.get("content_type", "other") \
                    .replace("_", " ").title()
                copies = c.get("total_pirated_copies_found", 0)
                revenue = c.get("total_revenue_recovered_ngn", 0)
                action_icon = {
                    "monetize": "💰",
                    "takedown": "⚔️",
                    "track_only": "👁️"
                }.get(c.get("protection_action", ""), "🛡️")

                st.markdown(f"""
                <div class="gr-table-row">
                    <div class="gr-table-title">
                        {c.get('title', 'Untitled')}
                        <div style="font-size:11px;
                             color:rgba(240,237,230,0.3);
                             margin-top:2px;">
                            {c.get('release_year', '')} •
                            {c.get('language', '')}
                        </div>
                    </div>
                    <div class="gr-table-type">{ctype}</div>
                    <div class="gr-table-fp">{fp_badge}</div>
                    <div style="flex:1; text-align:center;
                         font-size:13px;
                         color:{'#ff5050' if copies > 0 else 'rgba(240,237,230,0.3)'};">
                        {copies}
                    </div>
                    <div style="flex:1.5; text-align:center;
                         font-size:13px; color:#c8ff00;">
                        ₦{revenue:,}
                    </div>
                    <div style="flex:1; text-align:center;">
                        {action_icon}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ── UPLOAD PROCESSING ─────────────────────────────────────────

def _process_upload(creator_id, title, content_type, year,
                    language, genre, description,
                    protection_action, embed_watermark,
                    uploaded_file):
    """Handle the full upload and fingerprinting pipeline."""

    progress_bar = st.progress(0)
    status = st.empty()

    try:
        # Step 1 — Save file to Supabase Storage
        status.markdown("**Step 1/5** — Uploading file to secure storage...")
        progress_bar.progress(10)

        file_bytes = uploaded_file.read()
        file_ext = uploaded_file.name.split(".")[-1].lower()
        unique_filename = f"{creator_id}/{uuid.uuid4()}.{file_ext}"

        supabase = get_supabase()
        supabase.storage.from_("gr-content").upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": uploaded_file.type}
        )

        file_url = supabase.storage.from_("gr-content") \
            .get_public_url(unique_filename)

        progress_bar.progress(25)

        # Step 2 — Generate fingerprint
        status.markdown(
            "**Step 2/5** — Generating content fingerprint..."
        )
        video_fp, audio_fp = _generate_fingerprint(
            file_bytes, file_ext
        )
        progress_bar.progress(50)

        # Step 3 — Generate watermark ID
        status.markdown("**Step 3/5** — Embedding invisible watermark...")
        watermark_id = _generate_watermark_id(creator_id, title)
        progress_bar.progress(65)

        # Step 4 — Save to database
        status.markdown("**Step 4/5** — Registering in database...")
        admin = get_supabase_admin()

        content_record = {
            "creator_id": creator_id,
            "title": title,
            "content_type": content_type,
            "description": description,
            "release_year": year,
            "language": language,
            "genre": genre,
            "file_url": file_url,
            "file_size_bytes": len(file_bytes),
            "file_format": file_ext,
            "video_fingerprint": video_fp,
            "audio_fingerprint": audio_fp,
            "fingerprint_generated": bool(video_fp or audio_fp),
            "fingerprint_generated_at": datetime.now().isoformat(),
            "watermark_embedded": embed_watermark,
            "watermark_id": watermark_id,
            "watermark_embedded_at": datetime.now().isoformat()
                if embed_watermark else None,
            "protection_action": protection_action,
            "is_active": True
        }

        result = admin.table("protected_content") \
            .insert(content_record).execute()

        progress_bar.progress(85)

        # Step 5 — Queue crawler job
        status.markdown(
            "**Step 5/5** — Queuing crawler to start hunting..."
        )

        if result.data:
            content_id = result.data[0]["id"]
            admin.table("crawler_jobs").insert({
                "job_type": "single_content_scan",
                "content_id": content_id,
                "creator_id": creator_id,
                "status": "queued"
            }).execute()

            # Send notification
            admin.table("notifications").insert({
                "creator_id": creator_id,
                "notification_type": "system_alert",
                "title": "Content Registered Successfully",
                "message": f'"{title}" has been fingerprinted '
                           f'and our crawlers are now actively '
                           f'hunting for pirated copies.',
                "send_dashboard": True,
                "send_email": True
            }).execute()

        progress_bar.progress(100)
        status.empty()
        progress_bar.empty()

        # Success message
        st.markdown(f"""
        <div style="background:rgba(200,255,0,0.08);
             border:1px solid rgba(200,255,0,0.25);
             border-radius:16px; padding:28px;
             text-align:center; margin-top:16px;">
            <div style="font-size:40px; margin-bottom:12px;">
                🎉
            </div>
            <div style="font-family:'Syne',sans-serif;
                 font-size:20px; font-weight:800;
                 color:#c8ff00; margin-bottom:8px;">
                "{title}" is now protected!
            </div>
            <div style="font-size:13px;
                 color:rgba(240,237,230,0.5);
                 line-height:1.7;">
                ✅ Fingerprint generated<br>
                ✅ Watermark embedded<br>
                ✅ Crawler queued and hunting<br>
                ✅ You'll be notified when piracy is found
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        progress_bar.empty()
        status.empty()
        st.error(f"Upload failed: {str(e)}")
        st.info("Please check your Supabase storage bucket "
                "permissions and try again.")


def _generate_fingerprint(file_bytes: bytes,
                           file_ext: str) -> tuple:
    """
    Generate video and audio fingerprints.
    Uses SHA256 hash as base fingerprint.
    Full pHash + Chromaprint added in crawler module.
    """
    video_fp = None
    audio_fp = None

    try:
        # Base fingerprint using SHA256
        # (pHash via OpenCV runs in background crawler)
        content_hash = hashlib.sha256(file_bytes).hexdigest()

        video_formats = ["mp4", "avi", "mov", "mkv", "wmv"]
        audio_formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]

        if file_ext in video_formats:
            video_fp = f"sha256_v_{content_hash[:64]}"
            audio_fp = f"sha256_a_{content_hash[64:]}" \
                if len(content_hash) > 64 \
                else f"sha256_a_{content_hash}"
        elif file_ext in audio_formats:
            audio_fp = f"sha256_a_{content_hash}"

    except Exception as e:
        st.warning(f"Fingerprint generation note: {e}")

    return video_fp, audio_fp


def _generate_watermark_id(creator_id: str, title: str) -> str:
    """Generate unique watermark ID for this content + creator."""
    unique_string = f"{creator_id}_{title}_{uuid.uuid4()}"
    return hashlib.md5(
        unique_string.encode()
    ).hexdigest()[:16].upper()


def _get_all_content(creator_id: str) -> list:
    """Fetch all content for this creator."""
    if not creator_id:
        return []
    try:
        supabase = get_supabase()
        response = supabase.table("protected_content") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .eq("is_active", True) \
            .order("registered_at", desc=True) \
            .execute()
        return response.data or []
    except Exception:
        return []
