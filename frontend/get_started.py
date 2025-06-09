import re
from datetime import datetime

import bleach
import streamlit as st
from backend.workspace import (
    initialize,
    is_workspace_initialized,
    save_workspace,
    workspace_file_exists,
)

# File paths and URLs for resources
GETTING_STARTED_DIAG_PATH = "assets/getting_started_diag.png"
TESTING_FRAMEWORK_FILE_URL_EXCEL = "https://go.gov.sg/aivtf-excel"


def click_back_button() -> None:
    """
    Decrement the 'section' in the session state to navigate to the previous section.

    Returns:
        None
    """
    st.session_state["section"] -= 1


def click_next_button() -> None:
    """
    Display a dialog for creating a new workspace.

    Presents a modal form for users to name their workspace and explains
    the features of workspaces. The function handles form submission,
    input validation, and workspace initialization.

    Returns:
        None
    """

    # Using st.dialog as a function decorator
    @st.dialog("Provide Workspace Details")
    def name_your_workspace_dialog() -> None:
        # Input field for company name
        company_name = st.text_input(  # noqa: E501
            "Company Name",
            key="company_name",
            placeholder="e.g., Bank ABC",
            help="The name of the company will be reflected in the report generated after you complete the process checks and technical tests (optional)",  # noqa: E501
            max_chars=50,
        )

        # Input field for app name
        app_name = st.text_input(
            "Application Name",
            key="app_name",
            placeholder="e.g., Chatbot A",
            help="The name of the application will be reflected in the report generated after you complete the process checks and technical tests (optional)",  # noqa: E501
            max_chars=50,
        )

        # Input field for app description
        app_description = st.text_area(  # noqa: E501
            "Application Description",
            key="app_description",
            placeholder="e.g., Chatbot A is an internal facing chatbot used by employees to extract and summarise policies and publications by Bank ABC. The goal is to provide relationship managers with quick accurate summaries of relevant documents, saving time and improving service quality.",  # noqa: E501
            help="Briefly describe the application being assessed, including its purpose, key features, and any relevant context. This will help provide a clearer understanding of the application for your stakeholders reading the report",  # noqa: E501
            max_chars=256,
            height=150,
        )

        # Disable resizing of text area with custom CSS
        st.markdown(
            """
            <style>
                textarea {
                    resize: none !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Input field for workspace name
        workspace_name = st.text_input(
            "Workspace Name",
            key="workspace_name",
            placeholder="e.g., Chatbot A version 1",
            help="Enter a unique name that you can easily find and resume later",
            max_chars=50,
        )

        # Handle form submission
        if st.button("Continue", type="primary", use_container_width=True):
            # Sanitize file name using bleach
            stripped_workspace_name = workspace_name.strip()
            sanitized_file_name = bleach.clean(stripped_workspace_name, strip=True)
            # Replace spaces with hyphens and remove remaining special characters
            sanitized_file_name = re.sub(r"[^\w\-]", "-", sanitized_file_name).strip(
                "-"
            )

            # Sanitize company name using bleach
            stripped_company_name = company_name.strip()
            sanitized_company_name = bleach.clean(stripped_company_name, strip=True)

            # Sanitize app name using bleach
            stripped_app_name = app_name.strip()
            sanitized_app_name = bleach.clean(stripped_app_name, strip=True)

            # Sanitize app description using bleach
            stripped_app_description = app_description.strip()
            sanitized_app_description = bleach.clean(
                stripped_app_description, strip=True
            )

            # Check all required fields and display a combined error if needed
            missing_fields = []
            if not sanitized_file_name:
                missing_fields.append("workspace name")
            if not sanitized_company_name:
                missing_fields.append("company name")
            if not sanitized_app_name:
                missing_fields.append("application name")
            if not sanitized_app_description:
                missing_fields.append("application description")

            if missing_fields:
                st.error(f"Please enter a {', '.join(missing_fields)} to continue.")

            if (
                sanitized_file_name
                and sanitized_company_name
                and sanitized_app_name
                and sanitized_app_description
            ):
                # Check if the workspace file already exists
                if workspace_file_exists(sanitized_file_name):
                    st.error(
                        "A workspace with this name already exists. Please choose a different name."
                    )
                else:
                    # Use the sanitized file name as the Workspace ID
                    workspace_id = sanitized_file_name

                    # Create workspace data dictionary with metadata
                    workspace_data = {
                        "workspace_id": sanitized_file_name,
                        "created_at": datetime.now().isoformat(timespec="seconds"),
                        "last_updated": datetime.now().isoformat(timespec="seconds"),
                        "company_name": sanitized_company_name,
                        "app_name": sanitized_app_name,
                        "app_description": sanitized_app_description,
                    }

                    # Initialize workspace with metadata and save it to persistent storage
                    initialize(workspace_id, workspace_data)
                    save_workspace(workspace_id, workspace_data)

                    # Increment the section state
                    st.session_state["section"] += 1
                    st.rerun()

    # Call the dialog function to display it
    if is_workspace_initialized():
        st.session_state["section"] += 1
    else:
        name_your_workspace_dialog()


def click_start_over_button() -> None:
    """
    Return to the home page by clearing the session state.

    Displays a confirmation dialog before returning to the home page.
    Progress is automatically saved, so no data will be lost.

    Returns:
        None
    """

    # Using st.dialog as a function decorator
    @st.dialog("Return to Home Page")
    def confirm_reset_dialog() -> None:
        st.write(
            "Do you want to return to Home Page? Don't worry, your progress has been saved."
        )
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, start over", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        with col2:
            if st.button("No, cancel", use_container_width=True):
                st.rerun()

    # Call the dialog function to display it
    confirm_reset_dialog()


def display_getting_started() -> None:
    """
    Display the 'Getting Started' page for the application.

    Shows instructions on understanding the testing framework, beginning process checks,
    uploading technical test results, and generating a report.

    Returns:
        None
    """
    # Add custom CSS for purple headers
    st.markdown(
        """
        <style>
        h3 {
            color: #4C1D95 !important;  /* Purple color */
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.write(
        """
        ### Understand the testing framework
        The framework consists of 11 principles.
        Each principle has desired outcomes that can be achieved through specified testing processes.
        The implementation of these processes can be validated through documentary evidence.
    """
    )
    st.image(GETTING_STARTED_DIAG_PATH)
    st.info(
        f"""
        You can download a copy of the testing framework here\n
        Download Testing Framework - PDF\n
        [Download Testing Framework - Excel]({TESTING_FRAMEWORK_FILE_URL_EXCEL})
    """
    )

    st.write(
        """
        ### Begin the Process Checks
        - Familiarise yourself with the testing framework: principles, desired outcomes and testing processes 
        - For each process, select one of the following options: Yes, No or Not Applicable

            **1. Yes:** If the process is implemented, you can provide supporting evidence

            **2. No:** If the process is not implemented, provide reasons to show that the decision is a deliberate and considered one
            
            **3. Not Applicable:** If the process does not apply to your application, you can provide reasons to show that the decision is a deliberate and considered one

        ### Upload Technical Tests Results (Optional):
        If you wish to include results from technical tests conducted using Project Moonshot, you can upload the results in **Section 4 (Upload Technical Test Results)** of this tool.
        Reports generated after uploading technical test results will include both process checks and technical test outcomes.
        
        
        If you do not have any technical test results from Project Moonshot, you can skip this section without concern.
        The generated report will still provide valuable insights based on the process checks.

        ### Generate and Use the Report
        - Once all process checks are completed and technical tests results uploaded (if applicable), you can generate a summary report
        - Use this report to identify areas for improvement, demonstrate responsible AI practices, and build trust with your stakeholders
    """  # noqa: E501, W291, W293
    )


def display_navigation_buttons() -> None:
    """
    Display navigation buttons for moving between sections of the process checks.

    Shows Back, Start Over, and Next buttons as appropriate based on the current section.
    Only displays navigation controls when the user has progressed beyond the triage section.
    The Next button is always displayed for sections 1-4 when appropriate.

    Returns:
        None
    """
    if st.session_state["section"] >= 1:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("---")

    # Regular navigation buttons
    col1, _, col2, col3 = st.columns([2, 6, 2, 2])
    with col1:
        if st.session_state["section"] >= 1:
            st.button(
                ":material/home: Home",
                on_click=click_start_over_button,
                use_container_width=True,
            )
    with col2:
        if st.session_state["section"] > 1:
            st.button("← Back", on_click=click_back_button, use_container_width=True)
    with col3:
        # Display the Next button for sections 1-4
        if st.session_state["section"] < 5 and st.session_state["section"] >= 1:
            st.button(
                "Next →",
                on_click=click_next_button,
                use_container_width=True,
            )


def getting_started() -> None:
    """
    Display the 'Getting Started' page and navigation buttons.

    Calls display_getting_started to show the content and display_navigation_buttons
    to display navigation controls.

    Returns:
        None
    """
    display_getting_started()

    # Display the navigation buttons
    display_navigation_buttons()
