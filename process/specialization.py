import streamlit as st
import pandas as pd

def process_specialization_certificates(df):
    """
    Process and filter Specialization certificates based on specific criteria:
    - Enrollment Time >= Jan 01 2025
    - Completed = Yes
    """
    try:
        # Make a copy to avoid modifying the original dataframe
        filtered_df = df.copy()
        
        # Display original data info
        st.write(f"**Original data:** {len(df)} total rows")
        
        # Filter 1: Enrollment Time >= Jan 01 2025
        if 'Enrollment Time' in filtered_df.columns:
            # Convert enrollment time to datetime
            filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
            filtered_df['Enrollment Time'] = pd.to_datetime(filtered_df['Enrollment Time'], errors='coerce')
            # Use timezone-aware cutoff date to match the data format
            cutoff_date = pd.Timestamp('2025-01-01', tz='UTC')
            date_filter = filtered_df['Enrollment Time'] >= cutoff_date
            filtered_df = filtered_df[date_filter]
            st.write(f"**After Date filter:** {len(filtered_df)} rows (Enrollment Time >= Jan 01, 2025)")
        else:
            st.warning("⚠️ 'Enrollment Time' column not found in the data")
            return 0
        
        # Filter 2: Completed = "Yes"
        if 'Completed' in filtered_df.columns:
            completed_filter = filtered_df['Completed'] == 'Yes'
            filtered_df = filtered_df[completed_filter]
            st.write(f"**After Completed filter:** {len(filtered_df)} rows (Completed = 'Yes')")
        else:
            st.warning("⚠️ 'Completed' column not found in the data")
            return 0
        
        # Final count
        total_certificates = len(filtered_df)
        
        # Display result
        st.success(f"🎯 **Total {total_certificates} Specialization certificate{'s' if total_certificates != 1 else ''}**")
        
        # Show filtered data if any results
        if total_certificates > 0:
            st.subheader("Filtered Results")
            st.write("**Specialization Certificates (matching all criteria):**")
            # Display relevant columns
            display_columns = ['Name', 'Email', 'Specialization', 'University', 'Enrollment Time', 'Completed', 'Specialization Completion Time']
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            st.dataframe(filtered_df[available_columns])
            
        return total_certificates
        
    except Exception as e:
        st.error(f"❌ Error processing Specialization certificates: {str(e)}")
        return 0

def process_gcc_specialization_file(uploaded_file):
    """
    Process GCC Specialization file (Type B)
    """
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        
        st.success(f"✅ Successfully loaded GCC Specialization file with {len(df)} rows and {len(df.columns)} columns")
        
        # Specialization Certificate Processing
        st.subheader("🎓 Specialization Certificate Analysis")
        
        # Filter for Specialization certificates
        count = process_specialization_certificates(df)
        
        return {"df": df, "count": count}
        
    except Exception as e:
        st.error(f"❌ Error processing GCC Specialization file: {str(e)}")
        return None
