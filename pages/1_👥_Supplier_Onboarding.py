import streamlit as st

st.title("👥 Supplier Onboarding")

tab1, tab2 = st.tabs([
    "Supplier Onboarding",
    "Sample Guide for Questionnaire"
])

with tab1:
    st.subheader("Supplier Onboarding")

    modules = {
        "Module 1: Welcome": [
            "Company overview",
            "Vision and mission",
            "Products and services",
            "Seller journey",
            "Roles and responsibilities",
            "Support channels"
        ],
        "Module 2: Seller Registration": [
            "Eligibility criteria",
            "Registration process",
            "Required documents",
            "Business verification",
            "KYC/KYB requirements",
            "Approval timelines"
        ],
        "Module 3: Platform Navigation": [
            "Dashboard overview",
            "Profile management",
            "Product catalog (if applicable)",
            "Pricing",
            "Inventory management",
            "Orders",
            "Reports"
        ],
        "Module 4: Finance Basics": [
            "Settlements",
            "Settlement cycle",
            "Payment methods",
            "Transaction lifecycle",
            "Refund process",
            "Chargebacks",
            "Failed transactions",
            "Taxes",
            "Invoices"
        ],
        "Module 5: Compliance": [
            "KYC",
            "AML basics",
            "Fraud prevention",
            "Data privacy",
            "Information security",
            "Regulatory compliance",
            "Acceptable Use Policy"
        ],
        "Module 6: Seller Operations": [
            "Order lifecycle",
            "Returns",
            "Cancellations",
            "Escalations",
            "Dispute handling",
            "Customer communication"
        ],
        "Module 7: Best Practices": [
            "Improving seller performance",
            "Reducing cancellations",
            "Managing inventory",
            "Maintaining service quality",
            "Customer satisfaction"
        ],
        "Module 8: Support": [
            "Contact channels",
            "SLAs",
            "Escalation matrix",
            "Self-help resources",
            "FAQs"
        ]
    }

    for module, topics in modules.items():
        with st.expander(module):
            for topic in topics:
                st.write(f"• {topic}")

with tab2:
    st.subheader("Sample Guide for Questionnaire")
    st.info("Still Under Construction!")
