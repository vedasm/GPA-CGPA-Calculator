import csv
import io
import streamlit as st

from calculator import (
    GRADE_POINTS,
    Subject,
    Semester,
    calculate_cgpa,
    calculate_gpa,
    cgpa_to_percentage,
)

st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

if "gpa_rows" not in st.session_state:
    st.session_state.gpa_rows = 1
if "cgpa_rows" not in st.session_state:
    st.session_state.cgpa_rows = 1
if "gpa_result" not in st.session_state:
    st.session_state.gpa_result = None
if "cgpa_result" not in st.session_state:
    st.session_state.cgpa_result = None


st.title("🎓 GPA & CGPA Calculator")
st.caption("App for calculating semester GPA and overall CGPA.")

tab1, tab2, tab3 = st.tabs(["GPA Calculator", "CGPA Calculator", "Grade Scale"])


with tab1:
    st.subheader("GPA Calculator")
    st.write("Enter your subjects, credits, and grades.")

    # column headers
    col1, col2, col3 = st.columns([2.7, 1, 1])
    col1.markdown("**Subject Name**")
    col2.markdown("**Credits**")
    col3.markdown("**Grade**")

    subjects = []
    n = st.session_state.gpa_rows

    for i in range(n):
        c1, c2, c3 = st.columns([2.7, 1, 1])
        with c1:
            name = st.text_input(
                "name",
                key=f"gpa_{i}_name",
                placeholder=f"Subject {i + 1}",
                label_visibility="collapsed",
            )
        with c2:
            credits = st.number_input(
                "credits",
                min_value=1, max_value=50, value=1, step=1,
                key=f"gpa_{i}_credits",
                label_visibility="collapsed",
            )
        with c3:
            grade = st.selectbox(
                "grade",
                list(GRADE_POINTS.keys()),
                key=f"gpa_{i}_grade",
                label_visibility="collapsed",
            )
        subjects.append(Subject(name=name, credits=int(credits), grade=grade))

    b1, b2, b3 = st.columns(3)

    if b1.button("➕ Add Subject", use_container_width=True):
        if st.session_state.gpa_rows < 20:
            st.session_state.gpa_rows += 1
        st.rerun()

    if b2.button("➖ Remove Last", use_container_width=True, disabled=n <= 1):
        st.session_state.gpa_rows -= 1
        st.rerun()

    if b3.button("↺ Reset", key="gpa_reset", use_container_width=True):
        st.session_state.gpa_rows = 1
        st.session_state.gpa_result = None
        st.rerun()

    if st.button("Calculate GPA", type="primary", use_container_width=True):
        try:
            gpa, total_credits = calculate_gpa(subjects)
            st.session_state.gpa_result = {
                "gpa": gpa,
                "percentage": cgpa_to_percentage(gpa),
                "credits": total_credits,
                "rows": subjects,
            }
        except ValueError as e:
            st.session_state.gpa_result = {"error": str(e)}

    if st.session_state.gpa_result:
        res = st.session_state.gpa_result
        if "error" in res:
            st.error(res["error"])
        else:
            st.success("GPA calculated successfully.")

            m1, m2, m3 = st.columns(3)
            m1.metric("GPA", f"{res['gpa']:.2f}")
            m2.metric("Percentage", f"{res['percentage']:.2f}%")
            m3.metric("Credits", res["credits"])

            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(["Subject", "Credits", "Grade", "Grade Point"])
            for s in res["rows"]:
                writer.writerow([s.name, s.credits, s.grade, GRADE_POINTS[s.grade]]) # type: ignore
            csv_data = buf.getvalue().encode("utf-8")

            st.download_button(
                "Download GPA CSV",
                data=csv_data,
                file_name="gpa_result.csv",
                mime="text/csv",
                use_container_width=True,
            )

            with st.expander("View breakdown"):
                table = []
                for s in res["rows"]:
                    table.append({
                        "Subject": s.name, # type: ignore
                        "Credits": s.credits, # type: ignore
                        "Grade": s.grade, # type: ignore
                        "Grade Point": GRADE_POINTS[s.grade], # type: ignore
                    })
                st.dataframe(table, use_container_width=True, hide_index=True)


with tab2:
    st.subheader("CGPA Calculator")
    st.write("Enter semester GPA and credits for each semester.")

    col1, col2, col3 = st.columns(3)
    col1.markdown("**Semester**")
    col2.markdown("**GPA**")
    col3.markdown("**Credits**")

    semesters = []
    m = st.session_state.cgpa_rows

    for i in range(m):
        c1, c2, c3 = st.columns(3)
        with c1:
            sem_no = st.number_input(
                "sem",
                min_value=1, max_value=20, value=i + 1, step=1,
                key=f"cgpa_{i}_sem",
                label_visibility="collapsed",
            )
        with c2:
            gpa_val = st.number_input(
                "gpa",
                min_value=0.0, max_value=10.0, value=0.0, step=0.01, format="%.2f",
                key=f"cgpa_{i}_gpa",
                label_visibility="collapsed",
            )
        with c3:
            credits = st.number_input(
                "credits",
                min_value=1, max_value=50, value=20, step=1,
                key=f"cgpa_{i}_credits",
                label_visibility="collapsed",
            )
        semesters.append(Semester(semester_no=int(sem_no), gpa=float(gpa_val), credits=int(credits)))

    b1, b2, b3 = st.columns(3)

    if b1.button("➕ Add Semester", use_container_width=True):
        if st.session_state.cgpa_rows < 20:
            st.session_state.cgpa_rows += 1
        st.rerun()

    if b2.button("➖ Remove Last", key="cgpa_remove", use_container_width=True, disabled=m <= 1):
        st.session_state.cgpa_rows -= 1
        st.rerun()

    if b3.button("↺ Reset", key="cgpa_reset", use_container_width=True):
        st.session_state.cgpa_rows = 1
        st.session_state.cgpa_result = None
        st.rerun()

    if st.button("Calculate CGPA", type="primary", use_container_width=True):
        try:
            cgpa, total_credits = calculate_cgpa(semesters)
            st.session_state.cgpa_result = {
                "cgpa": cgpa,
                "percentage": cgpa_to_percentage(cgpa),
                "credits": total_credits,
                "rows": semesters,
            }
        except ValueError as e:
            st.session_state.cgpa_result = {"error": str(e)}

    if st.session_state.cgpa_result:
        res = st.session_state.cgpa_result
        if "error" in res:
            st.error(res["error"])
        else:
            st.success("CGPA calculated successfully.")

            m1, m2, m3 = st.columns(3)
            m1.metric("CGPA", f"{res['cgpa']:.2f}")
            m2.metric("Percentage", f"{res['percentage']:.2f}%")
            m3.metric("Credits", res["credits"])

            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(["Semester", "GPA", "Credits"])
            for s in res["rows"]:
                writer.writerow([s.semester_no, f"{s.gpa:.2f}", s.credits]) # type: ignore

            st.download_button(
                "Download CGPA CSV",
                data=buf.getvalue().encode("utf-8"),
                file_name="cgpa_result.csv",
                mime="text/csv",
                use_container_width=True,
            )

            with st.expander("View breakdown"):
                st.dataframe(
                    [{"Semester": s.semester_no, "GPA": f"{s.gpa:.2f}", "Credits": s.credits} for s in res["rows"]], # type: ignore
                    use_container_width=True,
                    hide_index=True,
                )

with tab3:
    st.subheader("Grade Scale")
    st.dataframe(
        [{"Grade": g, "Points": p} for g, p in GRADE_POINTS.items()],
        use_container_width=True,
        hide_index=True,
    )

st.divider()
st.caption("Built By Veda.")