import streamlit as st
import pandas as pd

from process.ai_essential import process_gcc_usage_report
from process.specialization import process_gcc_specialization_file

def join_and_analyze_tables(usage_df, spec_df, essentials_count, specialization_count):
    """
    Join the filtered tables and analyze unique learners
    """
    try:
        st.markdown("---")
        st.header("📊 Step 2: Combined Analysis")
        
        # Calculate and show total certificates
        total_certificates = essentials_count + specialization_count
        st.success(f"🎯 **Total Certificates: {total_certificates}** ({essentials_count} AI Essentials + {specialization_count} Specialization)")
        
        # Create Table 1: Filtered AI Essentials (Name, Email, Course)
        table1 = None
        if usage_df is not None and essentials_count > 0:
            # Filter the usage_df with the same criteria as in ai_essential.py
            filtered_usage = usage_df.copy()
            
            # Apply filters
            if 'Course' in filtered_usage.columns:
                filtered_usage = filtered_usage[filtered_usage['Course'] == 'Google AI Essentials']
            
            if 'Enrollment Time' in filtered_usage.columns:
                filtered_usage['Enrollment Time'] = pd.to_datetime(filtered_usage['Enrollment Time'], errors='coerce')
                cutoff_date = pd.Timestamp('2025-01-01', tz='UTC')
                filtered_usage = filtered_usage[filtered_usage['Enrollment Time'] >= cutoff_date]
            
            if 'Completed' in filtered_usage.columns:
                filtered_usage = filtered_usage[filtered_usage['Completed'] == 'Yes']
            
            # Create Table 1 with Name, Email, Course
            if len(filtered_usage) > 0:
                table1 = filtered_usage[['Name', 'Email', 'Course']].copy()
                table1.rename(columns={'Course': 'Course/Specs'}, inplace=True)
        
        # Create Table 2: Filtered Specialization (Name, Email, Specialization)
        table2 = None
        if spec_df is not None and specialization_count > 0:
            # Filter the spec_df with the same criteria as in specialization.py
            filtered_spec = spec_df.copy()
            
            # Apply filters
            if 'Enrollment Time' in filtered_spec.columns:
                filtered_spec['Enrollment Time'] = pd.to_datetime(filtered_spec['Enrollment Time'], errors='coerce')
                cutoff_date = pd.Timestamp('2025-01-01', tz='UTC')
                filtered_spec = filtered_spec[filtered_spec['Enrollment Time'] >= cutoff_date]
            
            if 'Completed' in filtered_spec.columns:
                filtered_spec = filtered_spec[filtered_spec['Completed'] == 'Yes']
            
            # Create Table 2 with Name, Email, Specialization
            if len(filtered_spec) > 0:
                table2 = filtered_spec[['Name', 'Email', 'Specialization']].copy()
                table2.rename(columns={'Specialization': 'Course/Specs'}, inplace=True)
        
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
            st.subheader("📋 Combined Table (Table 3)")
            st.write("**Combined data with Name, Email, and Course/Specs:**")
            st.dataframe(table3)
            
            # Count unique emails
            unique_emails = table3['Email'].nunique()
            st.success(f"👥 **Total {unique_emails} unique learners**")
            
            # Show some additional statistics
            st.subheader("📈 Additional Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Certificates", total_certificates)
            
            with col2:
                st.metric("Unique Learners", unique_emails)
            
            with col3:
                if unique_emails > 0:
                    avg_certs_per_learner = round(total_certificates / unique_emails, 2)
                    st.metric("Avg Certificates per Learner", avg_certs_per_learner)
                else:
                    st.metric("Avg Certificates per Learner", 0)
        
        else:
            st.warning("⚠️ No data available for combined analysis")
            
    except Exception as e:
        st.error(f"❌ Error in combined analysis: {str(e)}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="GCC File Processor",
        page_icon="📊",
        layout="wide"
    )
    
    # Main title
    st.title("📊 GCC File Processor")
    st.markdown("Upload your CSV files to process and analyze the data.")
    # File requirements section
    st.markdown("---")
    st.markdown("""
    ### 📋 File Requirements:
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
        st.header("📈 Step 1A: Usage Report CSV")
        st.markdown("Upload your GCC Usage Report CSV file")
        
        usage_file = st.file_uploader(
            "Choose Usage Report CSV file",
            type=['csv'],
            help="Upload a UTF-8 encoded, comma-separated CSV file",
            key="usage_uploader"
        )
        
        if usage_file is not None:
            st.success("✅ Usage Report CSV uploaded successfully!")
            with st.spinner("Processing GCC Usage Report..."):
                result = process_gcc_usage_report(usage_file)
                if result is not None:
                    st.session_state.usage_df = result['df']
                    st.session_state.essentials_count = result['count']
    
    with col2:
        st.header("🎯 Step 1B: Specialization CSV")
        st.markdown("Upload your GCC Specialization CSV file")
        
        spec_file = st.file_uploader(
            "Choose Specialization CSV file",
            type=['csv'],
            help="Upload a UTF-8 encoded, comma-separated CSV file",
            key="spec_uploader"
        )
        
        if spec_file is not None:
            st.success("✅ Specialization CSV uploaded successfully!")
            with st.spinner("Processing GCC Specialization file..."):
                result = process_gcc_specialization_file(spec_file)
                if result is not None:
                    st.session_state.spec_df = result['df']
                    st.session_state.specialization_count = result['count']
    
    # Step 2: Combined Analysis (only show if both files are processed)
    if (st.session_state.usage_df is not None or st.session_state.spec_df is not None):
        join_and_analyze_tables(
            st.session_state.usage_df, 
            st.session_state.spec_df,
            st.session_state.essentials_count,
            st.session_state.specialization_count
        )
    
    

if __name__ == "__main__":
    main()
