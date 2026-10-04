import streamlit as st

from pdf_processor import extract_text_from_pdf
from agent import analyze_document, verify_documents


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="DocFlow AI",
    page_icon="📄",
    layout="wide"
)


# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("📄 DocFlow AI")

st.subheader(
    "Autonomous Document Workflow Agent"
)

st.write(
    "Upload a document and DocFlow AI will understand it, "
    "identify requirements, verify supporting documents, "
    "and create an actionable workflow."
)


# -------------------------------------------------
# MAIN DOCUMENT
# -------------------------------------------------

st.header("1️⃣ Upload Requirement Document")

uploaded_file = st.file_uploader(
    "Upload scholarship notice, internship notice, "
    "application form, hackathon brief, etc.",
    type=["pdf"],
    key="main_document"
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button("🔍 Extract Document"):

        with st.spinner("Reading document..."):

            text = extract_text_from_pdf(
                uploaded_file
            )

        if text.strip():

            st.success(
                "Document extracted successfully!"
            )

            st.session_state[
                "document_text"
            ] = text

        else:

            st.warning(
                "No text could be extracted from this PDF."
            )


# -------------------------------------------------
# SHOW EXTRACTED DOCUMENT
# -------------------------------------------------

if "document_text" in st.session_state:

    text = st.session_state["document_text"]

    with st.expander(
        "📄 View extracted document"
    ):

        st.text_area(
            "Extracted text",
            text,
            height=300
        )


# -------------------------------------------------
# AI ANALYSIS
# -------------------------------------------------

if "document_text" in st.session_state:

    st.divider()

    st.header("2️⃣ AI Document Analysis")

    if st.button(
        "🧠 Analyze Requirement Document"
    ):

        with st.spinner(
            "DocFlow AI is analyzing the document..."
        ):

            analysis = analyze_document(
                st.session_state["document_text"]
            )

        if "error" not in analysis:

            st.session_state[
                "analysis"
            ] = analysis

            st.success(
                "Analysis completed!"
            )

        else:

            st.error(
                analysis["error"]
            )

            st.code(
                analysis["raw_response"]
            )


# -------------------------------------------------
# WORKFLOW DASHBOARD
# -------------------------------------------------

if "analysis" in st.session_state:

    analysis = st.session_state["analysis"]

    st.divider()

    st.header(
        "3️⃣ 📊 Workflow Dashboard"
    )


    # -------------------------------------------------
    # DOCUMENT INFORMATION
    # -------------------------------------------------

    st.subheader(
        "📄 Document Information"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Document Type",
            analysis["document_type"]
        )

    with col2:

        st.metric(
            "Priority",
            analysis["priority"]
        )

    with col3:

        st.metric(
            "Deadline",
            analysis["deadline"]
        )

    with col4:

        st.metric(
            "Status",
            "Analyzed"
        )


    st.info(
        analysis["purpose"]
    )


    # -------------------------------------------------
    # ELIGIBILITY
    # -------------------------------------------------

    st.subheader(
        "🎯 Eligibility"
    )

    for item in analysis.get(
        "eligibility",
        []
    ):

        st.write(
            "✅",
            item
        )


    # -------------------------------------------------
    # REQUIRED DOCUMENTS
    # -------------------------------------------------

    st.subheader(
        "📋 Required Documents"
    )

    required_documents = analysis.get(
        "required_documents",
        []
    )

    for item in required_documents:

        st.write(
            "•",
            item
        )


    # -------------------------------------------------
    # SUPPORTING DOCUMENT UPLOAD
    # -------------------------------------------------

    st.divider()

    st.header(
        "4️⃣ 📂 Upload Your Supporting Documents"
    )

    st.write(
        "Upload the documents you already have. "
        "DocFlow AI will automatically identify and "
        "match them against the requirements."
    )

    supporting_files = st.file_uploader(
        "Upload supporting PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key="supporting_documents"
    )


    # -------------------------------------------------
    # VERIFY DOCUMENTS
    # -------------------------------------------------

    if supporting_files:

        st.write(
            f"📁 {len(supporting_files)} "
            f"document(s) uploaded."
        )

        if st.button(
            "🤖 Verify Supporting Documents"
        ):

            documents = []

            progress = st.progress(0)

            for index, file in enumerate(
                supporting_files
            ):

                with st.spinner(
                    f"Reading {file.name}..."
                ):

                    extracted_text = (
                        extract_text_from_pdf(
                            file
                        )
                    )

                documents.append(
                    {
                        "name": file.name,
                        "text": extracted_text
                    }
                )

                progress.progress(
                    (index + 1)
                    / len(supporting_files)
                )


            with st.spinner(
                "AI is matching documents with requirements..."
            ):

                verification = verify_documents(
                    required_documents,
                    documents
                )


            if "error" not in verification:

                st.session_state[
                    "verification"
                ] = verification

                st.success(
                    "Document verification completed!"
                )

            else:

                st.error(
                    verification["error"]
                )

                st.code(
                    verification["raw_response"]
                )


# -------------------------------------------------
# VERIFICATION RESULTS
# -------------------------------------------------

if "verification" in st.session_state:

    verification = st.session_state[
        "verification"
    ]

    st.divider()

    st.header(
        "5️⃣ 🔍 Document Verification"
    )


    # -------------------------------------------------
    # VERIFIED
    # -------------------------------------------------

    st.subheader(
        "✅ Verified Documents"
    )

    verified = verification.get(
        "verified_documents",
        []
    )

    if verified:

        for item in verified:

            st.success(
                f"{item['required_document']}  "
                f"← {item['uploaded_file']}  "
                f"({item['confidence']}% confidence)"
            )

            st.caption(
                item["reason"]
            )

    else:

        st.info(
            "No required documents were verified."
        )


    # -------------------------------------------------
    # MISSING
    # -------------------------------------------------

    st.subheader(
        "❌ Missing Documents"
    )

    missing = verification.get(
        "missing_documents",
        []
    )

    if missing:

        for item in missing:

            st.error(
                f"Missing: {item}"
            )

    else:

        st.success(
            "🎉 No missing documents detected!"
        )


    # -------------------------------------------------
    # UNCLEAR
    # -------------------------------------------------

    unclear = verification.get(
        "unclear_documents",
        []
    )

    if unclear:

        st.subheader(
            "⚠️ Documents Requiring Review"
        )

        for item in unclear:

            st.warning(
                f"{item['uploaded_file']} "
                f"→ {item['possible_type']} "
                f"({item['confidence']}%)"
            )

            st.caption(
                item["reason"]
            )


    # -------------------------------------------------
    # AGENT NEXT ACTION
    # -------------------------------------------------

    st.divider()

    st.header(
        "🤖 Agent Recommendation"
    )

    st.info(
        verification.get(
            "next_action",
            "Review the document status."
        )
    )


    # -------------------------------------------------
    # ACTION PLAN
    # -------------------------------------------------

    st.header(
        "6️⃣ ⚡ Action Plan"
    )

    actions = analysis.get(
        "recommended_actions",
        []
    )

    completed = 0

    for index, action in enumerate(
        actions
    ):

        if st.checkbox(
            action,
            key=f"workflow_action_{index}"
        ):

            completed += 1


    total = len(actions)


    if total > 0:

        progress = completed / total

        st.progress(
            progress
        )

        st.write(
            f"**{completed} / {total} "
            f"tasks completed**"
        )


   # -------------------------------------------------
# HUMAN APPROVAL
# -------------------------------------------------

st.divider()

st.header("7️⃣ 👤 Human Approval")

st.write(
    "The AI has analyzed the requirement and "
    "verified the uploaded documents. Review the "
    "results before starting the workflow."
)

approval = st.checkbox(
    "I have reviewed the AI-generated workflow."
)

if approval:

    st.success("✅ Workflow approved.")

    if st.button(
        "🚀 Start Workflow",
        type="primary"
    ):

        st.session_state["workflow_started"] = True

        st.session_state["agent_activity"] = [
            "Requirement document analyzed",
            f"{len(required_documents)} requirements identified",
            f"{len(verified)} supporting documents verified",
            f"{len(missing)} missing requirements detected",
            "Document requirements prioritized",
            "Human approval received",
            "Workflow execution started"
        ]

        st.balloons()

        st.success(
            "🚀 DocFlow workflow started successfully!"
        )

else:

    st.warning(
        "Human approval is required."
    )


# -------------------------------------------------
# AGENT ACTIVITY
# -------------------------------------------------

if st.session_state.get(
    "workflow_started",
    False
):

    st.divider()

    st.header("8️⃣ 🤖 Agent Activity")

    st.write(
        "Live execution history of the DocFlow agent."
    )

    for activity in st.session_state[
        "agent_activity"
    ]:

        st.success(
            "✓ " + activity
        )


# -------------------------------------------------
# WORKFLOW EXECUTION
# -------------------------------------------------

if st.session_state.get(
    "workflow_started",
    False
):

    st.divider()

    st.header(
        "9️⃣ 🚀 Workflow Execution"
    )

    if missing:

        st.subheader(
            "⚠️ Pending Requirements"
        )

        for item in missing:

            st.warning(
                f"Action required: {item}"
            )

        st.info(
            "🤖 Next Agent Action: "
            f"Resolve the highest-priority missing "
            f"requirement — {missing[0]}."
        )

    else:

        st.success(
            "🎉 All required documents are verified. "
            "The workflow is ready for submission."
        )


    st.subheader(
        "📋 Workflow Status"
    )

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:

        st.metric(
            "Verified",
            len(verified)
        )

    with status_col2:

        st.metric(
            "Missing",
            len(missing)
        )

    with status_col3:

        st.metric(
            "Workflow",
            "ACTIVE"
        )