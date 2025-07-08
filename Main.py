import streamlit as st
import pandas as pd
import os

# --- Data Definition (Replaces Excel File) ---
data = {
    'Code': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
    'Course': [
        "Introduction to Programming", "Data Structures", "Algorithms",
        "Database Management", "Web Development", "Operating Systems",
        "Computer Networks", "Artificial Intelligence", "Machine Learning",
        "Cybersecurity Fundamentals", "Cloud Computing", "Mobile App Development",
        "Game Design", "Software Engineering", "Human-Computer Interaction"
    ],
    'Incompatibilities': [
        '', '101', '101,102', '', '103', '102',
        '101,104', '102,103', '108', '105', '107',
        '104,105', '101,102', '106', ''
    ]
}
df = pd.DataFrame(data)
# --- End of Data Definition ---

# Prepare data (same as your original code)
df['Incompatibilities'] = df['Incompatibilities'].fillna('').astype(str)
df['Incompatible_List'] = df['Incompatibilities'].apply(
    lambda x: [i.strip() for i in x.split(',') if i.strip().isdigit()]
)
df['Decision'] = 'No'  # Default

st.set_page_config(layout="wide")
st.title("🎓 Interactive Course Selection Tool")
st.markdown("Choose up to **5 courses**. Incompatible options will be grayed out but still visible below.")

# Track session state
if 'selections' not in st.session_state:
    st.session_state.selections = {}

selected_codes = [
    code for code, decision in st.session_state.selections.items() if decision == 'Yes'
]

# Find all incompatible course codes
incompatible_all = set()
for code in selected_codes:
    course_row = df[df['Code'] == int(code)]
    if not course_row.empty:
        incompatible_all.update(course_row.iloc[0]['Incompatible_List'])

# Count limit warning
if len(selected_codes) >= 5:
    st.warning("⚠️ You have selected 5 courses. Deselect one to add others.")

# Show the course table
st.markdown("### 📋 Course List")
for idx, row in df.iterrows():
    code = str(row['Code'])
    name = row['Course']
    is_selected = st.session_state.selections.get(code) == 'Yes'
    is_disabled = False
    reason = ""

    if code in incompatible_all and not is_selected:
        is_disabled = True
        reason = "❌ Incompatible with selected courses"

    if len(selected_codes) >= 5 and not is_selected:
        is_disabled = True
        reason = "⚠️ Limit reached"

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{name}** (Code: `{code}`)")
    with col2:
        option = st.selectbox(
            label="",
            options=["No", "Yes"],
            index=1 if is_selected else 0,
            key=f"decision_{code}",
            disabled=is_disabled,
            help=reason
        )
        st.session_state.selections[code] = option

# Final course selection
final_selected_codes = [c for c, v in st.session_state.selections.items() if v == 'Yes']
final_selected_names = [df[df['Code'] == int(c)].iloc[0]['Course'] for c in final_selected_codes]

st.markdown("---")
st.subheader("✅ Selected Courses:")
if final_selected_names:
    for name in final_selected_names:
        st.write(f"• {name}")
else:
    st.write("No courses selected.")

# Show incompatible courses in a message box
st.markdown("### 🚫 Incompatible Courses:")
if final_selected_codes:
    incompatible_names = set()
    for code in final_selected_codes:
        row = df[df['Code'] == int(code)].iloc[0]
        incompatible_codes = row['Incompatible_List']
        for inc in incompatible_codes:
            if inc not in final_selected_codes:
                course_name = df[df['Code'] == int(inc)]['Course'].values
                if len(course_name) > 0:
                    incompatible_names.add(course_name[0])

    if incompatible_names:
        st.error("The following courses are **not compatible** with your current selection:")
        for name in sorted(incompatible_names):
            st.markdown(f"• {name}")
    else:
        st.success("No conflicts! 🎉 All selected courses are compatible.")
else:
    st.info("Select courses to see incompatibility information.")

# Instructions for users
st.markdown("---")
st.markdown("### 📝 Instructions:")
st.markdown("""
1. **Select up to 5 courses** from the list above
2. **Incompatible courses** will be automatically disabled when you make selections
3. **View your final selection** in the summary above
4. **Check compatibility** in the incompatible courses section
""")

st.markdown("### 🚀 Deployment:")
st.markdown("To run this app locally: `pip install streamlit pandas` and then `streamlit run your_script_name.py`")
