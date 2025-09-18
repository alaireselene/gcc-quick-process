import streamlit as st
import pandas as pd

def process_ai_essentials_certificates(df):
    """
    Process and filter AI Essentials certificates based on specific criteria:
    - Course = "Google AI Essentials"
    - Enrollment Time >= Jan 01 2025
    - Completed = Yes
    """
    try:
        # Make a copy to avoid modifying the original dataframe
        filtered_df = df.copy()
        
        # Display original data info
        st.write(f"**Original data:** {len(df)} total rows")
        
        # Filter 1: Course = "Google AI Essentials"
        if 'Course' in filtered_df.columns:
            course_filter = filtered_df['Course'] == 'Google AI Essentials'
            filtered_df = filtered_df[course_filter]
            st.write(f"**After Course filter:** {len(filtered_df)} rows (Course = 'Google AI Essentials')")
        else:
            st.warning("⚠️ 'Course' column not found in the data")
            return 0
        
        # Filter 2: Enrollment Time >= Jan 01 2025
        if 'Enrollment Time' in filtered_df.columns:
            # Convert enrollment time to datetime
            filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
            filtered_df['Enrollment Time'] = pd.to_datetime(filtered_df['Enrollment Time'], errors='coerce')
            
            # Create cutoff date - start with naive datetime
            cutoff_date = pd.Timestamp('2025-01-01')
            
            # Handle timezone compatibility
            try:
                # First, try the comparison as-is (works if both are naive or both have same timezone)
                date_filter = filtered_df['Enrollment Time'] >= cutoff_date
                filtered_df = filtered_df[date_filter]
            except TypeError:
                # If comparison fails, try to make them compatible
                if filtered_df['Enrollment Time'].dt.tz is not None:
                    # Data is timezone-aware, make cutoff timezone-aware
                    cutoff_date = cutoff_date.tz_localize('UTC')
                else:
                    # Data is timezone-naive, ensure cutoff is also naive
                    cutoff_date = cutoff_date.tz_localize(None) if cutoff_date.tz is not None else cutoff_date
                
                date_filter = filtered_df['Enrollment Time'] >= cutoff_date
                filtered_df = filtered_df[date_filter]
            
            st.write(f"**After Date filter:** {len(filtered_df)} rows (Enrollment Time >= Jan 01, 2025)")
        else:
            st.warning("⚠️ 'Enrollment Time' column not found in the data")
            return 0
        
        # Filter 3: Completed = "Yes"
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
        st.success(f"🎯 **Total {total_certificates} AI Essentials certificate{'s' if total_certificates != 1 else ''}**")
        
        # Show filtered data if any results
        if total_certificates > 0:
            st.subheader("Filtered Results")
            st.write("**AI Essentials Certificates (matching all criteria):**")
            # Display relevant columns
            display_columns = ['Name', 'Email', 'Course', 'Enrollment Time', 'Completed', 'Completion Time']
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            st.dataframe(filtered_df[available_columns])
            
        return total_certificates
        
    except Exception as e:
        st.error(f"❌ Error processing AI Essentials certificates: {str(e)}")
        return 0

def process_gcc_usage_report(uploaded_file):
    """
    Process GCC Usage Report file (Type A)
    """
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        # Normalize emails early to avoid case-sensitivity issues
        if 'Email' in df.columns:
            df['Email'] = df['Email'].astype(str).str.strip().str.lower()
        
        st.success(f"✅ Successfully loaded GCC Usage Report file with {len(df)} rows and {len(df.columns)} columns")
        
        # AI Essentials Certificate Processing
        st.subheader("🤖 AI Essentials Certificate Analysis")
        
        # Filter for AI Essentials certificates
        count = process_ai_essentials_certificates(df)
        
        return {"df": df, "count": count}
        
    except Exception as e:
        st.error(f"❌ Error processing GCC Usage Report file: {str(e)}")
        return None
