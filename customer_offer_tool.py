import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Customer Offer Generator", layout="centered")
st.title("Bob Ruth Ford - Vehicle Purchase Offer Generator")

# Input form
with st.form("offer_form"):
    customer_name = st.text_input("Customer Name", "Rob Dell")
    vehicle = st.text_input("Year / Make / Model", "2024 Ford Lightning")
    vin = st.text_input("VIN", "1FT6W7L72RWG24659")
    mileage = st.number_input("Mileage", value=2859)
    offer_price = st.number_input("Offer Price ($)", value=52000)
    expiration_date = st.date_input("Offer Expiration Date", value=datetime(2025, 8, 15))
    submitted = st.form_submit_button("Generate Offer PDF")

# PDF generation logic
class OfferPDF(FPDF):
    def header(self):
        if os.path.exists("BRFLOGONEW.jpg"):
            self.image("BRFLOGONEW.jpg", 10, 8, 50)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Vehicle Purchase Offer", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Thank you for servicing your vehicle with Bob Ruth Ford.", 0, 0, "C")

    def content(self, customer_name, vehicle, vin, mileage, offer_price, expiration_date):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Dear {customer_name},", ln=True)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, (
            "We appreciate your continued trust in Bob Ruth Ford for your service needs. "
            "After evaluating your vehicle during your recent visit, we would like to extend a purchase offer as outlined below."
        ))
        self.ln(5)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Vehicle Details", ln=True)
        self.set_font("Arial", "", 12)
        self.cell(50, 10, "Year/Make/Model:", border=0)
        self.cell(0, 10, vehicle, ln=True)
        self.cell(50, 10, "VIN:", border=0)
        self.cell(0, 10, vin, ln=True)
        self.cell(50, 10, "Mileage:", border=0)
        self.cell(0, 10, f"{mileage:,} miles", ln=True)
        self.ln(5)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Offer Details", ln=True)
        self.set_font("Arial", "", 12)
        self.cell(50, 10, "Offer Price:", border=0)
        self.cell(0, 10, f"${offer_price:,.2f}", ln=True)
        self.cell(50, 10, "Offer Valid Until:", border=0)
        self.cell(0, 10, expiration_date.strftime('%Y-%m-%d'), ln=True)
        self.ln(10)

        self.multi_cell(0, 10, (
            "If you are interested in taking advantage of this offer or would like to discuss your options, "
            "please contact your service advisor or a member of our sales team. We would be happy to assist you."
        ))
        self.ln(10)

        self.cell(0, 10, "______________________________", ln=True)
        self.cell(0, 6, "Customer Signature", ln=True)

if submitted:
    pdf = OfferPDF()
    pdf.add_page()
    pdf.content(customer_name, vehicle, vin, mileage, offer_price, expiration_date)
    output_path = f"{customer_name.replace(' ', '_')}_Offer.pdf"
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        st.download_button(
            label="Download Offer PDF",
            data=f.read(),
            file_name=output_path,
            mime="application/pdf"
        )
