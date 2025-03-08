def calculate_sip_future_value_monthly(principal, rate_of_return, months_to_invest):
    """Corrected future value formula without excessive compounding."""
    if rate_of_return == 0:
        return principal * months_to_invest
    return principal * ((1 + rate_of_return) ** months_to_invest - 1) / rate_of_return


def main():
    # Take input values from the user
    sip_amount = float(input("Enter the monthly SIP amount (₹): "))
    step_up_rate = float(input("Enter the annual step-up rate (in percentage): ")) / 100
    roi_annual = float(input("Enter the annual return on investment (ROI in percentage): ")) / 100
    years = int(input("Enter the investment period (in years): "))

    # Monthly ROI calculation
    roi_monthly = roi_annual / 12  # Convert annual ROI to monthly ROI
    total_months = years * 12  # Total number of months

    # Initialize variables for total investment and maturity value
    total_invested = 0
    total_maturity_value = 0

    for i in range(years):
        # Adjust SIP for this year with step-up increment
        sip_monthly = sip_amount * ((1 + step_up_rate) ** i)
        # Total invested for this year
        total_invested += sip_monthly * 12
        # Future value of the SIP with monthly compounding
        future_value = calculate_sip_future_value_monthly(sip_monthly, roi_monthly, (years - i) * 12)
        total_maturity_value += future_value

    # Output results
    print(f"\nTotal Invested Amount: ₹{total_invested:.2f}")
    print(f"Total Maturity Value: ₹{total_maturity_value:.2f}")

# Run the main function
if __name__ == "__main__":
    main()
