"""
CIT3003 - Analysis of Algorithms
Retirement Investment Optimization - Main Application

Group Members:
Rushane Green - 2006930
Shavon Gordon - 2306989
Halmareo Francis - 2002360
Khadejah Benjamin - 2208656

Date: November 21, 2025

This is the main user interface that integrates all retirement simulation algorithms.
Provides a menu-driven CLI with input validation and formatted output.
"""

import sys
from retirement_algorithms import (
    fixedInvestor,
    variableInvestor,
    finallyRetired,
    maximumExpensed,
    format_currency,
    format_percentage
)


# ============================================
# COLOR SCHEME - Finance Professional Theme
# ============================================

class Colors:
    """ANSI color codes for terminal styling."""
    # Primary: Deep Navy Blue
    NAVY = '\033[38;5;17m'        # Deep navy blue text
    NAVY_BG = '\033[48;5;17m'     # Navy background
    
    # Secondary: Gold/Yellow
    GOLD = '\033[38;5;220m'       # Gold text
    GOLD_BOLD = '\033[1;38;5;220m'  # Bold gold
    
    # Utility colors
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Combined styles
    HEADER = NAVY_BG + GOLD_BOLD
    TITLE = GOLD_BOLD
    MENU_ITEM = NAVY
    SUCCESS = GREEN
    ERROR = RED
    PROMPT = CYAN


# ============================================
# DISPLAY FUNCTIONS
# ============================================

def clear_screen():
    """Clear terminal screen (works on Windows/Unix)."""
    print("\n" * 50)  # Simple clear by printing newlines


def print_header():
    """Display application header with branding."""
    width = 80
    clear_screen()
    
    print(Colors.HEADER + "=" * width + Colors.RESET)
    print(Colors.HEADER + " " * width + Colors.RESET)
    print(Colors.HEADER + 
          "        🏦  RETIREMENT INVESTMENT OPTIMIZATION SYSTEM  💰        ".center(width) +
          Colors.RESET)
    print(Colors.HEADER + 
          "                  AofA Financial Services Ltd.                  ".center(width) +
          Colors.RESET)
    print(Colors.HEADER + " " * width + Colors.RESET)
    print(Colors.HEADER + "=" * width + Colors.RESET)
    print()


def print_divider(char="─", length=80, color=Colors.NAVY):
    """Print a styled divider line."""
    print(color + char * length + Colors.RESET)


def print_section_title(title):
    """Print a section title with gold styling."""
    print()
    print(Colors.TITLE + "▶ " + title.upper() + Colors.RESET)
    print_divider("─", 80, Colors.GOLD)
    print()


def print_menu():
    """Display main menu options."""
    print_header()
    print(Colors.TITLE + "MAIN MENU" + Colors.RESET)
    print_divider()
    print()
    
    menu_items = [
        ("1", "Fixed Rate Investment Simulator", "Constant annual growth rate"),
        ("2", "Variable Rate Investment Simulator", "Different rates each year"),
        ("3", "Retirement Fund Depletion Calculator", "Years until funds depleted"),
        ("4", "Optimal Withdrawal Optimizer", "Binary search for max withdrawal"),
        ("5", "View Project Information", "About this application"),
        ("6", "Exit", "Quit the program"),
    ]
    
    for number, title, description in menu_items:
        print(f"  {Colors.GOLD}[{number}]{Colors.RESET} "
              f"{Colors.NAVY + Colors.BOLD}{title}{Colors.RESET}")
        print(f"      {Colors.WHITE}↳ {description}{Colors.RESET}")
        print()
    
    print_divider()


def print_result_box(title, content):
    """Display results in a formatted box."""
    width = 76
    print()
    print(Colors.GOLD + "┌" + "─" * width + "┐" + Colors.RESET)
    print(Colors.GOLD + "│" + Colors.RESET + 
          Colors.TITLE + f" 📊 {title}".center(width) + Colors.RESET + 
          Colors.GOLD + "│" + Colors.RESET)
    print(Colors.GOLD + "├" + "─" * width + "┤" + Colors.RESET)
    
    for line in content:
        # Pad line to fit box width
        display_line = str(line).ljust(width)
        print(Colors.GOLD + "│" + Colors.RESET + 
              " " + display_line + Colors.GOLD + "│" + Colors.RESET)
    
    print(Colors.GOLD + "└" + "─" * width + "┘" + Colors.RESET)
    print()


def print_success(message):
    """Print success message."""
    print(Colors.SUCCESS + "✓ " + message + Colors.RESET)


def print_error(message):
    """Print error message."""
    print(Colors.ERROR + "✗ ERROR: " + message + Colors.RESET)


def print_info(message):
    """Print informational message."""
    print(Colors.CYAN + "ℹ " + message + Colors.RESET)


# ============================================
# INPUT VALIDATION FUNCTIONS
# ============================================

def get_float_input(prompt, min_value=None, max_value=None, allow_zero=False):
    """
    Get and validate float input from user.
    
    Parameters:
        prompt (str): Input prompt message
        min_value (float): Minimum acceptable value (None = no minimum)
        max_value (float): Maximum acceptable value (None = no maximum)
        allow_zero (bool): Whether zero is acceptable
    
    Returns:
        float: Validated user input
    """
    while True:
        try:
            user_input = input(Colors.PROMPT + prompt + Colors.RESET).strip()
            
            # Allow user to cancel
            if user_input.lower() in ['q', 'quit', 'cancel']:
                return None
            
            value = float(user_input)
            
            # Check zero constraint
            if not allow_zero and value == 0:
                print_error("Value cannot be zero. Please try again.")
                continue
            
            # Check minimum constraint
            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}. Please try again.")
                continue
            
            # Check maximum constraint
            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}. Please try again.")
                continue
            
            return value
            
        except ValueError:
            print_error("Invalid input. Please enter a numeric value.")
        except KeyboardInterrupt:
            print("\n" + Colors.ERROR + "Input cancelled." + Colors.RESET)
            return None


def get_int_input(prompt, min_value=None, max_value=None):
    """
    Get and validate integer input from user.
    
    Parameters:
        prompt (str): Input prompt message
        min_value (int): Minimum acceptable value
        max_value (int): Maximum acceptable value
    
    Returns:
        int: Validated user input
    """
    while True:
        try:
            user_input = input(Colors.PROMPT + prompt + Colors.RESET).strip()
            
            # Allow user to cancel
            if user_input.lower() in ['q', 'quit', 'cancel']:
                return None
            
            value = int(user_input)
            
            # Check minimum constraint
            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}. Please try again.")
                continue
            
            # Check maximum constraint
            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}. Please try again.")
                continue
            
            return value
            
        except ValueError:
            print_error("Invalid input. Please enter a whole number.")
        except KeyboardInterrupt:
            print("\n" + Colors.ERROR + "Input cancelled." + Colors.RESET)
            return None


def get_rate_list(num_years):
    """
    Get a list of annual rates from user.
    
    Parameters:
        num_years (int): Number of rates needed
    
    Returns:
        list of float: Annual rates as decimals
    """
    print_info(f"Enter the annual growth rate for each of {num_years} years.")
    print_info("Rates should be entered as percentages (e.g., 5 for 5%, -2 for -2%)")
    print()
    
    rates = []
    for year in range(1, num_years + 1):
        rate = get_float_input(
            f"  Year {year} rate (%): ",
            min_value=-100,
            max_value=1000
        )
        
        if rate is None:
            return None
        
        # Convert percentage to decimal
        rates.append(rate / 100.0)
    
    return rates


def get_menu_choice():
    """Get and validate menu choice."""
    choice = input(Colors.PROMPT + "\nEnter your choice [1-6]: " + Colors.RESET).strip()
    return choice


def pause():
    """Pause and wait for user to press Enter."""
    input(Colors.CYAN + "\nPress ENTER to continue..." + Colors.RESET)


# ============================================
# SIMULATION SCENARIOS
# ============================================

def scenario_fixed_investor():
    """Scenario 1: Fixed Rate Investment Simulation."""
    print_section_title("Fixed Rate Investment Simulator")
    
    print("This simulator calculates retirement savings growth with:")
    print("  • Constant annual contributions")
    print("  • Fixed interest rate")
    print("  • Compound growth over time")
    print()
    print_divider("─", 50, Colors.NAVY)
    print()
    
    # Collect inputs
    principal = get_float_input(
        "Annual contribution amount ($): ",
        min_value=0,
        max_value=1000000
    )
    if principal is None:
        return
    
    rate_percent = get_float_input(
        "Annual interest rate (%): ",
        min_value=-100,
        max_value=100
    )
    if rate_percent is None:
        return
    rate = rate_percent / 100.0
    
    years = get_int_input(
        "Number of years: ",
        min_value=1,
        max_value=100
    )
    if years is None:
        return
    
    # Run simulation
    try:
        print()
        print_info("Running simulation...")
        
        final_balance = fixedInvestor(principal, rate, years)
        
        # Calculate additional metrics
        total_contributions = principal * years
        total_interest = final_balance - total_contributions
        
        # Display results
        results = [
            f"Annual Contribution:     {format_currency(principal)}",
            f"Interest Rate:           {format_percentage(rate)}",
            f"Investment Period:       {years} years",
            "",
            f"Total Contributed:       {format_currency(total_contributions)}",
            f"Total Interest Earned:   {format_currency(total_interest)}",
            "",
            f"{Colors.GOLD}FINAL BALANCE:           {format_currency(final_balance)}{Colors.RESET}",
        ]
        
        print_result_box("FIXED RATE INVESTMENT RESULTS", results)
        print_success("Simulation completed successfully!")
        
    except Exception as e:
        print_error(f"Simulation failed: {str(e)}")
    
    pause()


def scenario_variable_investor():
    """Scenario 2: Variable Rate Investment Simulation."""
    print_section_title("Variable Rate Investment Simulator")
    
    print("This simulator calculates investment growth with:")
    print("  • Initial lump sum investment")
    print("  • Different interest rates each year")
    print("  • Compound growth with variable rates")
    print()
    print_divider("─", 50, Colors.NAVY)
    print()
    
    # Collect inputs
    principal = get_float_input(
        "Initial investment amount ($): ",
        min_value=0,
        max_value=10000000
    )
    if principal is None:
        return
    
    num_years = get_int_input(
        "Number of years to simulate: ",
        min_value=1,
        max_value=50
    )
    if num_years is None:
        return
    
    print()
    rates = get_rate_list(num_years)
    if rates is None:
        return
    
    # Run simulation
    try:
        print()
        print_info("Running simulation...")
        
        final_balance = variableInvestor(principal, rates)
        
        # Calculate metrics
        total_growth = final_balance - principal
        average_rate = sum(rates) / len(rates)
        
        # Display results
        results = [
            f"Initial Investment:      {format_currency(principal)}",
            f"Investment Period:       {num_years} years",
            f"Average Rate:            {format_percentage(average_rate)}",
            "",
            f"Total Growth:            {format_currency(total_growth)}",
            f"Growth Percentage:       {format_percentage(total_growth / principal)}",
            "",
            f"{Colors.GOLD}FINAL BALANCE:           {format_currency(final_balance)}{Colors.RESET}",
        ]
        
        print_result_box("VARIABLE RATE INVESTMENT RESULTS", results)
        
        # Show year-by-year breakdown
        print(Colors.TITLE + "\n📈 YEAR-BY-YEAR BREAKDOWN:" + Colors.RESET)
        print_divider("─", 60, Colors.GOLD)
        
        balance = principal
        print(f"  Year 0:  {format_currency(balance):>15}  (Initial)")
        
        for year, rate in enumerate(rates, 1):
            balance = balance * (1 + rate)
            print(f"  Year {year}:  {format_currency(balance):>15}  "
                  f"(Rate: {format_percentage(rate)})")
        
        print_divider("─", 60, Colors.GOLD)
        print_success("Simulation completed successfully!")
        
    except Exception as e:
        print_error(f"Simulation failed: {str(e)}")
    
    pause()


def scenario_retirement_depletion():
    """Scenario 3: Retirement Fund Depletion Calculator."""
    print_section_title("Retirement Fund Depletion Calculator")
    
    print("This calculator determines:")
    print("  • How long retirement funds will last")
    print("  • Based on annual withdrawals")
    print("  • With continued investment growth")
    print()
    print_divider("─", 50, Colors.NAVY)
    print()
    
    # Collect inputs
    balance = get_float_input(
        "Starting retirement balance ($): ",
        min_value=0,
        max_value=100000000
    )
    if balance is None:
        return
    
    expense = get_float_input(
        "Annual withdrawal amount ($): ",
        min_value=0,
        max_value=balance
    )
    if expense is None:
        return
    
    rate_percent = get_float_input(
        "Expected annual return rate (%): ",
        min_value=-100,
        max_value=100
    )
    if rate_percent is None:
        return
    rate = rate_percent / 100.0
    
    # Run simulation
    try:
        print()
        print_info("Calculating retirement duration...")
        
        years_lasted = finallyRetired(balance, expense, rate)
        
        # Calculate metrics
        total_withdrawn = expense * years_lasted
        
        # Display results
        results = [
            f"Starting Balance:        {format_currency(balance)}",
            f"Annual Withdrawal:       {format_currency(expense)}",
            f"Expected Return Rate:    {format_percentage(rate)}",
            "",
            f"Total Amount Withdrawn:  {format_currency(total_withdrawn)}",
            "",
            f"{Colors.GOLD}RETIREMENT DURATION:     {years_lasted} years{Colors.RESET}",
        ]
        
        print_result_box("RETIREMENT FUND DEPLETION RESULTS", results)
        
        # Provide interpretation
        print(Colors.TITLE + "\n💡 INTERPRETATION:" + Colors.RESET)
        print_divider("─", 60, Colors.GOLD)
        
        if years_lasted == 0:
            print(Colors.RED + "  ⚠ WARNING: Insufficient funds for even one withdrawal!" + Colors.RESET)
        elif years_lasted < 10:
            print(Colors.RED + f"  ⚠ Funds will only last {years_lasted} years - consider reducing expenses." + Colors.RESET)
        elif years_lasted < 20:
            print(Colors.CYAN + f"  ℹ Funds will last {years_lasted} years - adequate for short retirement." + Colors.RESET)
        else:
            print(Colors.GREEN + f"  ✓ Funds will last {years_lasted} years - excellent sustainability!" + Colors.RESET)
        
        print_divider("─", 60, Colors.GOLD)
        print_success("Calculation completed successfully!")
        
    except Exception as e:
        print_error(f"Calculation failed: {str(e)}")
    
    pause()


def scenario_optimal_withdrawal():
    """Scenario 4: Optimal Withdrawal Optimizer (Binary Search)."""
    print_section_title("Optimal Withdrawal Optimizer")
    
    print("This optimizer uses BINARY SEARCH to find:")
    print("  • Maximum sustainable annual withdrawal")
    print("  • That lasts exactly your target retirement duration")
    print("  • Using successive approximation algorithm")
    print()
    print_divider("─", 50, Colors.NAVY)
    print()
    
    # Collect inputs
    balance = get_float_input(
        "Retirement fund balance ($): ",
        min_value=1,
        max_value=100000000
    )
    if balance is None:
        return
    
    rate_percent = get_float_input(
        "Expected annual return rate (%): ",
        min_value=-100,
        max_value=100
    )
    if rate_percent is None:
        return
    rate = rate_percent / 100.0
    
    target_years = get_int_input(
        "Target retirement duration (years): ",
        min_value=1,
        max_value=100
    )
    if target_years is None:
        return
    
    # Run optimization
    try:
        print()
        print_info("Running binary search optimization...")
        print_info("This may take a moment for large search spaces...")
        
        optimal_expense = maximumExpensed(balance, rate, target_years)
        
        # Verify the result
        actual_years = finallyRetired(balance, optimal_expense, rate)
        
        # Calculate metrics
        total_withdrawn = optimal_expense * target_years
        withdrawal_rate = (optimal_expense / balance) * 100
        
        # Display results
        results = [
            f"Starting Balance:        {format_currency(balance)}",
            f"Expected Return Rate:    {format_percentage(rate)}",
            f"Target Duration:         {target_years} years",
            "",
            f"Algorithm Used:          Binary Search (Successive Approximation)",
            f"Search Space:            $0 to {format_currency(balance)}",
            "",
            f"{Colors.GOLD}OPTIMAL WITHDRAWAL:      {format_currency(optimal_expense)}{Colors.RESET}",
            f"Withdrawal Rate:         {withdrawal_rate:.2f}% of balance",
            f"Total Over {target_years} Years:     {format_currency(total_withdrawn)}",
            "",
            f"Verification:            Lasts {actual_years} years (target: {target_years})",
        ]
        
        print_result_box("OPTIMAL WITHDRAWAL RESULTS", results)
        
        # Provide recommendations
        print(Colors.TITLE + "\n💡 FINANCIAL RECOMMENDATIONS:" + Colors.RESET)
        print_divider("─", 60, Colors.GOLD)
        
        monthly_withdrawal = optimal_expense / 12
        print(f"  • Monthly withdrawal:  {format_currency(monthly_withdrawal)}")
        
        if withdrawal_rate > 10:
            print(Colors.RED + f"  ⚠ High withdrawal rate ({withdrawal_rate:.1f}%) - consider growing balance first" + Colors.RESET)
        elif withdrawal_rate > 5:
            print(Colors.CYAN + f"  ℹ Moderate withdrawal rate ({withdrawal_rate:.1f}%) - monitor regularly" + Colors.RESET)
        else:
            print(Colors.GREEN + f"  ✓ Conservative withdrawal rate ({withdrawal_rate:.1f}%) - sustainable plan" + Colors.RESET)
        
        print_divider("─", 60, Colors.GOLD)
        print_success("Optimization completed successfully!")
        
    except Exception as e:
        print_error(f"Optimization failed: {str(e)}")
    
    pause()


def show_project_info():
    """Display project information and credits."""
    print_section_title("Project Information")
    
    info = [
        "CIT3003 - Analysis of Algorithms",
        "Semester 1, Academic Year 2025/2026",
        "University of Technology, Jamaica",
        "",
        "PROJECT: Retirement Investment Optimization",
        "         Using Algorithmic Design",
        "",
        "LECTURERS:",
        "  • Dr. Arnett Campbell",
        "  • Mr. Oral Robinson",
        "",
        "ALGORITHMS IMPLEMENTED:",
        "  1. Fixed Rate Compound Growth (Iterative)",
        "  2. Variable Rate Investment Simulation",
        "  3. Retirement Fund Depletion Modeling",
        "  4. Binary Search Optimization (Successive Approximation)",
        "",
        "TIME COMPLEXITY:",
        "  • Simulations: O(n) where n = years",
        "  • Optimization: O(log(balance) × target_years)",
        "",
        "DESIGN PARADIGM: Divide-and-Conquer",
        "",
        f"GROUP: [ Group Members:
        Rushane Green - 2006930
        Shavon Gordon - 2306989
        Halmareo Francis - 2002360
        Khadejah Benjamin - 2208656]",
    ]
    
    print_result_box("ABOUT THIS APPLICATION", info)
    
    pause()


# ============================================
# MAIN APPLICATION LOOP
# ============================================

def main():
    """Main application entry point."""
    
    while True:
        print_menu()
        
        choice = get_menu_choice()
        
        if choice == '1':
            scenario_fixed_investor()
            
        elif choice == '2':
            scenario_variable_investor()
            
        elif choice == '3':
            scenario_retirement_depletion()
            
        elif choice == '4':
            scenario_optimal_withdrawal()
            
        elif choice == '5':
            show_project_info()
            
        elif choice == '6':
            print_section_title("Exit")
            print(Colors.GOLD + "Thank you for using AofA Financial Services!" + Colors.RESET)
            print(Colors.NAVY + "Goodbye! 👋" + Colors.RESET)
            print()
            sys.exit(0)
            
        else:
            print_error("Invalid choice. Please select 1-6.")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + Colors.ERROR + "Program interrupted by user." + Colors.RESET)
        print(Colors.GOLD + "Goodbye!" + Colors.RESET)
        sys.exit(0)
    except Exception as e:
        print("\n" + Colors.ERROR + f"Unexpected error: {str(e)}" + Colors.RESET)

        sys.exit(1)

