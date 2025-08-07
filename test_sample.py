#!/usr/bin/env python3
"""
Test script for AI Essentials certificate filtering with sample data
"""

import pandas as pd
import io

def test_ai_essentials_filter():
    """Test the AI Essentials filtering logic with sample data"""
    
    # Sample data based on the provided example
    sample_data = """Name,Email,External Id,Course,Course ID,Course Slug,University,Enrollment Time,Class Start Time,Class End Time,Last Course Activity Time,Overall Progress,Estimated Learning Hours,Completed,Removed From Program,Program Slug,Program Name,Enrollment Source,Completion Time,Course Grade,Course Certificate URL,Course Type,Job Title,Job Type,Business Unit,Business Unit 2,Location City
Vũ Trang Nhung,hat22080256@hsb.edu.vn,,Satisfaction Guaranteed: Develop Customer Loyalty Online,UK7yonsIEey1tgpUmO8AYQ,satisfaction-guaranteed,Google,2024-08-15T09:10:18.000Z,2024-08-19T07:00:00.000Z,2024-09-23T06:59:59.000Z,,0.0,0.0,No,Yes,hanoi-school-of-busi-google-learning-program-tvhnm,Archived_Không sử dụng,,,0.0,,Course,,,,,
Phạm Thị Minh Thư,phamthiminhthu1522003@gmail.com,102,Foundations of Digital Marketing and E-commerce,g-0dF3JpEeys9RJMWW48Yw,foundations-of-digital-marketing-and-e-commerce,Google,2025-04-25T15:24:27.000Z,2025-04-28T07:00:00.000Z,2025-06-02T06:59:59.000Z,2025-05-12T15:08:27.000Z,57.73,13.52,No,No,nic-x-huflit-ftbgi,Google x NIC x HUFLIT,GCC,,46.25,,Course,Sinh viên,Khoa Quản trị kinh doanh,HUFLIT,Nữ,TP.HCM
John Doe,john.doe@example.com,103,Google AI Essentials,ai-essentials-123,google-ai-essentials,Google,2025-01-15T10:30:00.000Z,2025-01-20T07:00:00.000Z,2025-02-28T06:59:59.000Z,2025-02-15T14:30:00.000Z,100.0,20.0,Yes,No,ai-program-2025,Google AI Program 2025,GCC,2025-02-15T14:30:00.000Z,95.5,https://coursera.org/certificate/ai123,Course,Software Engineer,Technology,Engineering,AI Team,San Francisco
Jane Smith,jane.smith@example.com,104,Google AI Essentials,ai-essentials-124,google-ai-essentials,Google,2024-12-20T09:15:00.000Z,2025-01-05T07:00:00.000Z,2025-02-10T06:59:59.000Z,2025-02-08T16:45:00.000Z,100.0,18.5,Yes,No,ai-program-2025,Google AI Program 2025,GCC,2025-02-08T16:45:00.000Z,88.2,https://coursera.org/certificate/ai124,Course,Data Scientist,Technology,Research,AI Lab,New York
Mike Johnson,mike.j@example.com,105,Google AI Essentials,ai-essentials-125,google-ai-essentials,Google,2025-03-01T11:20:00.000Z,2025-03-05T07:00:00.000Z,2025-04-15T06:59:59.000Z,2025-04-10T13:20:00.000Z,85.0,15.2,No,No,ai-program-2025,Google AI Program 2025,GCC,,75.0,,Course,Product Manager,Business,Product,AI Strategy,Seattle"""
    
    # Read sample data into DataFrame
    df = pd.read_csv(io.StringIO(sample_data))
    
    print("=== AI Essentials Certificate Filter Test ===\n")
    print(f"Original data: {len(df)} total rows")
    
    # Filter 1: Course = "Google AI Essentials"
    course_filter = df['Course'] == 'Google AI Essentials'
    filtered_df = df[course_filter].copy()  # Use .copy() to avoid SettingWithCopyWarning
    print(f"After Course filter: {len(filtered_df)} rows (Course = 'Google AI Essentials')")
    
    # Filter 2: Enrollment Time >= Jan 01 2025
    filtered_df['Enrollment Time'] = pd.to_datetime(filtered_df['Enrollment Time'], errors='coerce')
    # Convert cutoff_date to UTC timezone to match the data
    cutoff_date = pd.Timestamp('2025-01-01', tz='UTC')
    date_filter = filtered_df['Enrollment Time'] >= cutoff_date
    filtered_df = filtered_df[date_filter]
    print(f"After Date filter: {len(filtered_df)} rows (Enrollment Time >= Jan 01, 2025)")
    
    # Filter 3: Completed = "Yes"
    completed_filter = filtered_df['Completed'] == 'Yes'
    filtered_df = filtered_df[completed_filter]
    print(f"After Completed filter: {len(filtered_df)} rows (Completed = 'Yes')")
    
    # Final count
    total_certificates = len(filtered_df)
    print(f"\n🎯 Total {total_certificates} AI Essentials certificate{'s' if total_certificates != 1 else ''}")
    
    if total_certificates > 0:
        print("\nFiltered Results:")
        display_columns = ['Name', 'Email', 'Course', 'Enrollment Time', 'Completed', 'Completion Time']
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        print(filtered_df[available_columns].to_string(index=False))
    
    return total_certificates

if __name__ == "__main__":
    test_ai_essentials_filter()
