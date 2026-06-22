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

st.set_page_config(
    page_title="GPA & CGPA Calculator",
    page_icon="🎓",
    layout="wide",
)

def init_state() -> None:
    defaults = {
        "gpa_rows": 1,
        "cgpa_rows": 1,
        "gpa_result": None,
        "cgpa_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def key(prefix: str, index: int, field: str) -> str:
    return f"{prefix}_{index}_{field}"

def add_row(prefix: str, limit: int = 20) -> None:
    rows_key = f"{prefix}_rows"
    if st.session_state[rows_key] < limit:
        st.session_state[rows_key] += 1

def remove_row(prefix: str, minimum: int = 1) -> None:
    rows_key = f"{prefix}_rows"
    if st.session_state[rows_key] > minimum:
        st.session_state[rows_key] -= 1

def reset_form(prefix: str) -> None:
    st.session_state[f"{prefix}_rows"] = 1
    st.session_state[f"{prefix}_result"] = None

def csv_bytes(headers, rows) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")

def header_block() -> None:
    st.title("🎓 GPA & CGPA Calculator")
    st.caption("App for calculating semester GPA and overall CGPA.")

def render_gpa_tab() -> None:
    st.subheader("GPA Calculator")
    st.write("Enter your subjects, credits, and grades.")

    c1, c2, c3 = st.columns([2.7, 1, 1])
    c1.markdown("**Subject Name**")
    c2.markdown("**Credits**")
    c3.markdown("**Grade**")

    rows = st.session_state.gpa_rows
    subjects = []

    for i in range(rows):
        a, b, c = st.columns([2.7, 1, 1])
        with a:
            name = st.text_input(
                "Subject name",
                key=key("gpa", i, "name"),
                placeholder=f"Subject {i + 1}",
                label_visibility="collapsed",
            )
        with b:
            credits = st.number_input(
                "Credits",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=key("gpa", i, "credits"),
                label_visibility="collapsed",
            )
        with c:
            grade = st.selectbox(
                "Grade",
                list(GRADE_POINTS.keys()),
                key=key("gpa", i, "grade"),
                label_visibility="collapsed",
            )
        subjects.append(Subject(name=name, credits=int(credits), grade=grade)) # type: ignore

    b1, b2, b3 = st.columns(3)
    if b1.button("➕ Add Subject", key="gpa_add_subject", use_container_width=True):
        add_row("gpa")
        st.rerun()
    if b2.button("➖ Remove Last", key="gpa_remove_subject", use_container_width=True, disabled=rows <= 1):
        remove_row("gpa")
        st.rerun()
    if b3.button("↺ Reset", key="gpa_reset", use_container_width=True):
        reset_form("gpa")
        st.rerun()

    if st.button("Calculate GPA", key="calculate_gpa", type="primary", use_container_width=True):
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

    result = st.session_state.gpa_result
    if result:
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("GPA calculated successfully.")
            m1, m2, m3 = st.columns(3)
            m1.metric("GPA", f"{result['gpa']:.2f}")
            m2.metric("Percentage", f"{result['percentage']:.2f}%")
            m3.metric("Credits", f"{result['credits']}")

            rows_csv = [
                [s.name, s.credits, s.grade, GRADE_POINTS[s.grade]] # type: ignore
                for s in result["rows"]
            ]
            st.download_button(
                "Download GPA CSV",
                data=csv_bytes(["Subject", "Credits", "Grade", "Grade Point"], rows_csv),
                file_name="gpa_result.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_gpa_csv",
            )

            with st.expander("View breakdown"):
                st.dataframe(
                    [
                        {
                            "Subject": s.name, # type: ignore
                            "Credits": s.credits, # pyright: ignore[reportAttributeAccessIssue]
                            "Grade": s.grade, # type: ignore
                            "Grade Point": GRADE_POINTS[s.grade], # type: ignore
                        }
                        for s in result["rows"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

def render_cgpa_tab() -> None:
    st.subheader("CGPA Calculator")
    st.write("Enter semester GPA and credits for each semester.")

    c1, c2, c3 = st.columns(3)
    c1.markdown("**Semester**")
    c2.markdown("**GPA**")
    c3.markdown("**Credits**")

    rows = st.session_state.cgpa_rows
    semesters = []

    for i in range(rows):
        a, b, c = st.columns(3)
        with a:
            sem_no = st.number_input(
                "Semester",
                min_value=1,
                max_value=20,
                value=i + 1,
                step=1,
                key=key("cgpa", i, "sem"),
                label_visibility="collapsed",
            )
        with b:
            gpa = st.number_input(
                "GPA",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                key=key("cgpa", i, "gpa"),
                label_visibility="collapsed",
            )
        with c:
            credits = st.number_input(
                "Credits",
                min_value=1,
                max_value=50,
                value=20,
                step=1,
                key=key("cgpa", i, "credits"),
                label_visibility="collapsed",
            )
        semesters.append(Semester(semester_no=int(sem_no), gpa=float(gpa), credits=int(credits))) # type: ignore

    b1, b2, b3 = st.columns(3)
    if b1.button("➕ Add Semester", key="cgpa_add_semester", use_container_width=True):
        add_row("cgpa")
        st.rerun()
    if b2.button("➖ Remove Last", key="cgpa_remove_semester", use_container_width=True, disabled=rows <= 1):
        remove_row("cgpa")
        st.rerun()
    if b3.button("↺ Reset", key="cgpa_reset", use_container_width=True):
        reset_form("cgpa")
        st.rerun()

    if st.button("Calculate CGPA", key="calculate_cgpa", type="primary", use_container_width=True):
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

    result = st.session_state.cgpa_result
    if result:
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("CGPA calculated successfully.")
            m1, m2, m3 = st.columns(3)
            m1.metric("CGPA", f"{result['cgpa']:.2f}")
            m2.metric("Percentage", f"{result['percentage']:.2f}%")
            m3.metric("Credits", f"{result['credits']}")

            rows_csv = [[s.semester_no, f"{s.gpa:.2f}", s.credits] for s in result["rows"]] # type: ignore
            st.download_button(
                "Download CGPA CSV",
                data=csv_bytes(["Semester", "GPA", "Credits"], rows_csv),
                file_name="cgpa_result.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_cgpa_csv",
            )

            with st.expander("View breakdown"):
                st.dataframe(
                    [
                        {"Semester": s.semester_no, "GPA": f"{s.gpa:.2f}", "Credits": s.credits} # type: ignore
                        for s in result["rows"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

def render_grade_scale() -> None:
    st.subheader("Grade Scale")
    st.dataframe(
        [{"Grade": grade, "Points": points} for grade, points in GRADE_POINTS.items()],
        use_container_width=True,
        hide_index=True,
    )

def main() -> None:
    init_state()
    header_block()

    tab1, tab2, tab3 = st.tabs(["GPA Calculator", "CGPA Calculator", "Grade Scale"])
    with tab1:
        render_gpa_tab()
    with tab2:
        render_cgpa_tab()
    with tab3:
        render_grade_scale()

    st.divider()
    st.caption("Built with Python and Streamlit.")

if __name__ == "__main__":
    main()
