import streamlit as st
import pandas as pd
from utils.auditor import load_data_to_sqlite, run_sql_audits

st.set_page_config(
    page_title="Database Data-Quality & Inconsistency Auditor",
    page_icon="🔍",
    layout="wide"
)

st.title("Database Data-Quality & Inconsistency Auditor")
st.markdown("Automated data validation pipeline connecting to organizational records to flag incomplete metadata, duplicates, and formatting errors.")

conn, df = load_data_to_sqlite()
audit_results = run_sql_audits(conn)

tab1, tab2, tab3, tab4 = st.tabs(["Data Health Overview", "Incomplete / Missing Metadata", "Duplicate Records", "Formatting & Syntax Errors"])

with tab1:
    st.header("Database Health Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records Audited", len(df))
    with col2:
        st.metric("Incomplete Records", len(audit_results["missing_data"]))
    with col3:
        st.metric("Duplicate Entries", len(audit_results["duplicates"]))
    with col4:
        st.metric("Formatting Errors", len(audit_results["formatting_errors"]))
        
    st.subheader("Raw Dataset Preview")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.header("Incomplete or Missing Metadata")
    st.markdown("Identifies records missing critical information such as contact names, valid grant amounts, or designated regions.")
    missing_df = audit_results["missing_data"]
    if not missing_df.empty:
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("No incomplete or missing metadata detected.")

with tab3:
    st.header("Duplicate Record Detector")
    st.markdown("Flags grant applications or contact entries submitted multiple times with identical parameters.")
    dup_df = audit_results["duplicates"]
    if not dup_df.empty:
        st.dataframe(dup_df, use_container_width=True)
    else:
        st.success("No duplicate records detected.")

with tab4:
    st.header("Formatting & Validation Errors")
    st.markdown("Detects invalid email syntax, malformed phone numbers, or structural discrepancies.")
    fmt_df = audit_results["formatting_errors"]
    if not fmt_df.empty:
        st.dataframe(fmt_df, use_container_width=True)
    else:
        st.success("No formatting errors detected.")
