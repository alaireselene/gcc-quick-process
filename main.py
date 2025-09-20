import streamlit as st
import pandas as pd

from process.ai_essential import process_gcc_usage_report
from process.specialization import process_gcc_specialization_file

def join_and_analyze_tables(usage_df, spec_df):
    """
    Join the filtered tables and analyze unique learners
    """
    try:
        st.markdown("---")
        st.header("Step 2: Combined Analysis")

        # Create Table 1: Filtered AI Essentials (Name, Email, Course)
        table1 = None
        if usage_df is not None:
            filtered_usage = usage_df.copy()

            # Apply filters
            if 'Course' in filtered_usage.columns:
                filtered_usage = filtered_usage[filtered_usage['Course'] == 'Google AI Essentials']

            # We will use unified 'Completion Time' for downstream logic
            # Ensure 'Completion Time' exists (AI Essentials already has it)

            if 'Completed' in filtered_usage.columns:
                filtered_usage = filtered_usage[filtered_usage['Completed'] == 'Yes']

            # Create Table 1 with Name, Email, Course/Specs (with completion date), Completion Time
            if len(filtered_usage) > 0:
                # Build Course/Specs with appended completion date if available
                if 'Course' in filtered_usage.columns:
                    course_specs = filtered_usage['Course'].astype(str)
                    # Use unified 'Completion Time'
                    comp = pd.to_datetime(filtered_usage.get('Completion Time'), errors='coerce', utc=True)
                    comp_str = comp.dt.strftime('%d/%m/%Y')
                    comp_str = comp_str.where(comp.notna(), '')
                    course_specs = course_specs + comp_str.apply(lambda s: f" ({s})" if s else "")
                    filtered_usage['Course/Specs'] = course_specs
                # Carry unified 'Completion Time'
                cols1 = [c for c in ['Name', 'Email', 'Course/Specs', 'Completion Time'] if c in filtered_usage.columns]
                table1 = filtered_usage[cols1].copy()

        # Create Table 2: Filtered Specialization (Name, Email, Specialization)
        table2 = None
        if spec_df is not None:
            filtered_spec = spec_df.copy()

            # Map Specialization Completion Time -> Completion Time
            if 'Specialization Completion Time' in filtered_spec.columns:
                filtered_spec['Completion Time'] = filtered_spec['Specialization Completion Time']

            if 'Completed' in filtered_spec.columns:
                filtered_spec = filtered_spec[filtered_spec['Completed'] == 'Yes']

            # Create Table 2 with Name, Email, Course/Specs (with completion date), Completion Time
            if len(filtered_spec) > 0:
                # Build Course/Specs with appended specialization completion date if available
                if 'Specialization' in filtered_spec.columns:
                    spec_specs = filtered_spec['Specialization'].astype(str)
                    # Use unified 'Completion Time'
                    scomp = pd.to_datetime(filtered_spec.get('Completion Time'), errors='coerce', utc=True)
                    scomp_str = scomp.dt.strftime('%d/%m/%Y')
                    scomp_str = scomp_str.where(scomp.notna(), '')
                    spec_specs = spec_specs + scomp_str.apply(lambda s: f" ({s})" if s else "")
                    filtered_spec['Course/Specs'] = spec_specs
                cols2 = [c for c in ['Name', 'Email', 'Course/Specs', 'Completion Time'] if c in filtered_spec.columns]
                table2 = filtered_spec[cols2].copy()
        # Join Table 1 and Table 2 to create Table 3
        table3 = pd.DataFrame()

        if table1 is not None and table2 is not None:
            table3 = pd.concat([table1, table2], ignore_index=True)
        elif table1 is not None:
            table3 = table1.copy()
        elif table2 is not None:
            table3 = table2.copy()

        # Display the combined table and analysis
        if not table3.empty:
            st.subheader("Combined Table (Table 3)")
            st.write("**Combined data with Name, Email, Course/Specs, and Completion Time:**")
            st.dataframe(table3)

            # Compute metrics and build downstream tables
            t3 = table3.copy()
            # Normalize email
            if 'Email' in t3.columns:
                t3['Email'] = t3['Email'].astype(str).str.strip().str.lower()
            # Parse unified Completion Time
            has_completion = 'Completion Time' in t3.columns
            if has_completion:
                t3['Completion Time'] = pd.to_datetime(t3['Completion Time'], errors='coerce', utc=True)
                cutoff = pd.Timestamp('2025-01-01', tz='UTC')
                # 2025-only subset for metrics (1) and (2)
                t3_2025 = t3.dropna(subset=['Completion Time'])
                t3_2025 = t3_2025[t3_2025['Completion Time'] >= cutoff]
                total_2025_certificates = int(len(t3_2025))
                unique_2025_learners = int(t3_2025['Email'].nunique())

                # Eligible emails for Top Learner List: max completion time >= cutoff on full data
                max_last = t3.groupby('Email', dropna=True)['Completion Time'].max()
                eligible_emails = set(max_last.index[(max_last >= cutoff)].tolist())
            else:
                cutoff = pd.Timestamp('2025-01-01', tz='UTC')
                t3_2025 = t3.copy()
                total_2025_certificates = 0
                unique_2025_learners = int(t3['Email'].nunique())
                eligible_emails = set(t3['Email'].dropna().unique().tolist())

            # Recompute totals based on combined table (no longer used for metrics)

            # Show some additional statistics
            st.subheader("Additional Statistics")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("2025 Certificates", total_2025_certificates)

            with col2:
                st.metric("2025 Unique Learners", unique_2025_learners)


            # Top Learner List: based on full table but only learners whose max Completion Time >= cutoff
            st.subheader("Top Learner List (2025-eligible)")
            try:
                # Ensure email is lowercase for grouping consistency
                t4 = t3.copy()
                # Filter to only eligible emails for top list
                if 'Email' in t4.columns and eligible_emails:
                    t4 = t4[t4['Email'].isin(eligible_emails)]
                # Derive a representative Name per email: most frequent Name, fallback to first non-null
                if 'Name' in t4.columns:
                    name_per_email = (
                        t4
                        .groupby('Email')['Name']
                        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else s.dropna().iat[0] if not s.dropna().empty else None)
                        .reset_index()
                    )
                else:
                    name_per_email = t4[['Email']].drop_duplicates().copy()
                    name_per_email['Name'] = None

                counts = (
                    t4
                    .groupby(["Email"], dropna=False)
                    .size()
                    .reset_index(name="Total course/spec number")
                )

                # Aggregate list of courses/specs per email (distinct, preserve appearance order)
                if 'Course/Specs' in t4.columns:
                    courses_per_email = (
                        t4
                        .groupby('Email')['Course/Specs']
                        .agg(lambda s: '\n'.join(list(dict.fromkeys([str(x) for x in s.dropna().tolist()]))))
                        .reset_index()
                        .rename(columns={"Course/Specs": "Courses/Specs list"})
                    )
                else:
                    courses_per_email = name_per_email[['Email']].copy()
                    courses_per_email['Courses/Specs list'] = ''

                table4 = (
                    counts
                    .merge(name_per_email, on='Email', how='left')
                    .merge(courses_per_email, on='Email', how='left')
                    [["Name", "Email", "Total course/spec number", "Courses/Specs list"]]
                    .sort_values(by="Total course/spec number", ascending=False)
                    .reset_index(drop=True)
                )
                st.write("Sorted in decreasing order by total (eligible learners only)")
                # Option to render with wrapped lines (HTML) or as a standard dataframe
                wrap_view = st.toggle("Wrap Courses/Specs list", value=True, key="wrap_courses_specs_list")
                if wrap_view:
                    # Convert newlines to <br> for HTML rendering and show as Markdown table
                    html_df = table4.copy()
                    html_df['Courses/Specs list'] = html_df['Courses/Specs list'].astype(str).str.replace('\n', '<br>')
                    st.markdown(html_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                else:
                    st.dataframe(table4, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not build Table 4: {e}")

        else:
            st.warning("No data available for combined analysis")

    except Exception as e:
        st.error(f"Error in combined analysis: {str(e)}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="GCC File Processor",
        page_icon="📊",
        layout="wide"
    )
    
    # Main title
    st.title("GCC File Processor")
    st.markdown("Upload your CSV files to process and analyze the data.")
    # File requirements section
    st.markdown("---")
    st.markdown("""
    ### File Requirements:
    - **Format:** CSV (Comma-separated values)
    - **Encoding:** UTF-8
    - **Separator:** Comma (,)
    """)
    st.markdown("---")
    
    # Initialize session state for storing results
    if 'usage_df' not in st.session_state:
        st.session_state.usage_df = None
    if 'spec_df' not in st.session_state:
        st.session_state.spec_df = None
    if 'essentials_count' not in st.session_state:
        st.session_state.essentials_count = 0
    if 'specialization_count' not in st.session_state:
        st.session_state.specialization_count = 0
    
    # Create two columns for the upload sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Step 1A: Usage Report CSV")
        st.markdown("Upload your GCC Usage Report CSV file")
        
        usage_file = st.file_uploader(
            "Choose Usage Report CSV file",
            type=['csv'],
            help="Upload a UTF-8 encoded, comma-separated CSV file",
            key="usage_uploader"
        )
        
        if usage_file is not None:
            st.success("Usage Report CSV uploaded successfully!")
            with st.spinner("Processing GCC Usage Report..."):
                result = process_gcc_usage_report(usage_file)
                if result is not None:
                    st.session_state.usage_df = result['df']
                    st.session_state.essentials_count = result['count']
    
    with col2:
        st.header("Step 1B: Specialization CSV")
        st.markdown("Upload your GCC Specialization CSV file")
        
        spec_file = st.file_uploader(
            "Choose Specialization CSV file",
            type=['csv'],
            help="Upload a UTF-8 encoded, comma-separated CSV file",
            key="spec_uploader"
        )
        
        if spec_file is not None:
            st.success("Specialization CSV uploaded successfully!")
            with st.spinner("Processing GCC Specialization file..."):
                result = process_gcc_specialization_file(spec_file)
                if result is not None:
                    st.session_state.spec_df = result['df']
                    st.session_state.specialization_count = result['count']
    
    # Step 2: Combined Analysis (only show if both files are processed)
    if (st.session_state.usage_df is not None or st.session_state.spec_df is not None):
        join_and_analyze_tables(
            st.session_state.usage_df, 
            st.session_state.spec_df
        )
    
    

if __name__ == "__main__":
    main()
