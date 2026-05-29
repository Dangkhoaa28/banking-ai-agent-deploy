import streamlit as st
import httpx
import os
import json

st.set_page_config(page_title="Banking AI Agent", page_icon="🏦", layout="centered")

BACKEND_URL = os.getenv("API_BASE_URL", "http://banking-backend:8000")

st.title("🏦 Banking AI Agent")
st.markdown("Enter your customer request below.")

message = st.text_area("Customer Message", "I lost my credit card yesterday, what should I do?")

if st.button("Submit"):
    with st.spinner("Processing request..."):
        try:
            response = httpx.post(
                f"{BACKEND_URL}/run-agent",
                json={"message": message, "customer_id": "test_user"},
                timeout=120.0
            )
            response.raise_for_status()
            result = response.json()
            
            st.markdown("### Results")
            
            # Badge colors based on priority
            priority_color = "red" if result["priority"] == "HIGH" else "orange" if result["priority"] == "MEDIUM" else "green"
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Intent**: {result['intent']} (Conf: {result['confidence']:.2f})")
            with col2:
                st.markdown(f"**Priority Level**: <span style='color:{priority_color}; font-weight:bold;'>{result['priority']}</span>", unsafe_allow_html=True)
                
            st.markdown("#### Draft Reply")
            st.success(result["draft_reply"])
            
            st.markdown("#### Details")
            st.write("**Missing Information:**", ", ".join(result["missing_info"]) if result["missing_info"] else "None")
            st.write("**Next Action:**", result["next_action"])
            st.write(f"**Processing Time:** {result['processing_time']}s")
            
        except httpx.HTTPStatusError as e:
            st.error(f"HTTP Error: {e.response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
