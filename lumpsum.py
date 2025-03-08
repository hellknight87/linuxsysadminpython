def calculate_lumpsum_future_value(principal, rate_of_return, years_to_invest, compounding_frequency=12):
    """Calculates the future value of a lump sum investment with monthly compounding."""
    return principal * (1 + rate_of_return / compounding_frequency) ** (compounding_frequency * years_to_invest)

def format_indian_numbering_system(amount):
    """Formats the amount as per the Indian numbering system (lakhs, crores, etc.)."""
    # Split the amount into integer and decimal parts
    integer_part, decimal_part = str(amount).split(".")
    
    # Add commas to the integer part for Indian numbering system
    if len(integer_part) > 3:
        integer_part = integer_part[::-1]  # Reverse the string
        integer_part = ','.join([integer_part[i:i+2] for i in range(0, len(integer_part), 2)])  # Add commas
        integer_part = integer_part[::-1]  # Reverse back to original order
    
    # Combine integer part and decimal part
    return f"{integer_part}.{decimal_part}"

def main():
    # Take input values from the user
    lump_sum_amount = float(input("Enter the lump-sum investment amount: ₹"))
    roi_annual = float(input("Enter the annual return on investment (ROI) in percentage: ")) / 100
    years = int(input("Enter the investment period (in years): "))
    
    # Compounding frequency (monthly = 12)
    compounding_frequency = 12
    
    # Calculate maturity value using the compound interest formula for monthly compounding
    total_maturity_value = calculate_lumpsum_future_value(lump_sum_amount, roi_annual, years, compounding_frequency)

    # Output the results
    print(f"\nTotal Invested Amount: ₹{format_indian_numbering_system(lump_sum_amount)}")
    print(f"Total Maturity Value: ₹{format_indian_numbering_system(total_maturity_value)}")

# Run the main function
if __name__ == "__main__":
    main()
