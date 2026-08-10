import streamlit as st
import stripe
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from simulation.engine import (
    get_random_stock_and_fractional_shares,
    create_timeline,
    save_purchase,
    load_purchases
)

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

st.set_page_config(page_title="AI Stock Simulator", layout="centered")

st.title("AI Stock Simulator")
st.caption("Educational simulation only • No real trades • Stripe test mode")

# ========== KYC SECTION ==========
st.sidebar.header("Identity Verification (KYC Demo)")

if "kyc_verified" not in st.session_state:
    st.session_state.kyc_verified = False

if not st.session_state.kyc_verified:
    with st.sidebar.form("kyc_form"):
        st.write("Complete this form to unlock trading:")
        full_name = st.text_input("Full Legal Name")
        email = st.text_input("Email Address")
        dob = st.date_input("Date of Birth")
        country = st.selectbox("Country", ["United States", "Canada", "United Kingdom", "Other"])

        submitted = st.form_submit_button("Submit KYC")

        if submitted:
            if full_name and email:
                st.session_state.kyc_verified = True
                st.session_state.kyc_name = full_name
                st.success("KYC Approved (Demo)")
                st.rerun()
            else:
                st.error("Please fill in at least Name and Email")
else:
    st.sidebar.success("KYC Verified ✓")
    st.sidebar.write(f"**Name:** {st.session_state.kyc_name}")
    st.sidebar.caption("Identity check passed (simulation only)")

# ========== MAIN CONTENT ==========
if st.session_state.kyc_verified:
    st.subheader("Buy a Random AI Stock")
    st.write("You’ll receive a random fractional share from across the AI infrastructure stack including GPUs, networking, photonics, memory, power systems, and semiconductor equipment.")

    if st.button("Buy a Random AI Stock – $25", type="primary"):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Random AI Stock Purchase (Demo)"
                        },
                        "unit_amount": 2500,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="http://localhost:8501?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:8501?canceled=true",
            )
            st.markdown(f"[Click here to complete payment with Stripe]({session.url})")
        except Exception as e:
            st.error(f"Stripe error: {e}")
else:
    st.warning("Please complete the KYC form in the sidebar before you can buy a stock.")

# Handle successful payment
query_params = st.query_params
if query_params.get("success") == "true":
    session_id = query_params.get("session_id")

    if session_id and "processed_session" not in st.session_state:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                purchase = get_random_stock_and_fractional_shares(25.0)
                timeline = create_timeline(purchase)
                save_purchase(purchase, timeline)

                st.session_state["processed_session"] = session_id
                st.success("Payment successful! Random AI stock purchased.")
                st.balloons()
        except Exception as e:
            st.error(f"Could not verify payment: {e}")

# ========== PORTFOLIO SECTION ==========
st.divider()
st.subheader("Your Portfolio")

purchases = load_purchases()

if not purchases:
    st.info("No positions yet. Complete KYC and buy a random AI stock to get started.")
else:
    for p in reversed(purchases):
        trade_date = p['timestamp'][:10]
        trade_dt = datetime.fromisoformat(p['timestamp'])
        settlement_date = (trade_dt + timedelta(days=1)).strftime('%Y-%m-%d')

        with st.expander(f"{p['ticker']} — {p['shares']} shares @ ${p['price']}  •  {p['status']}"):
            st.write(f"**Total invested:** ${p['total']}")
            st.write(f"**Trade Date:** {trade_date}")
            st.write(f"**Settlement Date (T+1):** {settlement_date}")
            st.write(f"**Status:** {p['status']}")
            
            st.write("### Settlement Timeline • Brokerage Flow Simulator")
            for event in p["timeline"]:
                st.markdown(f"- `{event['time']}` — {event['event']}")
