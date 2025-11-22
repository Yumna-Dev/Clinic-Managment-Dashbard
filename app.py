# ============================================================
# 🏥 Doctor Clinic Management Dashboard
# ============================================================
# Realistic clinic data with numpy, pandas & streamlit
# Complete with patient records, appointments & analytics

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Clinic Management System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Doctor Clinic Management Dashboard")
st.markdown("Manage **patient records, appointments, and clinic analytics** in real-time.")

# ------------------------------------------------------------
# 1️⃣ Generate Realistic Clinic Data
# ------------------------------------------------------------
@st.cache_data
def generate_clinic_data():
    np.random.seed(42)
    
    # Patient Data
    patient_ids = [f"PAT{1000 + i}" for i in range(200)]
    first_names = ["John", "Jane", "Robert", "Maria", "David", "Sarah", "Michael", "Lisa", 
                  "James", "Jennifer", "William", "Linda", "Richard", "Susan", "Joseph"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                 "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    
    patients = []
    for pid in patient_ids:
        patients.append({
            'patient_id': pid,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'age': np.random.randint(18, 80),
            'gender': random.choice(['Male', 'Female']),
            'phone': f"555-{np.random.randint(100,999)}-{np.random.randint(1000,9999)}",
            'email': f"patient{pid[3:]}@email.com",
            'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
            'emergency_contact': f"555-{np.random.randint(100,999)}-{np.random.randint(1000,9999)}",
            'registration_date': datetime.now() - timedelta(days=np.random.randint(1, 365))
        })
    
    # Doctors Data
    doctors = [
        {'doctor_id': 'DOC101', 'name': 'Dr. Sarah Wilson', 'specialization': 'Cardiology', 
         'phone': '555-101-1001', 'email': 'sarah.wilson@clinic.com', 'consultation_fee': 150},
        {'doctor_id': 'DOC102', 'name': 'Dr. Michael Chen', 'specialization': 'Pediatrics', 
         'phone': '555-101-1002', 'email': 'michael.chen@clinic.com', 'consultation_fee': 120},
        {'doctor_id': 'DOC103', 'name': 'Dr. Emily Davis', 'specialization': 'Dermatology', 
         'phone': '555-101-1003', 'email': 'emily.davis@clinic.com', 'consultation_fee': 130},
        {'doctor_id': 'DOC104', 'name': 'Dr. Robert Kumar', 'specialization': 'Orthopedics', 
         'phone': '555-101-1004', 'email': 'robert.kumar@clinic.com', 'consultation_fee': 160},
        {'doctor_id': 'DOC105', 'name': 'Dr. Lisa Rodriguez', 'specialization': 'General Medicine', 
         'phone': '555-101-1005', 'email': 'lisa.rodriguez@clinic.com', 'consultation_fee': 110}
    ]
    
    # Appointments Data
    appointments = []
    statuses = ['Scheduled', 'Completed', 'Cancelled', 'No-Show']
    reasons = ['Regular Checkup', 'Fever', 'Headache', 'Back Pain', 'Skin Issue', 
               'Heart Check', 'Child Vaccination', 'Follow-up', 'Emergency']
    
    for i in range(300):
        appt_date = datetime.now() - timedelta(days=np.random.randint(0, 90))
        appt_time = f"{np.random.randint(9, 17):02d}:{np.random.choice(['00', '15', '30', '45'])}"
        status = random.choice(statuses)
        
        appointments.append({
            'appointment_id': f"APT{5000 + i}",
            'patient_id': random.choice(patient_ids),
            'doctor_id': random.choice([doc['doctor_id'] for doc in doctors]),
            'appointment_date': appt_date.date(),
            'appointment_time': appt_time,
            'status': status,
            'reason': random.choice(reasons),
            'fee_paid': random.choice([True, False]) if status == 'Completed' else False,
            'notes': random.choice(['Routine check', 'Medication review', 'Test results', ''])
        })
    
    # Medical Records
    medical_records = []
    diagnoses = ['Hypertension', 'Diabetes Type 2', 'Common Cold', 'Migraine', 'Back Strain',
                'Skin Rash', 'Arthritis', 'Asthma', 'Anxiety', 'UTI', 'Sinusitis']
    medications = ['Amoxicillin 500mg', 'Metformin 850mg', 'Lisinopril 10mg', 'Ibuprofen 400mg',
                  'Atorvastatin 20mg', 'Ventolin Inhaler', 'Cetirizine 10mg', 'Omeprazole 20mg']
    
    for i in range(250):
        record_date = datetime.now() - timedelta(days=np.random.randint(1, 180))
        medical_records.append({
            'record_id': f"REC{7000 + i}",
            'patient_id': random.choice(patient_ids),
            'doctor_id': random.choice([doc['doctor_id'] for doc in doctors]),
            'visit_date': record_date.date(),
            'diagnosis': random.choice(diagnoses),
            'prescription': random.choice(medications),
            'blood_pressure': f"{np.random.randint(110, 140)}/{np.random.randint(70, 90)}",
            'temperature': round(np.random.uniform(36.5, 38.5), 1),
            'notes': random.choice(['Stable condition', 'Follow up in 2 weeks', 'Lab tests ordered', ''])
        })
    
    # Convert to DataFrames
    patients_df = pd.DataFrame(patients)
    doctors_df = pd.DataFrame(doctors)
    appointments_df = pd.DataFrame(appointments)
    medical_records_df = pd.DataFrame(medical_records)
    
    return patients_df, doctors_df, appointments_df, medical_records_df

# Load data
patients_df, doctors_df, appointments_df, medical_records_df = generate_clinic_data()

# ------------------------------------------------------------
# 2️⃣ Sidebar Filters
# ------------------------------------------------------------
st.sidebar.header("🔍 Clinic Filters")

# Date range for appointments
min_date = appointments_df['appointment_date'].min()
max_date = appointments_df['appointment_date'].max()

date_range = st.sidebar.date_input(
    "Appointment Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data based on date range
if len(date_range) == 2:
    filtered_appointments = appointments_df[
        (appointments_df['appointment_date'] >= date_range[0]) & 
        (appointments_df['appointment_date'] <= date_range[1])
    ]
else:
    filtered_appointments = appointments_df

# Doctor filter
doctor_options = ["All Doctors"] + doctors_df['name'].tolist()
selected_doctor = st.sidebar.selectbox("Select Doctor", doctor_options)

if selected_doctor != "All Doctors":
    doctor_id = doctors_df[doctors_df['name'] == selected_doctor]['doctor_id'].iloc[0]
    filtered_appointments = filtered_appointments[filtered_appointments['doctor_id'] == doctor_id]

# Status filter
status_options = ["All Status"] + appointments_df['status'].unique().tolist()
selected_status = st.sidebar.selectbox("Appointment Status", status_options)

if selected_status != "All Status":
    filtered_appointments = filtered_appointments[filtered_appointments['status'] == selected_status]

# ------------------------------------------------------------
# 3️⃣ Key Performance Indicators
# ------------------------------------------------------------
st.subheader("📊 Clinic Overview")

# Calculate KPIs
total_patients = len(patients_df)
total_appointments = len(filtered_appointments)
completed_appointments = len(filtered_appointments[filtered_appointments['status'] == 'Completed'])
revenue = len(filtered_appointments[filtered_appointments['status'] == 'Completed']) * 120  # Average fee
today_appointments = len(filtered_appointments[filtered_appointments['appointment_date'] == datetime.now().date()])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Patients", f"{total_patients}")
col2.metric("Total Appointments", f"{total_appointments}")
col3.metric("Completed Visits", f"{completed_appointments}")
col4.metric("Estimated Revenue", f"${revenue:,}")
col5.metric("Today's Appointments", f"{today_appointments}")

# ------------------------------------------------------------
# 4️⃣ Visualizations
# ------------------------------------------------------------
st.subheader("📈 Clinic Analytics")

# Appointment Status Distribution
col1, col2 = st.columns(2)

with col1:
    status_counts = filtered_appointments['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig1 = px.pie(
        status_counts, 
        values='Count', 
        names='Status',
        title='Appointment Status Distribution',
        hole=0.4
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Doctor Performance
    doctor_appointments = filtered_appointments.groupby('doctor_id').size().reset_index()
    doctor_appointments.columns = ['doctor_id', 'appointment_count']
    doctor_appointments = doctor_appointments.merge(doctors_df, on='doctor_id')
    
    fig2 = px.bar(
        doctor_appointments,
        x='name',
        y='appointment_count',
        title='Appointments by Doctor',
        color='specialization'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Monthly Trends
st.subheader("📅 Monthly Trends")

# Convert to datetime for grouping
filtered_appointments['appointment_date'] = pd.to_datetime(filtered_appointments['appointment_date'])
monthly_trends = filtered_appointments.groupby(
    filtered_appointments['appointment_date'].dt.to_period('M')
).size().reset_index()
monthly_trends.columns = ['Month', 'Appointments']
monthly_trends['Month'] = monthly_trends['Month'].dt.to_timestamp()

fig3 = px.line(
    monthly_trends,
    x='Month',
    y='Appointments',
    title='Monthly Appointment Trends',
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------------------
# 5️⃣ Patient & Appointment Management
# ------------------------------------------------------------
st.subheader("👥 Patient Management")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Patients", "📅 Appointments", "💊 Medical Records", "➕ New Entry"])

with tab1:
    st.dataframe(patients_df, use_container_width=True)

with tab2:
    # Enhanced appointments view
    appointments_display = filtered_appointments.merge(
        patients_df[['patient_id', 'first_name', 'last_name']], 
        on='patient_id'
    ).merge(
        doctors_df[['doctor_id', 'name', 'specialization']], 
        on='doctor_id'
    )
    
    # Rename for display
    appointments_display = appointments_display.rename(columns={
        'name': 'doctor_name',
        'first_name': 'patient_first_name',
        'last_name': 'patient_last_name'
    })
    
    st.dataframe(appointments_display, use_container_width=True)

with tab3:
    # Medical records with patient and doctor info
    records_display = medical_records_df.merge(
        patients_df[['patient_id', 'first_name', 'last_name']], 
        on='patient_id'
    ).merge(
        doctors_df[['doctor_id', 'name']], 
        on='doctor_id'
    )
    
    st.dataframe(records_display, use_container_width=True)

with tab4:
    # Quick add new patient form
    st.subheader("Add New Patient")
    
    with st.form("new_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        
        if st.form_submit_button("Add Patient"):
            new_patient_id = f"PAT{1000 + len(patients_df)}"
            new_patient = {
                'patient_id': new_patient_id,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender': gender,
                'phone': phone,
                'email': f"{first_name.lower()}.{last_name.lower()}@email.com",
                'blood_group': blood_group,
                'emergency_contact': phone,
                'registration_date': datetime.now()
            }
            
            # In a real app, you'd save to database
            st.success(f"✅ Patient {first_name} {last_name} added successfully!")
            st.info("In a real application, this would be saved to your database.")

# ------------------------------------------------------------
# 6️⃣ Real-time Alerts
# ------------------------------------------------------------
st.subheader("⚠️ Clinic Alerts")

# Today's appointments
today = datetime.now().date()
todays_appointments = appointments_df[appointments_df['appointment_date'] == today]

if not todays_appointments.empty:
    st.info(f"📅 You have {len(todays_appointments)} appointments today")
    
    for _, apt in todays_appointments.head(3).iterrows():
        patient_name = patients_df[patients_df['patient_id'] == apt['patient_id']].iloc[0]
        doctor_name = doctors_df[doctors_df['doctor_id'] == apt['doctor_id']].iloc[0]
        
        st.write(f"⏰ **{apt['appointment_time']}** - {patient_name['first_name']} {patient_name['last_name']} with {doctor_name['name']}")

# Low stock alert (simulated)
st.warning("💊 Medication stock low: Amoxicillin 500mg (15 units remaining)")

# ------------------------------------------------------------
# 7️⃣ Export Data
# ------------------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("📤 Export Data")

if st.sidebar.button("Export Patient Data"):
    patients_csv = patients_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download Patients CSV",
        data=patients_csv,
        file_name="clinic_patients.csv",
        mime="text/csv"
    )

if st.sidebar.button("Export Appointments Data"):
    appointments_csv = filtered_appointments.to_csv(index=False)
    st.sidebar.download_button(
        label="Download Appointments CSV",
        data=appointments_csv,
        file_name="clinic_appointments.csv",
        mime="text/csv"
    )