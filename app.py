import json
import random
import string
from pathlib import Path

import streamlit as st


# =========================================================
# BANK CLASS
# =========================================================

class Bank:

    DATABASE = "data.json"

    @classmethod
    def load_data(cls):
        """Load bank data from JSON file."""
        try:
            if Path(cls.DATABASE).exists():

                with open(cls.DATABASE, "r") as file:
                    data = json.load(file)

                    if isinstance(data, list):
                        return data

            return []

        except (json.JSONDecodeError, OSError):
            return []

    @classmethod
    def save_data(cls, data):
        """Save bank data to JSON file."""
        try:

            with open(cls.DATABASE, "w") as file:
                json.dump(data, file, indent=4)

            return True

        except OSError:
            return False

    @staticmethod
    def generate_account_number(existing_accounts):
        """Generate a unique account number."""

        characters = string.ascii_uppercase + string.digits

        while True:

            account_number = "".join(
                random.choices(characters, k=8)
            )

            if account_number not in existing_accounts:
                return account_number

    @staticmethod
    def find_account(data, account_number, pin):
        """Find account using account number and PIN."""

        for account in data:

            if (
                account["accountNo"] == account_number
                and account["pin"] == pin
            ):
                return account

        return None

    @staticmethod
    def find_account_by_email_and_pin(data, email, pin):
        """Find account using email and PIN."""

        for account in data:

            if (
                account["email"] == email
                and account["pin"] == pin
            ):
                return account

        return None


# =========================================================
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Python Bank",
    page_icon=None,
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

if "bank_data" not in st.session_state:
    st.session_state.bank_data = Bank.load_data()


data = st.session_state.bank_data


# =========================================================
# HEADER
# =========================================================

st.title("Python Bank")

st.caption(
    "Banking Management System using Python and Streamlit"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Banking Menu")

menu = st.sidebar.radio(
    "Select Operation",
    [
        "Home",
        "Create Account",
        "Get Account Number",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Account",
        "Delete Account"
    ]
)


# =========================================================
# HOME
# =========================================================

if menu == "Home":

    st.header("Welcome to Python Bank")

    total_accounts = len(data)

    total_balance = sum(
        account.get("balance", 0)
        for account in data
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Accounts",
            total_accounts
        )

    with col2:

        st.metric(
            "Total Bank Balance",
            f"₹{total_balance:,.2f}"
        )

    with col3:

        st.metric(
            "System Status",
            "Online"
        )

    st.divider()

    st.subheader("Available Services")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            Account Management

            - Create Account
            - Get Account Number
            - View Account
            - Update Account
            - Delete Account
            """
        )

    with col2:

        st.success(
            """
            Banking Services

            - Deposit Money
            - Withdraw Money
            - Check Balance
            - Persistent JSON Storage
            """
        )


# =========================================================
# CREATE ACCOUNT
# =========================================================

elif menu == "Create Account":

    st.header("Create New Account")

    with st.form("create_account_form"):

        name = st.text_input(
            "Full Name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            step=1
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "4-Digit PIN",
            type="password",
            max_chars=4
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Create Account"
        )

    if submit:

        if not name.strip():

            st.error(
                "Please enter your name."
            )

        elif age < 18:

            st.error(
                "You must be at least 18 years old."
            )

        elif not email.strip() or "@" not in email:

            st.error(
                "Please enter a valid email address."
            )

        elif any(
            account["email"].lower() == email.strip().lower()
            for account in data
        ):

            st.error(
                "An account with this email already exists."
            )

        elif len(pin) != 4 or not pin.isdigit():

            st.error(
                "PIN must contain exactly 4 digits."
            )

        elif pin != confirm_pin:

            st.error(
                "PINs do not match."
            )

        else:

            existing_accounts = [
                account["accountNo"]
                for account in data
            ]

            account_number = Bank.generate_account_number(
                existing_accounts
            )

            new_account = {

                "name": name.strip(),

                "age": int(age),

                "email": email.strip(),

                "pin": pin,

                "accountNo": account_number,

                "balance": 0.0
            }

            data.append(new_account)

            if Bank.save_data(data):

                st.success(
                    "Account created successfully."
                )

                st.subheader(
                    "Account Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"Name: {name}"
                    )

                    st.write(
                        f"Age: {age}"
                    )

                    st.write(
                        f"Email: {email}"
                    )

                with col2:

                    st.write(
                        f"Account Number: {account_number}"
                    )

                    st.write(
                        "Initial Balance: ₹0.00"
                    )

                st.warning(
                    "Please save your account number safely."
                )

            else:

                st.error(
                    "Unable to save account."
                )


# =========================================================
# GET ACCOUNT NUMBER
# =========================================================

elif menu == "Get Account Number":

    st.header("Get Account Number")

    st.write(
        "Enter your registered email and PIN "
        "to find your account number."
    )

    with st.form("get_account_form"):

        email = st.text_input(
            "Registered Email"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Get Account Number"
        )

    if submit:

        if not email.strip():

            st.error(
                "Please enter your email."
            )

        elif len(pin) != 4 or not pin.isdigit():

            st.error(
                "Please enter a valid 4-digit PIN."
            )

        else:

            account = Bank.find_account_by_email_and_pin(
                data,
                email.strip(),
                pin
            )

            if account:

                st.success(
                    "Account found successfully."
                )

                st.subheader(
                    "Account Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"Name: {account['name']}"
                    )

                    st.write(
                        f"Email: {account['email']}"
                    )

                with col2:

                    st.write(
                        f"Account Number: {account['accountNo']}"
                    )

            else:

                st.error(
                    "No account found with the provided "
                    "email and PIN."
                )


# =========================================================
# DEPOSIT MONEY
# =========================================================

elif menu == "Deposit Money":

    st.header("Deposit Money")

    with st.form("deposit_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Deposit Amount",
            min_value=0.01,
            step=100.0
        )

        submit = st.form_submit_button(
            "Deposit Money"
        )

    if submit:

        account = Bank.find_account(
            data,
            account_number.strip().upper(),
            pin
        )

        if not account:

            st.error(
                "Invalid account number or PIN."
            )

        elif amount > 10000:

            st.error(
                "Maximum deposit allowed is ₹10,000."
            )

        else:

            account["balance"] += amount

            if Bank.save_data(data):

                st.success(
                    f"₹{amount:,.2f} deposited successfully."
                )

                st.metric(
                    "New Balance",
                    f"₹{account['balance']:,.2f}"
                )

            else:

                st.error(
                    "Unable to save transaction."
                )


# =========================================================
# WITHDRAW MONEY
# =========================================================

elif menu == "Withdraw Money":

    st.header("Withdraw Money")

    with st.form("withdraw_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0.01,
            step=100.0
        )

        submit = st.form_submit_button(
            "Withdraw Money"
        )

    if submit:

        account = Bank.find_account(
            data,
            account_number.strip().upper(),
            pin
        )

        if not account:

            st.error(
                "Invalid account number or PIN."
            )

        elif amount > account["balance"]:

            st.error(
                "Insufficient balance."
            )

        else:

            account["balance"] -= amount

            if Bank.save_data(data):

                st.success(
                    f"₹{amount:,.2f} withdrawn successfully."
                )

                st.metric(
                    "Remaining Balance",
                    f"₹{account['balance']:,.2f}"
                )

            else:

                st.error(
                    "Unable to save transaction."
                )


# =========================================================
# ACCOUNT DETAILS
# =========================================================

elif menu == "Account Details":

    st.header("Account Details")

    with st.form("details_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "View Account"
        )

    if submit:

        account = Bank.find_account(
            data,
            account_number.strip().upper(),
            pin
        )

        if not account:

            st.error(
                "Invalid account number or PIN."
            )

        else:

            st.success(
                "Account found successfully."
            )

            st.subheader(
                "Account Information"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"Name: {account['name']}"
                )

                st.write(
                    f"Age: {account['age']}"
                )

                st.write(
                    f"Email: {account['email']}"
                )

            with col2:

                st.write(
                    f"Account Number: {account['accountNo']}"
                )

                st.write(
                    f"Balance: ₹{account['balance']:,.2f}"
                )

                st.write(
                    "PIN: ****"
                )


# =========================================================
# UPDATE ACCOUNT
# =========================================================

elif menu == "Update Account":

    st.header("Update Account")

    with st.form("update_login_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Verify Account"
        )

    if submit:

        account = Bank.find_account(
            data,
            account_number.strip().upper(),
            pin
        )

        if not account:

            st.error(
                "Invalid account number or PIN."
            )

        else:

            st.session_state["update_account"] = account

            st.rerun()

    if "update_account" in st.session_state:

        account = st.session_state["update_account"]

        st.divider()

        st.subheader(
            "Update Your Information"
        )

        with st.form("update_account_form"):

            new_name = st.text_input(
                "Name",
                value=account["name"]
            )

            new_email = st.text_input(
                "Email",
                value=account["email"]
            )

            new_pin = st.text_input(
                "New PIN",
                type="password",
                max_chars=4
            )

            update = st.form_submit_button(
                "Update Account"
            )

        if update:

            if not new_name.strip():

                st.error(
                    "Name cannot be empty."
                )

            elif not new_email.strip() or "@" not in new_email:

                st.error(
                    "Enter a valid email."
                )

            elif new_pin and (
                len(new_pin) != 4
                or not new_pin.isdigit()
            ):

                st.error(
                    "PIN must contain exactly 4 digits."
                )

            else:

                account["name"] = new_name.strip()

                account["email"] = new_email.strip()

                if new_pin:

                    account["pin"] = new_pin

                if Bank.save_data(data):

                    st.success(
                        "Account updated successfully."
                    )

                    del st.session_state["update_account"]

                    st.rerun()


# =========================================================
# DELETE ACCOUNT
# =========================================================

elif menu == "Delete Account":

    st.header("Delete Account")

    with st.form("delete_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        confirm = st.checkbox(
            "I understand that this action cannot be undone."
        )

        submit = st.form_submit_button(
            "Delete Account"
        )

    if submit:

        account = Bank.find_account(
            data,
            account_number.strip().upper(),
            pin
        )

        if not account:

            st.error(
                "Invalid account number or PIN."
            )

        elif not confirm:

            st.warning(
                "Please confirm account deletion."
            )

        elif account["balance"] > 0:

            st.error(
                "You cannot delete an account "
                "with a remaining balance."
            )

        else:

            data.remove(account)

            if Bank.save_data(data):

                st.success(
                    "Account deleted successfully."
                )

            else:

                st.error(
                    "Unable to delete account."
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Python Bank | Built with Python, JSON and Streamlit"
)
